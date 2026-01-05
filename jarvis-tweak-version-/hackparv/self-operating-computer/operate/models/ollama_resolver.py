"""
Ollama Model Resolver

This module provides functionality to resolve, validate, and manage Ollama models
for the self-operating-computer framework.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
import ollama
from operate.config import Config
from operate.utils.style import ANSI_GREEN, ANSI_RED, ANSI_RESET, ANSI_BRIGHT_MAGENTA


@dataclass
class ModelInfo:
    """Information about an Ollama model."""
    name: str
    size: str
    modified: datetime
    family: str = ""
    format: str = ""


class OllamaModelResolver:
    """Resolves and validates Ollama model specifications."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization of Ollama client."""
        if self._client is None:
            self._client = self.config.initialize_ollama()
        return self._client
    
    def resolve_model(self, model_spec: str) -> str:
        """
        Resolve model specification to actual model name.
        
        Args:
            model_spec: Can be "llava", "ollama:llava:7b", or "ollama"
            
        Returns:
            Actual model name to use with Ollama client
            
        Raises:
            ValueError: If model specification is invalid or model not found
        """
        if self.config.verbose:
            print(f"[OllamaModelResolver] Resolving model spec: {model_spec}")
        
        # Handle legacy format (backward compatibility)
        if model_spec == "llava":
            return "llava"
        
        # Handle explicit format: ollama:model_name
        if model_spec.startswith("ollama:"):
            model_name = model_spec[7:]  # Remove "ollama:" prefix
            if not model_name:
                raise ValueError("Model name cannot be empty after 'ollama:' prefix")
            return model_name
        
        # Handle auto-resolve format: "ollama"
        if model_spec == "ollama":
            # Try to get configured default first
            default_model = self.config.get_default_ollama_model()
            if default_model:
                if self.config.verbose:
                    print(f"[OllamaModelResolver] Using configured default: {default_model}")
                return default_model
            
            # Fall back to "llava" for backward compatibility
            if self.config.verbose:
                print("[OllamaModelResolver] No default configured, falling back to 'llava'")
            return "llava"
        
        # If we get here, it's an unrecognized format
        raise ValueError(
            f"Invalid model specification: '{model_spec}'. "
            f"Use 'llava', 'ollama:model_name', or 'ollama'"
        )
    
    def validate_model(self, model_name: str) -> bool:
        """
        Validate that a model exists and is accessible.
        
        Args:
            model_name: Name of the model to validate
            
        Returns:
            True if model exists and is accessible, False otherwise
        """
        try:
            available_models = self.list_available_models()
            model_names = [model.name for model in available_models]
            
            if self.config.verbose:
                print(f"[OllamaModelResolver] Validating model '{model_name}' against available: {model_names}")
            
            return model_name in model_names
        
        except Exception as e:
            if self.config.verbose:
                print(f"[OllamaModelResolver] Error validating model: {e}")
            return False
    
    def list_available_models(self) -> List[ModelInfo]:
        """
        List all locally available Ollama models.
        
        Returns:
            List of ModelInfo objects for available models
            
        Raises:
            ConnectionError: If Ollama service is not available
        """
        try:
            response = self.client.list()
            models = []
            
            # Handle both dict and object responses from Ollama
            model_list = response.models if hasattr(response, 'models') else response.get('models', [])
            
            for model_data in model_list:
                # Handle both dict and object formats
                if hasattr(model_data, 'model'):
                    # Object format
                    name = model_data.model
                    size = self._format_size(model_data.size)
                    modified = model_data.modified_at
                    details = model_data.details if hasattr(model_data, 'details') else None
                    family = details.family if details and hasattr(details, 'family') else ''
                    format_type = details.format if details and hasattr(details, 'format') else ''
                else:
                    # Dict format (fallback)
                    name = model_data.get('name', '')
                    size = self._format_size(model_data.get('size', 0))
                    modified_str = model_data.get('modified_at', '')
                    
                    # Parse the modified date
                    try:
                        # Handle different datetime formats from Ollama
                        if isinstance(modified_str, str):
                            # Remove 'Z' and replace with timezone info
                            if modified_str.endswith('Z'):
                                modified_str = modified_str[:-1] + '+00:00'
                            modified = datetime.fromisoformat(modified_str)
                        else:
                            modified = datetime.now()
                    except (ValueError, AttributeError, TypeError):
                        modified = datetime.now()
                    
                    family = model_data.get('details', {}).get('family', '')
                    format_type = model_data.get('details', {}).get('format', '')
                
                model_info = ModelInfo(
                    name=name,
                    size=size,
                    modified=modified,
                    family=family,
                    format=format_type
                )
                models.append(model_info)
            
            if self.config.verbose:
                print(f"[OllamaModelResolver] Found {len(models)} available models")
            
            return models
        
        except ollama.ResponseError as e:
            if "connection" in str(e).lower():
                raise ConnectionError(
                    "Cannot connect to Ollama service. "
                    "Please ensure Ollama is running with 'ollama serve'"
                ) from e
            raise
        except Exception as e:
            raise ConnectionError(f"Error connecting to Ollama: {e}") from e
    
    def get_model_suggestions(self, invalid_model: str, max_suggestions: int = 3) -> List[str]:
        """
        Get model suggestions for an invalid model name.
        
        Args:
            invalid_model: The invalid model name
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of suggested model names
        """
        try:
            available_models = self.list_available_models()
            model_names = [model.name for model in available_models]
            
            # Simple suggestion logic: find models that contain similar text
            suggestions = []
            invalid_lower = invalid_model.lower()
            
            # First, look for exact substring matches
            for name in model_names:
                if invalid_lower in name.lower() or name.lower() in invalid_lower:
                    suggestions.append(name)
            
            # If we don't have enough suggestions, add popular models
            if len(suggestions) < max_suggestions:
                popular_models = ['llava', 'llava:7b', 'llama2', 'codellama']
                for popular in popular_models:
                    if popular in model_names and popular not in suggestions:
                        suggestions.append(popular)
                        if len(suggestions) >= max_suggestions:
                            break
            
            # If still not enough, just add the first available models
            if len(suggestions) < max_suggestions:
                for name in model_names:
                    if name not in suggestions:
                        suggestions.append(name)
                        if len(suggestions) >= max_suggestions:
                            break
            
            return suggestions[:max_suggestions]
        
        except Exception:
            # If we can't get suggestions, return some common defaults
            return ['llava', 'llava:7b', 'llama2']
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human-readable format."""
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(size_bytes)
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"
    
    def print_model_list(self, models: List[ModelInfo]) -> None:
        """Print a formatted list of models."""
        if not models:
            print(f"{ANSI_RED}No Ollama models found.{ANSI_RESET}")
            print(f"{ANSI_BRIGHT_MAGENTA}To install models, try:{ANSI_RESET}")
            print("  ollama pull llava")
            print("  ollama pull llava:7b")
            print("  ollama pull llama2")
            return
        
        print(f"{ANSI_GREEN}Available Ollama models:{ANSI_RESET}")
        print(f"{'NAME':<20} {'SIZE':<10} {'MODIFIED':<20}")
        print("-" * 50)
        
        for model in models:
            modified_str = model.modified.strftime("%Y-%m-%d %H:%M")
            print(f"{model.name:<20} {model.size:<10} {modified_str:<20}")
    
    def validate_and_resolve(self, model_spec: str) -> Tuple[str, bool]:
        """
        Validate and resolve a model specification.
        
        Args:
            model_spec: Model specification to resolve and validate
            
        Returns:
            Tuple of (resolved_model_name, is_valid)
        """
        try:
            resolved_model = self.resolve_model(model_spec)
            is_valid = self.validate_model(resolved_model)
            return resolved_model, is_valid
        except ValueError:
            return model_spec, False