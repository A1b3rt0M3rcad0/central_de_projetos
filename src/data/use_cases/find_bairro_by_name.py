from src.domain.use_cases.i_find_bairro_by_name import IFindBairroByName
from src.data.interface.i_bairro_repository import IBairroRepository
from src.domain.entities.bairro import BairroEntity

class FindBairroByName(IFindBairroByName):

    def __init__(self, bairro_repository:IBairroRepository) -> None:
        self.__bairro_repository = bairro_repository
    
    def find(self, name:str) -> BairroEntity:
        try:
            result = self.__bairro_repository.find_by_name(
                name=name
            )
            return result
        except Exception as e:
            raise e from e