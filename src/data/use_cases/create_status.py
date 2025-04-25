from src.domain.use_cases.i_create_status import ICreateStatus
from src.data.interface.i_status_repository import IStatusRepository
from src.errors.use_cases.create_status_error import CreateStatusError

class CreateStatus(ICreateStatus):

    def __init__(self, status_repository:IStatusRepository) -> None:
        self.__status_repository = status_repository
        
    def create(self, description:str) -> None:
        try:
            self.__status_repository.insert(
                description=description
            )
        except Exception as e:
            raise CreateStatusError(
                message=f'Error on create status: {e}'
            ) from e