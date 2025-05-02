from src.domain.use_cases.i_create_bairro import ICreateBairro
from src.data.interface.i_bairro_repository import IBairroRepository

class CreateBairro(ICreateBairro):
    
    def __init__(self, bairro_repository:IBairroRepository) -> None:
        self.__bairo_repository = bairro_repository
    
    def create(self, name:str) -> None:
        try:
            self.__bairo_repository.insert(
                name=name
            )
        except Exception as e:
            raise e from e