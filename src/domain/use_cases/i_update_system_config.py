"""Interface for Update System Config Use Case"""
from abc import ABC, abstractmethod


class IUpdateSystemConfig(ABC):
    """Interface para atualizar configuração do sistema"""
    
    @abstractmethod
    def execute(self, config_key: str, new_value: str) -> None:
        """
        Atualiza o valor de uma configuração do sistema
        
        Args:
            config_key: Chave da configuração
            new_value: Novo valor (string, JSON, etc)
        """
        pass

