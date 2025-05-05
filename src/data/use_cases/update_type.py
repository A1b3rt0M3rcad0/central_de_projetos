from src.data.interface.i_types_repository import ITypesRepository
from src.domain.use_cases.i_update_type import IUpdateType

class UpdateType(IUpdateType):

    def __init__(self, types_repository:ITypesRepository) -> None:
        self.__types_repository = types_repository
    
    def update(self, name:str, new_name:str) -> None:
        try:
            self.__types_repository.update(
                name=name,
                new_name=new_name
            )
        except Exception as e:
            raise e from e