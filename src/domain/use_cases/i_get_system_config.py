"""Interface for Get System Config Use Case"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IGetSystemConfig(ABC):
    """Interface para buscar configurações do sistema"""
    
    @abstractmethod
    def execute(self, config_key: str = None) -> Dict[str, Any]:
        """
        Busca configurações do sistema
        
        Args:
            config_key: Chave específica ou None para buscar todas
        
        Returns:
            Dict com configurações
        """
        pass

