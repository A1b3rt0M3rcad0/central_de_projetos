"""Get System Config Use Case"""
from src.domain.use_cases.i_get_system_config import IGetSystemConfig
from src.data.interface.i_system_config_repository import ISystemConfigRepository
from typing import Dict, Any


class GetSystemConfig(IGetSystemConfig):
    """Use case para buscar configurações do sistema"""
    
    def __init__(self, system_config_repository: ISystemConfigRepository):
        self.__system_config_repository = system_config_repository
    
    def execute(self, config_key: str = None) -> Dict[str, Any]:
        """
        Busca configurações do sistema
        
        Args:
            config_key: Chave específica ou None para buscar todas
        
        Returns:
            Dict com configurações
        """
        if config_key:
            # Buscar configuração específica
            config = self.__system_config_repository.find_by_key(config_key)
            if not config:
                return {'configs': []}
            
            return {
                'configs': [{
                    'id': config.config_id,
                    'key': config.config_key,
                    'value': config.config_value,
                    'parsed_value': config.get_parsed_value(),
                    'description': config.description,
                    'type': config.config_type,
                    'is_active': config.is_active
                }]
            }
        
        # Buscar todas as configurações ativas
        configs = self.__system_config_repository.find_all_active()
        return {
            'configs': [
                {
                    'id': config.config_id,
                    'key': config.config_key,
                    'value': config.config_value,
                    'parsed_value': config.get_parsed_value(),
                    'description': config.description,
                    'type': config.config_type,
                    'is_active': config.is_active
                }
                for config in configs
            ]
        }

