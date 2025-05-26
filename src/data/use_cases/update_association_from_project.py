from src.data.interface.i_user_repository import IUserRepository
from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.use_cases.i_update_association_from_project import IUpdateAssociationFromProject
from src.domain.value_objects.cpf import CPF
from src.errors.use_cases.user_not_found_error import UserNotFoundError
from src.errors.use_cases.invalid_role_error import InvalidRoleError
from src.errors.use_cases.association_not_found_error import AssociationNotFoundError
from src.errors.repository.already_exists_error.user_project_not_exists import UserProjectNotExists


class UpdateAssociationFromProject(IUpdateAssociationFromProject):

    def __init__(self, user_project_repository:IUserProjectRepository, user_repository:IUserRepository) -> None:
        self.__user_project_repository = user_project_repository
        self.__user_repository = user_repository
    
    def update(self, cpf:CPF, project_id:int, new_cpf:CPF) -> None:
        try:
            user = self.__user_repository.find(cpf=new_cpf)

            if user.role != 'VEREADOR':
                raise InvalidRoleError(f'The roles not is "VEREADOR" to associate a project: {user.role}')
        
            self.__user_project_repository.find(
                cpf_user=cpf,
                project_id=project_id
            )
            update_params = {'cpf': new_cpf.value}
            self.__user_project_repository.update(
                cpf_user=cpf,
                project_id=project_id,
                update_params=update_params
            )
        except RuntimeError as e:
            raise UserNotFoundError(f'Cpf: {new_cpf} not founded from user: {e}') from e
        except UserProjectNotExists as e:
            raise AssociationNotFoundError(f'Association not founded: {e.message}') from e
        except Exception as e:
            raise e from e
