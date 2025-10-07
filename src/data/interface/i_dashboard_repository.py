from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IDashboardRepository(ABC):
    """Interface do repositório de dashboard"""
    
    @abstractmethod
    def get_counts_summary(self, excluded_status: List[int] = None) -> Dict[str, int]:
        """Retorna contagens gerais (projetos, bairros, empresas, fiscais)"""
        pass
    
    @abstractmethod
    def get_projects_by_bairro(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por bairro"""
        pass
    
    @abstractmethod
    def get_budget_by_bairro(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna orçamento por bairro"""
        pass
    
    @abstractmethod
    def get_projects_by_fiscal(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por fiscal"""
        pass
    
    @abstractmethod
    def get_projects_by_empresa(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por empresa"""
        pass
    
    @abstractmethod
    def get_projects_by_user(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por usuário"""
        pass
    
    @abstractmethod
    def get_projects_by_bairro_and_type(self, excluded_status: List[int] = None) -> Dict[str, Any]:
        """Retorna contagem de projetos por bairro e tipo com lista de tipos"""
        pass
    
    @abstractmethod
    def get_all_types(self) -> List[Dict[str, Any]]:
        """Retorna lista de todos os tipos"""
        pass
    
    @abstractmethod
    def get_projects_by_bairro_and_status(self, excluded_status: List[int] = None) -> Dict[str, Any]:
        """Retorna contagem de projetos por bairro e status com lista de bairros"""
        pass
    
    @abstractmethod
    def get_all_bairros(self) -> List[Dict[str, Any]]:
        """Retorna lista de todos os bairros"""
        pass
    
    @abstractmethod
    def get_projects_by_type(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por tipo"""
        pass
    
    @abstractmethod
    def get_projects_by_status(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por status"""
        pass

