"""
Property prediction module for machine learning-based chemical property estimation.

This module provides the main interface for predicting molecular properties
using machine learning models trained on molecular descriptors.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import logging
from pathlib import Path
import pickle
import json

from .descriptors import MolecularDescriptors
from .models import ChemicalMLModel
from .feature_engineering import FeatureEngineer
from chemesty.molecules.molecule import Molecule
from chemesty.molecules.file_formats import MolecularStructure

logger = logging.getLogger(__name__)


class PropertyPredictor:
    """
    Main class for predicting molecular properties using machine learning.
    
    This class provides a high-level interface for training and using ML models
    to predict various chemical properties from molecular structures.
    """
    
    def __init__(self, model_dir: Optional[str] = None):
        """
        Initialize the PropertyPredictor.
        
        Args:
            model_dir: Directory containing pre-trained models. If None,
                      uses default model directory.
        """
        self.descriptor_calculator = MolecularDescriptors()
        self.feature_engineer = FeatureEngineer()
        self.models: Dict[str, ChemicalMLModel] = {}
        self.model_dir = Path(model_dir) if model_dir else Path(__file__).parent / "models"
        self.model_dir.mkdir(exist_ok=True)
        
        # Load any existing models
        self._load_existing_models()
    
    def predict_property(
        self, 
        molecule: Union[Molecule, MolecularStructure], 
        property_name: str,
        return_uncertainty: bool = False
    ) -> Union[float, Tuple[float, float]]:
        """
        Predict a specific property for a molecule.
        
        Args:
            molecule: The molecule to predict properties for
            property_name: Name of the property to predict (e.g., 'logP', 'solubility')
            return_uncertainty: Whether to return prediction uncertainty
            
        Returns:
            Predicted property value, optionally with uncertainty estimate
            
        Raises:
            ValueError: If the property model is not available
        """
        if property_name not in self.models:
            raise ValueError(f"No model available for property '{property_name}'. "
                           f"Available properties: {list(self.models.keys())}")
        
        # Calculate descriptors
        descriptors = self.descriptor_calculator.calculate_all_descriptors(molecule)
        
        # Engineer features
        features = self.feature_engineer.engineer_features(descriptors)
        
        # Make prediction
        model = self.models[property_name]
        prediction = model.predict(features, return_uncertainty=return_uncertainty)
        
        logger.info(f"Predicted {property_name} for molecule: {prediction}")
        return prediction
    
    def predict_multiple_properties(
        self, 
        molecule: Union[Molecule, MolecularStructure],
        property_names: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Predict multiple properties for a molecule.
        
        Args:
            molecule: The molecule to predict properties for
            property_names: List of property names to predict. If None, predicts all available.
            
        Returns:
            Dictionary mapping property names to predicted values
        """
        if property_names is None:
            property_names = list(self.models.keys())
        
        results = {}
        for prop_name in property_names:
            try:
                results[prop_name] = self.predict_property(molecule, prop_name)
            except ValueError as e:
                logger.warning(f"Could not predict {prop_name}: {e}")
                results[prop_name] = None
        
        return results
    
    def batch_predict(
        self, 
        molecules: List[Union[Molecule, MolecularStructure]],
        property_name: str
    ) -> List[float]:
        """
        Predict a property for multiple molecules efficiently.
        
        Args:
            molecules: List of molecules to predict properties for
            property_name: Name of the property to predict
            
        Returns:
            List of predicted property values
        """
        if property_name not in self.models:
            raise ValueError(f"No model available for property '{property_name}'")
        
        # Calculate descriptors for all molecules
        all_descriptors = []
        for molecule in molecules:
            descriptors = self.descriptor_calculator.calculate_all_descriptors(molecule)
            features = self.feature_engineer.engineer_features(descriptors)
            all_descriptors.append(features)
        
        # Batch prediction
        model = self.models[property_name]
        predictions = model.batch_predict(all_descriptors)
        
        logger.info(f"Batch predicted {property_name} for {len(molecules)} molecules")
        return predictions
    
    def train_model(
        self,
        molecules: List[Union[Molecule, MolecularStructure]],
        property_values: List[float],
        property_name: str,
        model_type: str = "random_forest",
        validation_split: float = 0.2,
        **model_kwargs
    ) -> Dict[str, Any]:
        """
        Train a new model for property prediction.
        
        Args:
            molecules: Training molecules
            property_values: Target property values
            property_name: Name of the property being predicted
            model_type: Type of ML model to use
            validation_split: Fraction of data to use for validation
            **model_kwargs: Additional arguments for the model
            
        Returns:
            Training metrics and model information
        """
        logger.info(f"Training model for {property_name} with {len(molecules)} molecules")
        
        # Calculate descriptors and features
        X = []
        for molecule in molecules:
            descriptors = self.descriptor_calculator.calculate_all_descriptors(molecule)
            features = self.feature_engineer.engineer_features(descriptors)
            X.append(features)
        
        X = np.array(X)
        y = np.array(property_values)
        
        # Create and train model
        model = ChemicalMLModel(model_type=model_type, **model_kwargs)
        metrics = model.train(X, y, validation_split=validation_split)
        
        # Store the trained model
        self.models[property_name] = model
        
        # Save model to disk
        self._save_model(property_name, model)
        
        logger.info(f"Model training completed for {property_name}. Metrics: {metrics}")
        return metrics
    
    def evaluate_model(
        self,
        molecules: List[Union[Molecule, MolecularStructure]],
        property_values: List[float],
        property_name: str
    ) -> Dict[str, float]:
        """
        Evaluate a trained model on test data.
        
        Args:
            molecules: Test molecules
            property_values: True property values
            property_name: Name of the property
            
        Returns:
            Evaluation metrics
        """
        if property_name not in self.models:
            raise ValueError(f"No model available for property '{property_name}'")
        
        # Calculate features
        X = []
        for molecule in molecules:
            descriptors = self.descriptor_calculator.calculate_all_descriptors(molecule)
            features = self.feature_engineer.engineer_features(descriptors)
            X.append(features)
        
        X = np.array(X)
        y = np.array(property_values)
        
        # Evaluate model
        model = self.models[property_name]
        metrics = model.evaluate(X, y)
        
        logger.info(f"Model evaluation for {property_name}: {metrics}")
        return metrics
    
    def get_feature_importance(self, property_name: str) -> Dict[str, float]:
        """
        Get feature importance for a trained model.
        
        Args:
            property_name: Name of the property
            
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if property_name not in self.models:
            raise ValueError(f"No model available for property '{property_name}'")
        
        model = self.models[property_name]
        importance = model.get_feature_importance()
        
        # Map to feature names
        feature_names = self.feature_engineer.get_feature_names()
        if len(feature_names) == len(importance):
            return dict(zip(feature_names, importance))
        else:
            return {f"feature_{i}": imp for i, imp in enumerate(importance)}
    
    def list_available_properties(self) -> List[str]:
        """
        Get list of available property models.
        
        Returns:
            List of property names that can be predicted
        """
        return list(self.models.keys())
    
    def _load_existing_models(self):
        """Load any existing models from the model directory."""
        if not self.model_dir.exists():
            return
        
        for model_file in self.model_dir.glob("*.pkl"):
            property_name = model_file.stem
            try:
                with open(model_file, 'rb') as f:
                    model = pickle.load(f)
                self.models[property_name] = model
                logger.info(f"Loaded model for {property_name}")
            except Exception as e:
                logger.warning(f"Could not load model {model_file}: {e}")
    
    def _save_model(self, property_name: str, model: ChemicalMLModel):
        """Save a trained model to disk."""
        model_file = self.model_dir / f"{property_name}.pkl"
        try:
            with open(model_file, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"Saved model for {property_name} to {model_file}")
        except Exception as e:
            logger.error(f"Could not save model {property_name}: {e}")
    
    def save_predictions(
        self, 
        molecules: List[Union[Molecule, MolecularStructure]],
        predictions: Dict[str, List[float]],
        output_file: str
    ):
        """
        Save predictions to a file.
        
        Args:
            molecules: List of molecules
            predictions: Dictionary mapping property names to prediction lists
            output_file: Path to output file
        """
        results = []
        for i, molecule in enumerate(molecules):
            result = {"molecule_index": i}
            if hasattr(molecule, 'name'):
                result["molecule_name"] = molecule.name
            
            for prop_name, pred_list in predictions.items():
                if i < len(pred_list):
                    result[prop_name] = pred_list[i]
            
            results.append(result)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved predictions to {output_file}")