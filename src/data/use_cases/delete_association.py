from src.domain.use_cases.i_delete_association import IDeleteAssociation
from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.value_objects.cpf import CPF

class DeleteAssociation(IDeleteAssociation):

    def __init__(self, user_project_repository:IUserProjectRepository) -> None:
        self.__user_project_repository = user_project_repository
    
    def delete(self, cpf:CPF, project_id:int) -> None:
        try:
            self.__user_project_repository.delete(
                cpf_user=cpf,
                project_id=project_id
            )
        except Exception as e:
            raise e