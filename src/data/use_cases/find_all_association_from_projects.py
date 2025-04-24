from src.domain.entities.user_project import UserProjectEntity
from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.use_cases.i_find_all_association_from_projects import IFindAllAssociationfromProjects
from typing import List, Optional

class FindAllAssociationFromProject(IFindAllAssociationfromProjects):

    def __init__(self, user_project_repository:IUserProjectRepository) -> None:
        self.__user_project_repository = user_project_repository
    
    def find(self) -> List[Optional[UserProjectEntity]]:
        try:
            projects = self.__user_project_repository.find_all()
            return projects
        except Exception as e:
            raise e from e