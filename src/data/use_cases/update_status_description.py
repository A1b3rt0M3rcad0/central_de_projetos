from src.data.interface.i_status_repository import IStatusRepository
from src.domain.use_cases.i_update_status_description import IUpdateStatusDescription
from src.errors.use_cases.status_description_error import StatusDescriptionError
from src.errors.repository.status_description_already_exists import StatusDescriptionAlreadyExists

class UpdateStatusDescription(IUpdateStatusDescription):

    def __init__(self, status_repository:IStatusRepository):
        self.__status_repository=status_repository
    
    def update(self, description:str) -> None:
        try:
            self.__status_repository.update(
                description=description
            )
        except StatusDescriptionAlreadyExists as e:
            raise StatusDescriptionError(f'Error on update status description:{e.message} -> {e}') from e
        except Exception as e:
            raise e from e