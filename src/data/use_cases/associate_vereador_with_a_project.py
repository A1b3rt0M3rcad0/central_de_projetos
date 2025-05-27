from src.domain.use_cases.i_associate_vereador_with_a_project import IAssociateVereadorWithAProject
from src.data.interface.i_user_repository import IUserRepository
from src.data.interface.i_project_repository import IProjectRepository
from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.value_objects.cpf import CPF
from src.errors.use_cases.invalid_role_error import InvalidRoleError
from src.errors.use_cases.user_not_found_error import UserNotFoundError
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError
from src.errors.repository.already_exists_error.user_project_already_exists import UserProjectAlreadyExists
from src.errors.use_cases.invalid_association_error import InvalidAssociationError

class AssociateVereadorWithAProject(IAssociateVereadorWithAProject):

    def __init__(
            self, 
            user_project_repository:IUserProjectRepository,
            user_repository:IUserRepository,
            project_repository:IProjectRepository,
            ) -> None:
        self.__user_project_repository =  user_project_repository
        self.__user_repository = user_repository
        self.__project_repository = project_repository

    def associate(self, cpf_user:CPF, project_id:int):
        self.__valid_user_and_role(cpf_user=cpf_user)
        self.__valid_project(project_id=project_id)
        try:
            self.__user_project_repository.insert(
                cpf_user=cpf_user,
                project_id=project_id
            )
        except UserProjectAlreadyExists as e:
            raise InvalidAssociationError(
                f'This association already exists: {e.message}: {e}'
            ) from e
        except Exception as e:
            raise e from e
    
    def __valid_user_and_role(self, cpf_user:CPF) -> None:
        try:
            user = self.__user_repository.find(
                cpf_user
            )
            if user.role.value != 'VEREADOR':
                raise InvalidRoleError(
                    message=f'The role : {user.role.value} not is valid to associate'
                )
        except InvalidRoleError as e:
            raise e from e
        except AttributeError as e:
            raise UserNotFoundError(f'The user with cpf: {cpf_user} not founded') from e
        except Exception as e:
            raise e from e
    
    def __valid_project(self, project_id:int) -> None:
        try:
            self.__project_repository.find(
                project_id=project_id
            )
        except AttributeError as e:
            raise ProjectNotFoundError(f'Project with id {project_id} not founded') from e