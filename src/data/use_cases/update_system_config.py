"""Update System Config Use Case"""
from src.domain.use_cases.i_update_system_config import IUpdateSystemConfig
from src.data.interface.i_system_config_repository import ISystemConfigRepository


class UpdateSystemConfig(IUpdateSystemConfig):
    """Use case para atualizar configuração do sistema"""
    
    def __init__(self, system_config_repository: ISystemConfigRepository):
        self.__system_config_repository = system_config_repository
    
    def execute(self, config_key: str, new_value: str) -> None:
        """
        Atualiza o valor de uma configuração do sistema
        
        Args:
            config_key: Chave da configuração
            new_value: Novo valor (string, JSON, etc)
        """
        self.__system_config_repository.update_value(config_key, new_value)

