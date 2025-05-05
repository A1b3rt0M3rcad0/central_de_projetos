from src.domain.use_cases.i_delete_type import IDeleteType
from src.data.interface.i_types_repository import ITypesRepository

class DeleteType(IDeleteType):

    def __init__(self, types_repository:ITypesRepository) -> None:
        self.__types_repository = types_repository
    
    def delete(self, name:str) -> None:
        try:
            self.__types_repository.delete(
                name=name
            )
        except Exception as e:
            raise e from e