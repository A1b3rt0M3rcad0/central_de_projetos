from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.entities.eap import EAPItemEntity
from ...domain.value_objects.eap_type import EAPType
from ...domain.value_objects.eap_status import EAPStatus


class IEAPItemRepository(ABC):
    """Interface para o repositório de itens da EAP"""
    
    @abstractmethod
    def create(self, item: EAPItemEntity) -> EAPItemEntity:
        """
        Cria um novo item da EAP
        
        Args:
            item: Entidade EAPItem a ser criada
            
        Returns:
            EAPItemEntity: O item criado com ID
        """
        pass
    
    @abstractmethod
    def find_by_id(self, item_id: int) -> Optional[EAPItemEntity]:
        """
        Busca um item pelo ID
        
        Args:
            item_id: ID do item
            
        Returns:
            EAPItemEntity: O item encontrado ou None
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
            EAPItemEntity: O item encontrado ou None
        """
        pass
    
    @abstractmethod
    def update(self, item: EAPItemEntity) -> EAPItemEntity:
        """
        Atualiza um item da EAP
        
        Args:
            item: Entidade EAPItem com dados atualizados
            
        Returns:
            EAPItemEntity: O item atualizado
        """
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> None:
        """
        Exclui um item da EAP
        
        Args:
            item_id: ID do item a ser excluído
        """
        pass
    
    @abstractmethod
    def count_children(self, parent_id: int) -> int:
        """
        Conta quantos filhos um item possui
        
        Args:
            parent_id: ID do item pai
            
        Returns:
            int: Número de filhos
        """
        pass
    
    @abstractmethod
    def get_children_budget_total(self, parent_id: int) -> float:
        """
        Calcula o orçamento total de todos os filhos de um item
        
        Args:
            parent_id: ID do item pai
            
        Returns:
            float: Soma do orçamento de todos os filhos
        """
        pass
    
    @abstractmethod
    def exists_by_code(self, eap_id: int, code: str) -> bool:
        """
        Verifica se um código já existe em uma EAP
        
        Args:
            eap_id: ID da EAP
            code: Código a ser verificado
            
        Returns:
            bool: True se o código existir
        """
        pass
