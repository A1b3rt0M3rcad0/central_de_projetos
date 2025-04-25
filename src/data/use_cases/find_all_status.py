from src.domain.entities.status import StatusEntity
from typing import List
from src.domain.use_cases.i_find_status import IFindStatus
from src.data.interface.i_status_repository import IStatusRepository

class FindAllStatus(IFindStatus):

    def __init__(self, status_repository:IStatusRepository) -> None:
        self.__status_repository = status_repository
    
    def find(self, status_id:id) -> List[StatusEntity]:
        try:
            result = self.__status_repository.find(
                status_id=status_id
            )
            return result
        except Exception as e:
            raise e from e