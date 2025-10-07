from datetime import datetime
from typing import Any
import json


class SystemConfigEntity:
    """Entidade de configuração do sistema"""
    
    def __init__(
        self,
        config_id: int,
        config_key: str,
        config_value: str = None,
        description: str = None,
        config_type: str = 'string',
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.config_id = config_id
        self.config_key = config_key
        self.config_value = config_value
        self.description = description
        self.config_type = config_type
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def get_parsed_value(self) -> Any:
        """Retorna o valor parseado de acordo com o tipo"""
        if not self.config_value:
            return None
        
        parsers = {
            'json': self._parse_json,
            'list': self._parse_list,
            'boolean': self._parse_boolean,
            'number': self._parse_number
        }
        
        parser = parsers.get(self.config_type)
        return parser() if parser else self.config_value
    
    def _parse_json(self) -> Any:
        """Parse JSON value"""
        try:
            return json.loads(self.config_value)
        except json.JSONDecodeError:
            return None
    
    def _parse_list(self) -> Any:
        """Parse list value"""
        try:
            return json.loads(self.config_value) if isinstance(self.config_value, str) else self.config_value
        except json.JSONDecodeError:
            return []
    
    def _parse_boolean(self) -> bool:
        """Parse boolean value"""
        if isinstance(self.config_value, str):
            return self.config_value.lower() in ('true', '1', 'yes')
        return bool(self.config_value)
    
    def _parse_number(self) -> Any:
        """Parse number value"""
        try:
            return int(self.config_value) if '.' not in str(self.config_value) else float(self.config_value)
        except (ValueError, TypeError):
            return 0
    
    def __repr__(self):
        return f"<SystemConfigEntity(key='{self.config_key}', value='{self.config_value}')>"

