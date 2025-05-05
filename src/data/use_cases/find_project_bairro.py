from src.domain.use_cases.i_find_project_bairro import IFindProjectBairro
from src.domain.entities.project_bairro import ProjectBairroEntity
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository

class FindProjectBairro(IFindProjectBairro):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def find(self, project_id:int, bairro_id:int) -> ProjectBairroEntity:
        try:
            result = self.__project_bairro_repository.find(
                project_id=project_id,
                bairro_id=bairro_id
            )
            return result
        except Exception as e:
            raise e from e