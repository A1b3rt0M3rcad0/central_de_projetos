from src.domain.entities.user import UserEntity
from src.domain.use_cases.i_find_all_user import IFindAllUser
from src.data.interface.i_user_repository import IUserRepository
from typing import List

class FindAllUser(IFindAllUser):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def find(self) -> List[UserEntity]:
        try:
            result = self.__user_repository.find_all()
            return result
        except Exception as e:
            raise e from e