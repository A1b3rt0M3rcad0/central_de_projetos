from src.domain.use_cases.i_count_bairros import ICountBairros
from src.data.interface.i_bairro_repository import IBairroRepository
from typing import Dict

class CountBairros(ICountBairros):

    def __init__(self, bairro_repository:IBairroRepository) -> None:
        self.__bairro_repository = bairro_repository
    
    def count(self) -> Dict[str, int]:
        try:
            return self.__bairro_repository.count_bairros()
        except Exception as e:
            raise e from e