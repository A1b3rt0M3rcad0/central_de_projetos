from src.domain.use_cases.i_find_bairro_by_id import IFindBairroById
from src.domain.entities.bairro import BairroEntity
from src.data.interface.i_bairro_repository import IBairroRepository

class FindBairrobyId(IFindBairroById):

    def __init__(self, bairro_repository:IBairroRepository) -> None:
        self.__bairro_repository = bairro_repository
    
    def find(self, bairro_id:int) -> BairroEntity:
        try:
            result = self.__bairro_repository.find_by_id(
                bairro_id=bairro_id
            )
            return result
        except Exception as e:
            raise e from e
    
