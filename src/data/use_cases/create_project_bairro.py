from src.domain.use_cases.i_create_project_bairro import ICreateProjectBairro
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository

class CreateProjectBairro(ICreateProjectBairro):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def create(self, project_id:int, bairro_id:int) -> None:
        try:
            self.__project_bairro_repository.insert(
                bairro_id=bairro_id,
                project_id=project_id
            )
        except Exception as e:
            raise e from e