from src.domain.use_cases.i_find_all_projects_from_bairro import IFindAllProjectsFromBairro
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository
from src.domain.entities.project_bairro import ProjectBairroEntity
from typing import List

class FindAllProjectsFromBairro(IFindAllProjectsFromBairro):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def find(self, bairro_id:int) -> List[ProjectBairroEntity]:
        try:
            results = self.__project_bairro_repository.find_all_from_bairro(
                bairro_id=bairro_id
            )
            return results
        except Exception as e:
            raise e from e