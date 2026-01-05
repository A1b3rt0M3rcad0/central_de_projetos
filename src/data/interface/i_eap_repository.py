from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.entities.eap import EAPEntity


class IEAPRepository(ABC):
    """Interface para o repositório de EAP"""
    
    @abstractmethod
    def create(self, eap: EAPEntity) -> EAPEntity:
        """
        Cria uma nova EAP
        
        Args:
            eap: Entidade EAP a ser criada
            
        Returns:
            EAPEntity: A EAP criada com ID
        """
        pass
    
    @abstractmethod
    def find_by_id(self, eap_id: int) -> Optional[EAPEntity]:
        """
        Busca uma EAP pelo ID
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            EAPEntity: A EAP encontrada ou None
        """
        pass
    
    @abstractmethod
    def find_by_project_id(self, project_id: int) -> Optional[EAPEntity]:
        """
        Busca a EAP de um projeto específico
        
        Args:
            project_id: ID do projeto
            
        Returns:
            EAPEntity: A EAP do projeto ou None
        """
        pass
    
    @abstractmethod
    def find_templates(self) -> List[EAPEntity]:
        """
        Busca todas as EAPs que são templates
        
        Returns:
            List[EAPEntity]: Lista de EAPs templates
        """
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[EAPEntity]:
        """
        Busca EAPs pelo nome (busca parcial)
        
        Args:
            name: Nome ou parte do nome da EAP
            
        Returns:
            List[EAPEntity]: Lista de EAPs encontradas
        """
        pass
    
    @abstractmethod
    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[EAPEntity]:
        """
        Busca todas as EAPs com paginação
        
        Args:
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[EAPEntity]: Lista de EAPs
        """
        pass
    
    @abstractmethod
    def update(self, eap: EAPEntity) -> EAPEntity:
        """
        Atualiza uma EAP
        
        Args:
            eap: Entidade EAP com dados atualizados
            
        Returns:
            EAPEntity: A EAP atualizada
        """
        pass
    
    @abstractmethod
    def delete(self, eap_id: int) -> None:
        """
        Exclui uma EAP
        
        Args:
            eap_id: ID da EAP a ser excluída
        """
        pass
    
    @abstractmethod
    def delete_by_project_id(self, project_id: int) -> None:
        """
        Exclui todas as EAPs de um projeto
        
        Args:
            project_id: ID do projeto
        """
        pass
    
    @abstractmethod
    def count_by_project_id(self, project_id: int) -> int:
        """
        Conta quantas EAPs um projeto possui
        
        Args:
            project_id: ID do projeto
            
        Returns:
            int: Número de EAPs do projeto
        """
        pass
