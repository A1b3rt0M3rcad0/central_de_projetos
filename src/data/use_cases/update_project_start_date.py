from datetime import datetime
from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_update_project_start_date import IUpdateProjectStartDate

class UpdateProjectStartDate(IUpdateProjectStartDate):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def update(self, project_id:datetime, start_date:datetime) -> None:
        try:
            update_params = {'start_date': start_date}
            self.__project_repository.update(
                project_id=project_id,
                update_params=update_params
            )
        except Exception as e:
            raise e from e