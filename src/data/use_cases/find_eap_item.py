from typing import List, Optional

from src.domain.entities.eap import EAPItemEntity
from src.domain.use_cases.i_find_eap_item import IFindEAPItem
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.domain.value_objects.eap_type import EAPType
from src.domain.value_objects.eap_status import EAPStatus


class FindEAPItem(IFindEAPItem):
    """Caso de uso para busca de itens da EAP"""
    
    def __init__(self, eap_item_repository: IEAPItemRepository):
        self.__eap_item_repository = eap_item_repository
    
    def find_by_id(self, item_id: int) -> Optional[EAPItemEntity]:
        """
        Busca um item pelo ID
        
        Args:
            item_id: ID do item
            
        Returns:
            EAPItemEntity: O item encontrado ou None se não existir
        """
        return self.__eap_item_repository.find_by_id(item_id)
    
    def find_by_eap_id(self, eap_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPItemEntity]: Lista de itens da EAP
        """
        return self.__eap_item_repository.find_by_eap_id(eap_id)
    
    def find_by_parent_id(self, parent_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens filhos de um item específico
        
        Args:
            parent_id: ID do item pai
            
        Returns:
            List[EAPItemEntity]: Lista de itens filhos
        """
        return self.__eap_item_repository.find_by_parent_id(parent_id)
    
    def find_root_items(self, eap_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens raiz de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPItemEntity]: Lista de itens raiz
        """
        return self.__eap_item_repository.find_root_items(eap_id)
    
    def find_by_type(self, eap_id: int, eap_type: EAPType) -> List[EAPItemEntity]:
        """
        Busca todos os itens de um tipo específico em uma EAP
        
        Args:
            eap_id: ID da EAP
            eap_type: Tipo dos itens
            
        Returns:
            List[EAPItemEntity]: Lista de itens do tipo especificado
        """
        return self.__eap_item_repository.find_by_type(eap_id, eap_type)
    
    def find_by_status(self, eap_id: int, status: EAPStatus) -> List[EAPItemEntity]:
        """
        Busca todos os itens com um status específico em uma EAP
        
        Args:
            eap_id: ID da EAP
            status: Status dos itens
            
        Returns:
            List[EAPItemEntity]: Lista de itens com o status especificado
        """
        return self.__eap_item_repository.find_by_status(eap_id, status)
    
    def find_by_code(self, eap_id: int, code: str) -> Optional[EAPItemEntity]:
        """
        Busca um item pelo código em uma EAP específica
        
        Args:
            eap_id: ID da EAP
            code: Código do item
            
        Returns:
            EAPItemEntity: O item encontrado ou None se não existir
        """
        return self.__eap_item_repository.find_by_code(eap_id, code)
