from src.domain.use_cases.i_get_project_verba_by_bairro import IGetProjectVerbaByBairro
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository
from src.domain.entities.project_bairro_verba_summary import ProjectBairroVerbaSummary

class GetProjectVerbaByBairro(IGetProjectVerbaByBairro):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def get(self) -> ProjectBairroVerbaSummary:
        try:
            result = self.__project_bairro_repository.get_project_verba_by_bairro()
            return result
        except Exception as e :
            raise e from e