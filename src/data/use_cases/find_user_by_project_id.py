from src.domain.use_cases.i_find_user_by_project_id import IFindUserByProjectId
from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.entities.user import UserEntity

class FindUserByProjectId(IFindUserByProjectId):

    def __init__(self, user_project_repository:IUserProjectRepository) -> None:
        self.__user_project_repository = user_project_repository
    
    def find(self, project_id:int) -> UserEntity | None:
        try:
            result = self.__user_project_repository.find_user_by_project_id(project_id=project_id)
            return result
        except Exception as e:
            raise e from e