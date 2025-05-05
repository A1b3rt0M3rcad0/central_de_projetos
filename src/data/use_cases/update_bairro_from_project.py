from src.data.interface.i_project_bairro_repository import IProjectBairroRepository
from src.domain.use_cases.i_update_bairro_from_project import IUpdateBairroFromProject

class UpdateBairroFromProject(IUpdateBairroFromProject):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def update(self, project_id:int, bairro_id:int, new_bairro_id:int) -> None:
        try:
            self.__project_bairro_repository.update_bairro(
                project_id=project_id,
                bairro_id=bairro_id,
                new_bairro_id=new_bairro_id
            )
        except Exception as e:
            raise e from e