"""
Feature engineering module for chemical machine learning.

This module provides tools for preprocessing and engineering features
from molecular descriptors for use in machine learning models.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import logging
from abc import ABC, abstractmethod

try:
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
    from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
    from sklearn.decomposition import PCA
    from sklearn.impute import SimpleImputer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. Feature engineering functionality will be limited.")

logger = logging.getLogger(__name__)


class BaseFeatureProcessor(ABC):
    """Abstract base class for feature processors."""
    
    @abstractmethod
    def fit(self, X: np.ndarray) -> 'BaseFeatureProcessor':
        """Fit the processor to the data."""
        pass
    
    @abstractmethod
    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform the data."""
        pass
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform the data."""
        return self.fit(X).transform(X)


class FeatureEngineer:
    """
    Main class for feature engineering in chemical machine learning.
    
    Provides comprehensive feature preprocessing, selection, and engineering
    capabilities for molecular descriptors.
    """
    
    def __init__(self):
        """Initialize the FeatureEngineer."""
        self.processors: List[BaseFeatureProcessor] = []
        self.feature_names: List[str] = []
        self.is_fitted = False
        
        # Default feature processing pipeline
        self.scaler = None
        self.selector = None
        self.imputer = None
        self.dimensionality_reducer = None
        
        if not SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not available. Feature engineering will be limited.")
    
    def engineer_features(
        self, 
        descriptors: Dict[str, float],
        feature_names: Optional[List[str]] = None
    ) -> np.ndarray:
        """
        Engineer features from molecular descriptors.
        
        Args:
            descriptors: Dictionary of molecular descriptors
            feature_names: Optional list of feature names to use
            
        Returns:
            Engineered feature vector
        """
        # Convert descriptors to feature vector
        if feature_names is None:
            feature_names = sorted(descriptors.keys())
        
        features = np.array([descriptors.get(name, 0.0) for name in feature_names])
        
        # Apply additional feature engineering
        engineered_features = self._apply_feature_engineering(features, descriptors)
        
        return engineered_features
    
    def _apply_feature_engineering(
        self, 
        base_features: np.ndarray, 
        descriptors: Dict[str, float]
    ) -> np.ndarray:
        """
        Apply feature engineering transformations.
        
        Args:
            base_features: Base feature vector
            descriptors: Original descriptor dictionary
            
        Returns:
            Engineered feature vector
        """
        features = base_features.copy()
        
        # Add derived features
        derived_features = self._create_derived_features(descriptors)
        if derived_features.size > 0:
            features = np.concatenate([features, derived_features])
        
        # Add interaction features
        interaction_features = self._create_interaction_features(base_features)
        if interaction_features.size > 0:
            features = np.concatenate([features, interaction_features])
        
        # Add polynomial features
        poly_features = self._create_polynomial_features(base_features)
        if poly_features.size > 0:
            features = np.concatenate([features, poly_features])
        
        return features
    
    def _create_derived_features(self, descriptors: Dict[str, float]) -> np.ndarray:
        """
        Create derived features from molecular descriptors.
        
        Args:
            descriptors: Dictionary of molecular descriptors
            
        Returns:
            Array of derived features
        """
        derived = []
        
        # Molecular weight per atom
        if 'molecular_weight' in descriptors and 'num_atoms' in descriptors:
            if descriptors['num_atoms'] > 0:
                derived.append(descriptors['molecular_weight'] / descriptors['num_atoms'])
            else:
                derived.append(0.0)
        
        # Heavy atom fraction
        if 'num_heavy_atoms' in descriptors and 'num_atoms' in descriptors:
            if descriptors['num_atoms'] > 0:
                derived.append(descriptors['num_heavy_atoms'] / descriptors['num_atoms'])
            else:
                derived.append(0.0)
        
        # Bond density
        if 'num_bonds' in descriptors and 'num_atoms' in descriptors:
            if descriptors['num_atoms'] > 0:
                derived.append(descriptors['num_bonds'] / descriptors['num_atoms'])
            else:
                derived.append(0.0)
        
        # Heteroatom fraction
        if 'num_heteroatoms' in descriptors and 'num_atoms' in descriptors:
            if descriptors['num_atoms'] > 0:
                derived.append(descriptors['num_heteroatoms'] / descriptors['num_atoms'])
            else:
                derived.append(0.0)
        
        # Rotatable bond fraction
        if 'num_rotatable_bonds' in descriptors and 'num_bonds' in descriptors:
            if descriptors['num_bonds'] > 0:
                derived.append(descriptors['num_rotatable_bonds'] / descriptors['num_bonds'])
            else:
                derived.append(0.0)
        
        # H-bond donor/acceptor ratio
        if 'num_h_donors' in descriptors and 'num_h_acceptors' in descriptors:
            if descriptors['num_h_acceptors'] > 0:
                derived.append(descriptors['num_h_donors'] / descriptors['num_h_acceptors'])
            else:
                derived.append(descriptors['num_h_donors'])
        
        # Ring density
        if 'num_rings' in descriptors and 'num_atoms' in descriptors:
            if descriptors['num_atoms'] > 0:
                derived.append(descriptors['num_rings'] / descriptors['num_atoms'])
            else:
                derived.append(0.0)
        
        # Lipophilicity efficiency (LogP per heavy atom)
        if 'logp' in descriptors and 'num_heavy_atoms' in descriptors:
            if descriptors['num_heavy_atoms'] > 0:
                derived.append(descriptors['logp'] / descriptors['num_heavy_atoms'])
            else:
                derived.append(0.0)
        
        # TPSA efficiency (TPSA per heavy atom)
        if 'tpsa' in descriptors and 'num_heavy_atoms' in descriptors:
            if descriptors['num_heavy_atoms'] > 0:
                derived.append(descriptors['tpsa'] / descriptors['num_heavy_atoms'])
            else:
                derived.append(0.0)
        
        return np.array(derived)
    
    def _create_interaction_features(self, features: np.ndarray, max_interactions: int = 10) -> np.ndarray:
        """
        Create interaction features between existing features.
        
        Args:
            features: Base feature vector
            max_interactions: Maximum number of interaction features to create
            
        Returns:
            Array of interaction features
        """
        if len(features) < 2:
            return np.array([])
        
        interactions = []
        count = 0
        
        # Create pairwise interactions (products)
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                if count >= max_interactions:
                    break
                interactions.append(features[i] * features[j])
                count += 1
            if count >= max_interactions:
                break
        
        return np.array(interactions)
    
    def _create_polynomial_features(self, features: np.ndarray, degree: int = 2) -> np.ndarray:
        """
        Create polynomial features.
        
        Args:
            features: Base feature vector
            degree: Polynomial degree
            
        Returns:
            Array of polynomial features
        """
        if degree < 2:
            return np.array([])
        
        poly_features = []
        
        # Add squared terms
        if degree >= 2:
            poly_features.extend(features ** 2)
        
        # Add cubic terms for important features (first few)
        if degree >= 3 and len(features) > 0:
            n_cubic = min(5, len(features))  # Limit cubic terms
            poly_features.extend(features[:n_cubic] ** 3)
        
        return np.array(poly_features)
    
    def setup_preprocessing_pipeline(
        self,
        scaling_method: str = "standard",
        feature_selection_method: Optional[str] = None,
        n_features: Optional[int] = None,
        handle_missing: str = "mean",
        dimensionality_reduction: Optional[str] = None,
        n_components: Optional[int] = None
    ):
        """
        Set up the feature preprocessing pipeline.
        
        Args:
            scaling_method: Method for feature scaling ('standard', 'minmax', 'robust')
            feature_selection_method: Method for feature selection ('kbest', 'mutual_info')
            n_features: Number of features to select
            handle_missing: Method for handling missing values ('mean', 'median', 'most_frequent')
            dimensionality_reduction: Method for dimensionality reduction ('pca')
            n_components: Number of components for dimensionality reduction
        """
        if not SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not available. Preprocessing pipeline setup skipped.")
            return
        
        # Missing value imputation
        if handle_missing:
            self.imputer = SimpleImputer(strategy=handle_missing)
        
        # Feature scaling
        if scaling_method == "standard":
            self.scaler = StandardScaler()
        elif scaling_method == "minmax":
            self.scaler = MinMaxScaler()
        elif scaling_method == "robust":
            self.scaler = RobustScaler()
        
        # Feature selection
        if feature_selection_method and n_features:
            if feature_selection_method == "kbest":
                self.selector = SelectKBest(score_func=f_regression, k=n_features)
            elif feature_selection_method == "mutual_info":
                self.selector = SelectKBest(score_func=mutual_info_regression, k=n_features)
        
        # Dimensionality reduction
        if dimensionality_reduction == "pca" and n_components:
            self.dimensionality_reducer = PCA(n_components=n_components)
    
    def fit_preprocessing_pipeline(self, X: np.ndarray, y: Optional[np.ndarray] = None):
        """
        Fit the preprocessing pipeline to the data.
        
        Args:
            X: Feature matrix
            y: Target values (required for supervised feature selection)
        """
        if not SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not available. Pipeline fitting skipped.")
            return
        
        current_X = X.copy()
        
        # Fit imputer
        if self.imputer:
            self.imputer.fit(current_X)
            current_X = self.imputer.transform(current_X)
        
        # Fit scaler
        if self.scaler:
            self.scaler.fit(current_X)
            current_X = self.scaler.transform(current_X)
        
        # Fit feature selector
        if self.selector and y is not None:
            self.selector.fit(current_X, y)
            current_X = self.selector.transform(current_X)
        
        # Fit dimensionality reducer
        if self.dimensionality_reducer:
            self.dimensionality_reducer.fit(current_X)
        
        self.is_fitted = True
        logger.info("Preprocessing pipeline fitted successfully")
    
    def apply_preprocessing_pipeline(self, X: np.ndarray) -> np.ndarray:
        """
        Apply the fitted preprocessing pipeline to new data.
        
        Args:
            X: Feature matrix
            
        Returns:
            Preprocessed feature matrix
        """
        if not SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not available. Returning original features.")
            return X
        
        if not self.is_fitted:
            logger.warning("Preprocessing pipeline not fitted. Returning original features.")
            return X
        
        current_X = X.copy()
        
        # Apply imputer
        if self.imputer:
            current_X = self.imputer.transform(current_X)
        
        # Apply scaler
        if self.scaler:
            current_X = self.scaler.transform(current_X)
        
        # Apply feature selector
        if self.selector:
            current_X = self.selector.transform(current_X)
        
        # Apply dimensionality reducer
        if self.dimensionality_reducer:
            current_X = self.dimensionality_reducer.transform(current_X)
        
        return current_X
    
    def get_feature_names(self) -> List[str]:
        """
        Get the names of the engineered features.
        
        Returns:
            List of feature names
        """
        if not self.feature_names:
            # Generate default feature names
            base_names = [
                'molecular_weight', 'num_atoms', 'num_heavy_atoms', 'num_bonds',
                'num_heteroatoms', 'formal_charge', 'num_rotatable_bonds',
                'num_h_donors', 'num_h_acceptors', 'tpsa', 'logp', 'num_rings',
                'molecular_refractivity', 'balaban_j', 'bertz_ct', 'chi0v',
                'chi1v', 'kappa1', 'kappa2', 'kappa3'
            ]
            
            # Add derived feature names
            derived_names = [
                'mw_per_atom', 'heavy_atom_fraction', 'bond_density',
                'heteroatom_fraction', 'rotatable_bond_fraction',
                'hbd_hba_ratio', 'ring_density', 'lipophilicity_efficiency',
                'tpsa_efficiency'
            ]
            
            # Add interaction feature names (simplified)
            interaction_names = [f'interaction_{i}' for i in range(10)]
            
            # Add polynomial feature names
            poly_names = [f'poly_{name}_2' for name in base_names[:10]]
            poly_names.extend([f'poly_{name}_3' for name in base_names[:5]])
            
            self.feature_names = base_names + derived_names + interaction_names + poly_names
        
        return self.feature_names
    
    def get_feature_importance_analysis(
        self, 
        feature_importance: np.ndarray,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Analyze feature importance and provide insights.
        
        Args:
            feature_importance: Array of feature importance scores
            top_n: Number of top features to analyze
            
        Returns:
            Dictionary containing feature importance analysis
        """
        feature_names = self.get_feature_names()
        
        if len(feature_importance) != len(feature_names):
            logger.warning("Feature importance length doesn't match feature names length")
            feature_names = [f"feature_{i}" for i in range(len(feature_importance))]
        
        # Sort features by importance
        importance_pairs = list(zip(feature_names, feature_importance))
        importance_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
        
        analysis = {
            'top_features': importance_pairs[:top_n],
            'feature_categories': self._categorize_features(importance_pairs[:top_n]),
            'importance_statistics': {
                'mean': np.mean(feature_importance),
                'std': np.std(feature_importance),
                'max': np.max(feature_importance),
                'min': np.min(feature_importance)
            }
        }
        
        return analysis
    
    def _categorize_features(self, feature_importance_pairs: List[Tuple[str, float]]) -> Dict[str, List[Tuple[str, float]]]:
        """
        Categorize features by type for analysis.
        
        Args:
            feature_importance_pairs: List of (feature_name, importance) tuples
            
        Returns:
            Dictionary mapping categories to feature lists
        """
        categories = {
            'molecular_properties': [],
            'structural_features': [],
            'derived_features': [],
            'interaction_features': [],
            'polynomial_features': []
        }
        
        for name, importance in feature_importance_pairs:
            if any(prop in name.lower() for prop in ['weight', 'charge', 'tpsa', 'logp', 'refractivity']):
                categories['molecular_properties'].append((name, importance))
            elif any(struct in name.lower() for struct in ['atom', 'bond', 'ring', 'donor', 'acceptor']):
                categories['structural_features'].append((name, importance))
            elif any(derived in name.lower() for derived in ['fraction', 'density', 'ratio', 'efficiency']):
                categories['derived_features'].append((name, importance))
            elif 'interaction' in name.lower():
                categories['interaction_features'].append((name, importance))
            elif 'poly' in name.lower():
                categories['polynomial_features'].append((name, importance))
            else:
                categories['molecular_properties'].append((name, importance))  # Default category
        
        return categories
    
    def create_feature_matrix(
        self, 
        descriptor_list: List[Dict[str, float]],
        apply_preprocessing: bool = True
    ) -> np.ndarray:
        """
        Create a feature matrix from a list of descriptor dictionaries.
        
        Args:
            descriptor_list: List of descriptor dictionaries
            apply_preprocessing: Whether to apply preprocessing pipeline
            
        Returns:
            Feature matrix
        """
        if not descriptor_list:
            return np.array([])
        
        # Get feature names from first descriptor
        feature_names = sorted(descriptor_list[0].keys())
        
        # Create feature matrix
        feature_matrix = []
        for descriptors in descriptor_list:
            features = self.engineer_features(descriptors, feature_names)
            feature_matrix.append(features)
        
        feature_matrix = np.array(feature_matrix)
        
        # Apply preprocessing if requested and pipeline is fitted
        if apply_preprocessing and self.is_fitted:
            feature_matrix = self.apply_preprocessing_pipeline(feature_matrix)
        
        return feature_matrix
    
    def save_feature_engineering_config(self, filepath: str):
        """
        Save the feature engineering configuration.
        
        Args:
            filepath: Path to save the configuration
        """
        import json
        
        config = {
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted,
            'has_imputer': self.imputer is not None,
            'has_scaler': self.scaler is not None,
            'has_selector': self.selector is not None,
            'has_dimensionality_reducer': self.dimensionality_reducer is not None
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Feature engineering configuration saved to {filepath}")
    
    def load_feature_engineering_config(self, filepath: str):
        """
        Load the feature engineering configuration.
        
        Args:
            filepath: Path to load the configuration from
        """
        import json
        
        with open(filepath, 'r') as f:
            config = json.load(f)
        
        self.feature_names = config.get('feature_names', [])
        self.is_fitted = config.get('is_fitted', False)
        
        logger.info(f"Feature engineering configuration loaded from {filepath}")