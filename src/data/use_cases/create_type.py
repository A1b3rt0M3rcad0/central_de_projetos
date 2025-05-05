from src.domain.use_cases.i_create_type import ICreateType
from src.data.interface.i_types_repository import ITypesRepository

class CreateType(ICreateType):

    def __init__(self, types_repository:ITypesRepository) -> None:
        self.__types_repository = types_repository
    
    def create(self, name:str) -> None:
        try:
            self.__types_repository.insert(
                name=name
            )
        except Exception as e:
            raise e from e