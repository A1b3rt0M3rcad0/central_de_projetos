from typing import List, Optional

from src.domain.entities.eap import EAPEntity
from src.domain.use_cases.i_find_eap import IFindEAP
from src.data.interface.i_eap_repository import IEAPRepository


class FindEAP(IFindEAP):
    """Caso de uso para busca de EAP"""
    
    def __init__(self, eap_repository: IEAPRepository):
        self.__eap_repository = eap_repository
    
    def find_by_id(self, eap_id: int) -> Optional[EAPEntity]:
        """
        Busca uma EAP pelo ID
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            EAPEntity: A EAP encontrada ou None se não existir
        """
        return self.__eap_repository.find_by_id(eap_id)
    
    def find_by_project_id(self, project_id: int) -> Optional[EAPEntity]:
        """
        Busca a EAP de um projeto específico
        
        Args:
            project_id: ID do projeto
            
        Returns:
            EAPEntity: A EAP do projeto ou None se não existir
        """
        return self.__eap_repository.find_by_project_id(project_id)
    
    def find_templates(self) -> List[EAPEntity]:
        """
        Busca todas as EAPs que são templates
        
        Returns:
            List[EAPEntity]: Lista de EAPs templates
        """
        return self.__eap_repository.find_templates()
    
    def find_by_name(self, name: str) -> List[EAPEntity]:
        """
        Busca EAPs pelo nome (busca parcial)
        
        Args:
            name: Nome ou parte do nome da EAP
            
        Returns:
            List[EAPEntity]: Lista de EAPs encontradas
        """
        return self.__eap_repository.find_by_name(name)
    
    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[EAPEntity]:
        """
        Busca todas as EAPs com paginação
        
        Args:
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[EAPEntity]: Lista de EAPs
        """
        return self.__eap_repository.find_all(limit, offset)
