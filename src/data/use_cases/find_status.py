from src.domain.use_cases.i_find_status import IFindStatus
from src.data.interface.i_status_repository import IStatusRepository
from src.domain.entities.status import StatusEntity
from src.errors.use_cases.status_not_found_error import StatusNotFoundError

class FindStatus(IFindStatus):

    def __init__(self, status_repository:IStatusRepository) -> None:
        self.__status_repository = status_repository
    
    def find(self, status_id:int) -> StatusEntity:
        try:
            result = self.__status_repository.find(
                status_id=status_id
            )
            return result
        except AttributeError as e:
            raise StatusNotFoundError(
                message=f'Status with id {status_id} not founded: {e}'
            ) from e
        except Exception as e:
            raise e from e