from src.infra.relational.models.system_config import SystemConfig
from src.domain.entities.system_config import SystemConfigEntity
from src.data.interface.i_system_config_repository import ISystemConfigRepository
from src.errors.system_config_errors import SystemConfigNotFound, ErrorOnFindSystemConfig, ErrorOnUpdateSystemConfig
from typing import List, Optional
import json


class SystemConfigRepository(ISystemConfigRepository):
    """Repositório de configurações do sistema"""
    
    def __init__(self, db_connection_handler):
        self.__db_connection_handler = db_connection_handler
    
    def find_by_key(self, config_key: str) -> Optional[SystemConfigEntity]:
        """Busca uma configuração pela chave"""
        try:
            with self.__db_connection_handler as db:
                config = db.session.query(SystemConfig).filter(
                    SystemConfig.config_key == config_key,
                    SystemConfig.is_active.is_(True)
                ).first()
                
                if not config:
                    return None
                
                return SystemConfigEntity(
                    config_id=config.id,
                    config_key=config.config_key,
                    config_value=config.config_value,
                    description=config.description,
                    config_type=config.config_type,
                    is_active=config.is_active,
                    created_at=config.created_at,
                    updated_at=config.updated_at
                )
        except Exception as e:
            raise ErrorOnFindSystemConfig(
                message=f'Error on find system config by key={config_key}: {str(e)}'
            ) from e
    
    def find_all_active(self) -> List[SystemConfigEntity]:
        """Busca todas as configurações ativas"""
        try:
            with self.__db_connection_handler as db:
                configs = db.session.query(SystemConfig).filter(
                    SystemConfig.is_active.is_(True)
                ).all()
                
                return [
                    SystemConfigEntity(
                        config_id=config.id,
                        config_key=config.config_key,
                        config_value=config.config_value,
                        description=config.description,
                        config_type=config.config_type,
                        is_active=config.is_active,
                        created_at=config.created_at,
                        updated_at=config.updated_at
                    )
                    for config in configs
                ]
        except Exception as e:
            raise ErrorOnFindSystemConfig(
                message=f'Error on find all system configs: {str(e)}'
            ) from e
    
    def update_value(self, config_key: str, new_value: str) -> None:
        """Atualiza o valor de uma configuração"""
        try:
            with self.__db_connection_handler as db:
                config = db.session.query(SystemConfig).filter(
                    SystemConfig.config_key == config_key
                ).first()
                
                if not config:
                    raise SystemConfigNotFound(
                        message=f'System config with key={config_key} not found'
                    )
                
                db.session.query(SystemConfig).filter(
                    SystemConfig.config_key == config_key
                ).update({'config_value': new_value})
                
                db.session.commit()
        except SystemConfigNotFound as e:
            raise e from e
        except Exception as e:
            raise ErrorOnUpdateSystemConfig(
                message=f'Error on update system config key={config_key}: {str(e)}'
            ) from e
    
    def get_dashboard_excluded_status(self) -> List[int]:
        """Retorna lista de IDs de status excluídos do dashboard"""
        try:
            config = self.find_by_key('dashboard.excluded_status')
            if not config:
                return []
            
            parsed_value = config.get_parsed_value()
            if isinstance(parsed_value, list):
                return [int(x) for x in parsed_value if str(x).isdigit()]
            return []
        except Exception:
            # Se houver erro, retorna lista vazia para não quebrar o dashboard
            return []

