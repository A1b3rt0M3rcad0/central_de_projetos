from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_update_project_andamento import IUpdateProjectAndamento


class UpdateProjectAndamento(IUpdateProjectAndamento):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def update(self, project_id:int, andamento_do_projeto:str) -> None:
        try:
            update_params = {"andamento_do_projeto": andamento_do_projeto}
            self.__project_repository.update(
                project_id=project_id,
                update_params=update_params
            )
        except Exception as e:
            raise e from e