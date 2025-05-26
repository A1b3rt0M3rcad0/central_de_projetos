from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.data.interface.i_history_project_repository import IHistoryProjectRepository
from src.errors.repository.not_exists_error.project_not_exists import ProjectNotExistsError
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError
from typing import Optional

class CreateHistoryProject(ICreateHistoryProject):

    def __init__(self, history_project_repository:IHistoryProjectRepository) -> None:
        self.__history_project_repository = history_project_repository
    
    def create(self, project_id:int, data_name:str, description:Optional[str] = None):
        try:
            self.__history_project_repository.insert(
                project_id=project_id,
                data_name=data_name,
                description=description
            )
        except ProjectNotExistsError as e:
            raise ProjectNotFoundError(
                message=f'Project not founded: {e}'
            ) from e