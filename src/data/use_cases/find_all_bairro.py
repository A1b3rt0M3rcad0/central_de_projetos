from src.domain.use_cases.i_find_all_bairro import IFindAllBairro
from src.domain.entities.bairro import BairroEntity
from src.data.interface.i_bairro_repository import IBairroRepository
from typing import List

class FindAllBairro(IFindAllBairro):

    def __init__(self, bairro_repository:IBairroRepository) -> None:
        self.__bairro_repository = bairro_repository

    def find(self) -> List[BairroEntity]:
        try:
            result = self.__bairro_repository.find_all()
            return result
        except Exception as e:
            raise e from e
        