from src.data.interface.i_user_repository import IUserRepository
from src.domain.use_cases.i_find_all_user_by_role import IFindAllUserByRole
from src.domain.entities.user import UserEntity
from src.domain.value_objects.roles import Role
from typing import List

class FindAllUserByRole(IFindAllUserByRole):

    def __init__(self, user_project_repository:IUserRepository) -> None:
        self.__user_project_repository = user_project_repository
    
    def find(self, role:Role) -> List[UserEntity]:
        try:
            result = self.__user_project_repository.find_all_by_role(role=role)
            return result
        except Exception as e:
            raise e from e