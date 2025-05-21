from src.domain.entities.status import StatusEntity
from typing import List
from src.domain.use_cases.i_find_all_status import IFindAllStatus
from src.data.interface.i_status_repository import IStatusRepository

class FindAllStatus(IFindAllStatus):

    def __init__(self, status_repository:IStatusRepository) -> None:
        self.__status_repository = status_repository
    
    def find(self) -> List[StatusEntity]:
        try:
            result = self.__status_repository.find_all()
            return result
        except Exception as e:
            raise e from e