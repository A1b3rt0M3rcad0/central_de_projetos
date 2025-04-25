from datetime import datetime
from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_update_project_expected_completion_date_entry import IUpdateProjectExpectedCompletionDate

class UpdateProjectExpectedCompletionDate(IUpdateProjectExpectedCompletionDate):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def update(self, project_id:int, expected_completion_date:datetime) -> None:
        try:
            update_params = {'expected_completion_date':expected_completion_date}
            self.__project_repository.update(
                project_id=project_id,
                update_params=update_params
            )
        except Exception as e:
            raise e from e
