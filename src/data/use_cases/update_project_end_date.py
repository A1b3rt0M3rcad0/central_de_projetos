from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_update_project_end_date import IUpdateProjectEndDate
from src.errors.use_cases.invalid_end_date_error import InvalidEndDateError
from datetime import datetime

class UpdateProjectEndDate(IUpdateProjectEndDate):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository=project_repository
    
    def update(self, project_id:int, end_date:datetime):
        try:
            project = self.__project_repository.find(
                project_id=project_id
            )
            project_start_date = project.start_date
            if project_start_date is not None:
                if project_start_date > end_date:
                    raise InvalidEndDateError(message=f'the end date is less than the initial date: initial:{project_start_date}, end:{end_date}')
            self.__project_repository.update(
                project_id=project_id,
                end_date=end_date
            )
        except Exception as e:
            raise e from e