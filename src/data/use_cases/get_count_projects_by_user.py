from src.domain.use_cases.i_get_count_projects_by_user import IGetCountProjectsByuser
from src.data.interface.i_user_repository import IUserRepository
from typing import Dict

class GetCountProjectsByUser(IGetCountProjectsByuser):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def get(self) -> Dict[str, int]:
        try:
            return self.__user_repository.get_count_projects_by_user()
        except Exception as e:
            raise e from e