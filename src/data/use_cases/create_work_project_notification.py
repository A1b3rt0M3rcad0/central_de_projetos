from src.domain.use_cases.i_create_work_project_notification import ICreateWorkProjectNotification
from src.domain.use_cases.i_create_notification import ICreateNotification
from src.domain.entities.notification import NotificationType
from src.data.interface.i_user_repository import IUserRepository
from src.data.interface.i_project_repository import IProjectRepository
from src.domain.value_objects.roles import Role


class CreateWorkProjectNotification(ICreateWorkProjectNotification):
    """Implementação do caso de uso para criação de notificações de work project"""

    def __init__(
        self, 
        create_notification_case: ICreateNotification,
        user_repository: IUserRepository,
        project_repository: IProjectRepository
    ) -> None:
        self.__create_notification_case = create_notification_case
        self.__user_repository = user_repository
        self.__project_repository = project_repository

    def create_for_admins(
        self,
        work_project_id: int,
        project_id: int,
        fiscal_name: str,
        work_project_title: str
    ) -> None:
        """Cria notificações para todos os admins quando um work project é criado"""
        try:
            # Buscar o nome do projeto
            project = self.__project_repository.find(project_id)
            project_name = project.name if project else f"Projeto #{project_id}"
            
            # Buscar todos os usuários com role ADMIN
            admin_users = self.__user_repository.find_all_by_role(Role("ADMIN"))
            
            # Criar notificação para cada admin
            for admin in admin_users:
                self.__create_notification_case.create(
                    recipient_cpf=admin.cpf.value,
                    notification_type=NotificationType.WORK_PROJECT_CREATED,
                    title="Nova Fiscalização Criada",
                    message=f"O fiscal {fiscal_name} realizou uma nova fiscalização: '{work_project_title}' no projeto '{project_name}'",
                    related_entity_id=work_project_id,
                    related_entity_type="work_project"
                )
                
        except Exception as e:
            raise e from e
