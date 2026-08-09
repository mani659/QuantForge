from typing import Tuple, Dict
from types import MappingProxyType

from boe.interpretation.models import InterpretationModelContract
from boe.interpretation.interpretation_errors import (
    DuplicateInterpretationModel,
    InterpretationModelNotFound,
    InvalidInterpretationModel,
    RegistryConfigurationError
)

class InterpretationRegistry:
    """
    Registry for managing Interpretation Models.
    It selects models but DOES NOT perform interpretation itself.
    Follows Open/Closed Principle by allowing registration of new models without modifying this class.
    Must be instantiated; no singleton/global mutable state.
    """
    
    def __init__(self, initial_models: Tuple[InterpretationModelContract, ...] = ()):
        self._models: Dict[str, InterpretationModelContract] = {}
        for model in initial_models:
            self.register(model)
            
    def register(self, model: InterpretationModelContract) -> None:
        if not isinstance(model, InterpretationModelContract):
            raise InvalidInterpretationModel("Model must implement InterpretationModelContract.")
            
        model_name = model.model_name
        if not model_name:
            raise InvalidInterpretationModel("Model must provide a non-empty model_name.")
            
        if model_name in self._models:
            raise DuplicateInterpretationModel(f"Model '{model_name}' is already registered.")
            
        self._models[model_name] = model

    def get_model(self, model_name: str) -> InterpretationModelContract:
        if not model_name:
            raise InterpretationModelNotFound("Model name cannot be empty.")
            
        model = self._models.get(model_name)
        if not model:
            raise InterpretationModelNotFound(f"Model '{model_name}' not found in registry.")
            
        return model

    def has_model(self, model_name: str) -> bool:
        return model_name in self._models

    @property
    def registered_models(self) -> Tuple[str, ...]:
        """Returns a deterministic, sorted tuple of registered model names."""
        return tuple(sorted(self._models.keys()))
