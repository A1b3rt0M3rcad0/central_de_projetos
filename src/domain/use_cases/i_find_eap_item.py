from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.eap import EAPItemEntity
from ..value_objects.eap_type import EAPType
from ..value_objects.eap_status import EAPStatus


class IFindEAPItem(ABC):
    """Interface para o caso de uso de busca de itens da EAP"""
    
    @abstractmethod
    def find_by_id(self, item_id: int) -> Optional[EAPItemEntity]:
        """
        Busca um item pelo ID
        
        Args:
            item_id: ID do item
            
        Returns:
            EAPItemEntity: O item encontrado ou None se não existir
        """
        pass
    
    @abstractmethod
    def find_by_eap_id(self, eap_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPItemEntity]: Lista de itens da EAP
        """
        pass
    
    @abstractmethod
    def find_by_parent_id(self, parent_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens filhos de um item específico
        
        Args:
            parent_id: ID do item pai
            
        Returns:
            List[EAPItemEntity]: Lista de itens filhos
        """
        pass
    
    @abstractmethod
    def find_root_items(self, eap_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens raiz de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPItemEntity]: Lista de itens raiz
        """
        pass
    
    @abstractmethod
    def find_by_type(self, eap_id: int, eap_type: EAPType) -> List[EAPItemEntity]:
        """
        Busca todos os itens de um tipo específico em uma EAP
        
        Args:
            eap_id: ID da EAP
            eap_type: Tipo dos itens
            
        Returns:
            List[EAPItemEntity]: Lista de itens do tipo especificado
        """
        pass
    
    @abstractmethod
    def find_by_status(self, eap_id: int, status: EAPStatus) -> List[EAPItemEntity]:
        """
        Busca todos os itens com um status específico em uma EAP
        
        Args:
            eap_id: ID da EAP
            status: Status dos itens
            
        Returns:
            List[EAPItemEntity]: Lista de itens com o status especificado
        """
        pass
    
    @abstractmethod
    def find_by_code(self, eap_id: int, code: str) -> Optional[EAPItemEntity]:
        """
        Busca um item pelo código em uma EAP específica
        
        Args:
            eap_id: ID da EAP
            code: Código do item
            
        Returns:
            EAPItemEntity: O item encontrado ou None se não existir
        """
        pass
