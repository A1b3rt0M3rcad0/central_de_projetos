from abc import ABC, abstractmethod
from src.domain.entities.system_config import SystemConfigEntity
from typing import List, Optional


class ISystemConfigRepository(ABC):
    """Interface do repositório de configurações do sistema"""
    
    @abstractmethod
    def find_by_key(self, config_key: str) -> Optional[SystemConfigEntity]:
        """Busca uma configuração pela chave"""
        pass
    
    @abstractmethod
    def find_all_active(self) -> List[SystemConfigEntity]:
        """Busca todas as configurações ativas"""
        pass
    
    @abstractmethod
    def update_value(self, config_key: str, new_value: str) -> None:
        """Atualiza o valor de uma configuração"""
        pass
    
    @abstractmethod
    def get_dashboard_excluded_status(self) -> List[int]:
        """Retorna lista de IDs de status excluídos do dashboard"""
        pass

