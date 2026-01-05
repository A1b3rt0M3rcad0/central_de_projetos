from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.eap import EAPEntity


class IFindEAP(ABC):
    """Interface para o caso de uso de busca de EAP"""
    
    @abstractmethod
    def find_by_id(self, eap_id: int) -> Optional[EAPEntity]:
        """
        Busca uma EAP pelo ID
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            EAPEntity: A EAP encontrada ou None se não existir
        """
        pass
    
    @abstractmethod
    def find_by_project_id(self, project_id: int) -> Optional[EAPEntity]:
        """
        Busca a EAP de um projeto específico
        
        Args:
            project_id: ID do projeto
            
        Returns:
            EAPEntity: A EAP do projeto ou None se não existir
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
