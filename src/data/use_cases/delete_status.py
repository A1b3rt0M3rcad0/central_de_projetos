from src.data.interface.i_status_repository import IStatusRepository
from src.domain.use_cases.i_delete_status import IDeleteStatus

class DeleteStatus(IDeleteStatus):

    def __init__(self, status_repository:IStatusRepository) -> None:
        self.__status_repository = status_repository
    
    def delete(self, status_id:int):
        try:
            self.__status_repository.delete(
                status_id=status_id
            )
        except Exception as e:
            raise e from e