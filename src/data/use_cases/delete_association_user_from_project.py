from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.use_cases.i_delete_association_user_from_project import IDeleteAssociationUserFromProject

class DeleteAssociationUserFromProject(IDeleteAssociationUserFromProject):

    def __init__(self, user_project_repository:IUserProjectRepository) -> None:
        self.__user_project_repository = user_project_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__user_project_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e