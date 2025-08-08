"""
Machine learning models for chemical property prediction.

This module provides various ML model implementations optimized for
chemical property prediction tasks.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import logging
from abc import ABC, abstractmethod
import warnings

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
    from sklearn.svm import SVR
    from sklearn.neural_network import MLPRegressor
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. ML functionality will be limited.")

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

logger = logging.getLogger(__name__)


class BaseMLModel(ABC):
    """Abstract base class for machine learning models."""
    
    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray, validation_split: float = 0.2) -> Dict[str, Any]:
        """Train the model on the given data."""
        pass
    
    @abstractmethod
    def predict(self, X: Union[np.ndarray, List], return_uncertainty: bool = False) -> Union[float, Tuple[float, float]]:
        """Make predictions on new data."""
        pass
    
    @abstractmethod
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Evaluate the model on test data."""
        pass


class ChemicalMLModel(BaseMLModel):
    """
    Main machine learning model class for chemical property prediction.
    
    Supports various ML algorithms including Random Forest, Gradient Boosting,
    Linear models, SVM, Neural Networks, and XGBoost.
    """
    
    SUPPORTED_MODELS = {
        'random_forest': 'Random Forest Regressor',
        'gradient_boosting': 'Gradient Boosting Regressor',
        'linear': 'Linear Regression',
        'ridge': 'Ridge Regression',
        'lasso': 'Lasso Regression',
        'elastic_net': 'Elastic Net Regression',
        'svr': 'Support Vector Regression',
        'neural_network': 'Multi-layer Perceptron',
        'xgboost': 'XGBoost Regressor'
    }
    
    def __init__(self, model_type: str = "random_forest", **kwargs):
        """
        Initialize the ChemicalMLModel.
        
        Args:
            model_type: Type of ML model to use
            **kwargs: Additional parameters for the specific model
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for ML functionality")
        
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = None
        
        # Initialize the specific model
        self._initialize_model(**kwargs)
    
    def _initialize_model(self, **kwargs):
        """Initialize the specific ML model based on model_type."""
        if self.model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', None),
                min_samples_split=kwargs.get('min_samples_split', 2),
                min_samples_leaf=kwargs.get('min_samples_leaf', 1),
                random_state=kwargs.get('random_state', 42),
                n_jobs=kwargs.get('n_jobs', -1)
            )
        
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                learning_rate=kwargs.get('learning_rate', 0.1),
                max_depth=kwargs.get('max_depth', 3),
                random_state=kwargs.get('random_state', 42)
            )
        
        elif self.model_type == 'linear':
            self.model = LinearRegression()
        
        elif self.model_type == 'ridge':
            self.model = Ridge(
                alpha=kwargs.get('alpha', 1.0),
                random_state=kwargs.get('random_state', 42)
            )
        
        elif self.model_type == 'lasso':
            self.model = Lasso(
                alpha=kwargs.get('alpha', 1.0),
                random_state=kwargs.get('random_state', 42)
            )
        
        elif self.model_type == 'elastic_net':
            self.model = ElasticNet(
                alpha=kwargs.get('alpha', 1.0),
                l1_ratio=kwargs.get('l1_ratio', 0.5),
                random_state=kwargs.get('random_state', 42)
            )
        
        elif self.model_type == 'svr':
            self.model = SVR(
                kernel=kwargs.get('kernel', 'rbf'),
                C=kwargs.get('C', 1.0),
                gamma=kwargs.get('gamma', 'scale')
            )
        
        elif self.model_type == 'neural_network':
            self.model = MLPRegressor(
                hidden_layer_sizes=kwargs.get('hidden_layer_sizes', (100,)),
                activation=kwargs.get('activation', 'relu'),
                solver=kwargs.get('solver', 'adam'),
                alpha=kwargs.get('alpha', 0.0001),
                learning_rate=kwargs.get('learning_rate', 'constant'),
                max_iter=kwargs.get('max_iter', 1000),
                random_state=kwargs.get('random_state', 42)
            )
        
        elif self.model_type == 'xgboost':
            if not XGBOOST_AVAILABLE:
                raise ImportError("XGBoost is not available. Please install xgboost package.")
            self.model = xgb.XGBRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                learning_rate=kwargs.get('learning_rate', 0.1),
                max_depth=kwargs.get('max_depth', 6),
                random_state=kwargs.get('random_state', 42)
            )
        
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}. "
                           f"Supported types: {list(self.SUPPORTED_MODELS.keys())}")
    
    def train(self, X: np.ndarray, y: np.ndarray, validation_split: float = 0.2) -> Dict[str, Any]:
        """
        Train the model on the given data.
        
        Args:
            X: Feature matrix
            y: Target values
            validation_split: Fraction of data to use for validation
            
        Returns:
            Dictionary containing training metrics
        """
        logger.info(f"Training {self.SUPPORTED_MODELS[self.model_type]} on {len(X)} samples")
        
        # Split data for validation
        if validation_split > 0:
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=validation_split, random_state=42
            )
        else:
            X_train, X_val, y_train, y_val = X, None, y, None
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        # Calculate training metrics
        train_pred = self.model.predict(X_train_scaled)
        train_metrics = self._calculate_metrics(y_train, train_pred)
        
        metrics = {
            'model_type': self.model_type,
            'n_samples': len(X),
            'n_features': X.shape[1],
            'train_r2': train_metrics['r2'],
            'train_rmse': train_metrics['rmse'],
            'train_mae': train_metrics['mae']
        }
        
        # Validation metrics if validation split is used
        if X_val is not None:
            X_val_scaled = self.scaler.transform(X_val)
            val_pred = self.model.predict(X_val_scaled)
            val_metrics = self._calculate_metrics(y_val, val_pred)
            
            metrics.update({
                'val_r2': val_metrics['r2'],
                'val_rmse': val_metrics['rmse'],
                'val_mae': val_metrics['mae']
            })
        
        # Cross-validation score
        try:
            cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5, scoring='r2')
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()
        except Exception as e:
            logger.warning(f"Could not calculate cross-validation scores: {e}")
        
        return metrics
    
    def predict(self, X: Union[np.ndarray, List], return_uncertainty: bool = False) -> Union[float, Tuple[float, float]]:
        """
        Make predictions on new data.
        
        Args:
            X: Feature vector or matrix
            return_uncertainty: Whether to return prediction uncertainty
            
        Returns:
            Predicted value(s), optionally with uncertainty estimate
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Handle single sample
        if isinstance(X, list):
            X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)
        
        if return_uncertainty:
            # Estimate uncertainty for ensemble models
            uncertainty = self._estimate_uncertainty(X_scaled)
            if len(prediction) == 1:
                return prediction[0], uncertainty
            else:
                return prediction, uncertainty
        
        return prediction[0] if len(prediction) == 1 else prediction
    
    def batch_predict(self, X_list: List[np.ndarray]) -> List[float]:
        """
        Make predictions on multiple samples efficiently.
        
        Args:
            X_list: List of feature vectors
            
        Returns:
            List of predicted values
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Stack all feature vectors
        X = np.vstack(X_list)
        
        # Scale and predict
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        return predictions.tolist()
    
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Evaluate the model on test data.
        
        Args:
            X: Test feature matrix
            y: True target values
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Scale features and predict
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        # Calculate metrics
        metrics = self._calculate_metrics(y, predictions)
        metrics['n_test_samples'] = len(y)
        
        return metrics
    
    def get_feature_importance(self) -> np.ndarray:
        """
        Get feature importance scores.
        
        Returns:
            Array of feature importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
        
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            return np.abs(self.model.coef_)
        else:
            logger.warning(f"Feature importance not available for {self.model_type}")
            return np.array([])
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate regression metrics."""
        return {
            'r2': r2_score(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred)
        }
    
    def _estimate_uncertainty(self, X: np.ndarray) -> float:
        """
        Estimate prediction uncertainty.
        
        For ensemble models, uses prediction variance.
        For other models, returns a simple heuristic.
        """
        if self.model_type in ['random_forest', 'gradient_boosting']:
            # For ensemble models, use prediction variance
            if hasattr(self.model, 'estimators_'):
                predictions = np.array([
                    estimator.predict(X) for estimator in self.model.estimators_
                ])
                return np.std(predictions, axis=0).mean()
        
        # Simple heuristic for other models
        return 0.1  # Default uncertainty estimate
    
    @classmethod
    def get_supported_models(cls) -> Dict[str, str]:
        """Get dictionary of supported model types and their descriptions."""
        return cls.SUPPORTED_MODELS.copy()


class EnsembleModel(BaseMLModel):
    """
    Ensemble model that combines multiple ChemicalMLModel instances.
    """
    
    def __init__(self, model_configs: List[Dict[str, Any]]):
        """
        Initialize ensemble model.
        
        Args:
            model_configs: List of model configuration dictionaries
        """
        self.models = []
        for config in model_configs:
            model_type = config.pop('model_type', 'random_forest')
            model = ChemicalMLModel(model_type=model_type, **config)
            self.models.append(model)
        
        self.is_trained = False
    
    def train(self, X: np.ndarray, y: np.ndarray, validation_split: float = 0.2) -> Dict[str, Any]:
        """Train all models in the ensemble."""
        all_metrics = []
        
        for i, model in enumerate(self.models):
            logger.info(f"Training ensemble model {i+1}/{len(self.models)}")
            metrics = model.train(X, y, validation_split)
            all_metrics.append(metrics)
        
        self.is_trained = True
        
        # Aggregate metrics
        ensemble_metrics = {
            'n_models': len(self.models),
            'model_types': [model.model_type for model in self.models]
        }
        
        # Average performance metrics
        for metric in ['train_r2', 'train_rmse', 'train_mae', 'val_r2', 'val_rmse', 'val_mae']:
            values = [m.get(metric) for m in all_metrics if m.get(metric) is not None]
            if values:
                ensemble_metrics[f'avg_{metric}'] = np.mean(values)
                ensemble_metrics[f'std_{metric}'] = np.std(values)
        
        return ensemble_metrics
    
    def predict(self, X: Union[np.ndarray, List], return_uncertainty: bool = False) -> Union[float, Tuple[float, float]]:
        """Make ensemble predictions by averaging individual model predictions."""
        if not self.is_trained:
            raise ValueError("Ensemble must be trained before making predictions")
        
        predictions = []
        for model in self.models:
            pred = model.predict(X, return_uncertainty=False)
            predictions.append(pred)
        
        ensemble_pred = np.mean(predictions)
        
        if return_uncertainty:
            uncertainty = np.std(predictions)
            return ensemble_pred, uncertainty
        
        return ensemble_pred
    
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Evaluate the ensemble model."""
        if not self.is_trained:
            raise ValueError("Ensemble must be trained before evaluation")
        
        # Get ensemble predictions
        predictions = []
        for i in range(len(X)):
            pred = self.predict(X[i])
            predictions.append(pred)
        
        predictions = np.array(predictions)
        
        # Calculate ensemble metrics
        metrics = {
            'ensemble_r2': r2_score(y, predictions),
            'ensemble_rmse': np.sqrt(mean_squared_error(y, predictions)),
            'ensemble_mae': mean_absolute_error(y, predictions),
            'n_models': len(self.models)
        }
        
        return metrics