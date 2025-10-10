from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EAPCode:
    """Value Object que representa o código hierárquico de um item da EAP"""
    
    value: str
    
    def __post_init__(self):
        """Validações do código EAP"""
        if not self.value:
            raise ValueError("Código EAP não pode estar vazio")
        
        if not self._is_valid_format():
            raise ValueError("Formato do código EAP inválido")
    
    def _is_valid_format(self) -> bool:
        """Valida se o formato do código está correto (ex: 1, 1.1, 1.1.1)"""
        parts = self.value.split('.')
        
        # Verifica se todas as partes são números
        for part in parts:
            if not part.isdigit():
                return False
        
        # Verifica se não há zeros à esquerda
        for part in parts:
            if len(part) > 1 and part.startswith('0'):
                return False
        
        return True
    
    def get_level(self) -> int:
        """Retorna o nível hierárquico do código (1, 2, 3, etc.)"""
        return len(self.value.split('.'))
    
    def get_parent_code(self) -> 'EAPCode':
        """Retorna o código do item pai"""
        parts = self.value.split('.')
        if len(parts) <= 1:
            raise ValueError("Item raiz não possui pai")
        
        parent_parts = parts[:-1]
        return EAPCode('.'.join(parent_parts))
    
    def get_sibling_codes(self, count: int) -> List['EAPCode']:
        """Retorna códigos de irmãos (mesmo nível)"""
        parts = self.value.split('.')
        if len(parts) == 0:
            return []
        
        last_part = int(parts[-1])
        sibling_codes = []
        
        for i in range(1, count + 1):
            sibling_parts = parts[:-1] + [str(last_part + i)]
            sibling_codes.append(EAPCode('.'.join(sibling_parts)))
        
        return sibling_codes
    
    def get_child_codes(self, count: int) -> List['EAPCode']:
        """Retorna códigos de filhos"""
        child_codes = []
        
        for i in range(1, count + 1):
            child_code = f"{self.value}.{i}"
            child_codes.append(EAPCode(child_code))
        
        return child_codes
    
    def is_child_of(self, parent_code: 'EAPCode') -> bool:
        """Verifica se este código é filho de outro"""
        return self.value.startswith(parent_code.value + '.')
    
    def is_sibling_of(self, sibling_code: 'EAPCode') -> bool:
        """Verifica se este código é irmão de outro"""
        if self.get_level() != sibling_code.get_level():
            return False
        
        parts = self.value.split('.')
        sibling_parts = sibling_code.value.split('.')
        
        # Compara todas as partes exceto a última
        return parts[:-1] == sibling_parts[:-1]
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"EAPCode('{self.value}')"
