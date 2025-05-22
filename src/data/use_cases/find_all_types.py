from src.domain.use_cases.i_find_all_types import IFindAllTypes
from src.data.interface.i_types_repository import ITypesRepository
from src.domain.entities.types import TypesEntity
from typing import List

class FindAllTypes(IFindAllTypes):

    def __init__(self, types_repository:ITypesRepository) -> None:
        self.__types_repository = types_repository
    
    def find(self) -> List[TypesEntity]:
        try:
            result = self.__types_repository.find_all()
            return result
        except Exception as e:
            raise e from e