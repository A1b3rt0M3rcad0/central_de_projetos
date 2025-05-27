from src.data.interface.i_status_repository import IStatusRepository
from src.domain.use_cases.i_update_status_description import IUpdateStatusDescription
from src.errors.use_cases.status_description_error import StatusDescriptionError
from src.errors.repository.already_exists_error.status_already_exists import StatusAlreadyExists

class UpdateStatusDescription(IUpdateStatusDescription):

    def __init__(self, status_repository:IStatusRepository):
        self.__status_repository=status_repository
    
    def update(self, status_id:int, description:str) -> None:
        try:
            self.__status_repository.update(
                status_id=status_id,
                new_description=description
            )
        except StatusAlreadyExists as e:
            raise StatusDescriptionError(f'Error on update status description:{e.message} -> {e}') from e
        except Exception as e:
            raise e from e