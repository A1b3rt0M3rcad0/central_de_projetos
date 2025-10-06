from abc import ABC, abstractmethod


class ICreateWorkProjectNotification(ABC):
    """Interface para criação de notificações de work project"""

    @abstractmethod
    def create_for_admins(
        self,
        work_project_id: int,
        project_id: int,
        fiscal_name: str,
        work_project_title: str
    ) -> None:
        """
        Cria notificações para todos os admins quando um work project é criado
        
        Args:
            work_project_id: ID do work project criado
            project_id: ID do projeto pai
            fiscal_name: Nome do fiscal que criou
            work_project_title: Título do work project
        """
        pass
