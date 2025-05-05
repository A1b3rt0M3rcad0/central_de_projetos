from src.domain.entities.types import TypesEntity
from src.data.interface.i_types_repository import ITypesRepository
from src.domain.use_cases.i_find_type_by_exact_name import IFindTypeByExactName

class FindTypebyExactName(IFindTypeByExactName):

    def __init__(self, types_repository:ITypesRepository) -> None:
        self.__types_repository = types_repository
    
    def find(self, name:str) -> TypesEntity:
        try:
            result = self.__types_repository.find_by_name(
                name=name
            )
            return result
        except Exception as e:
            raise e from e