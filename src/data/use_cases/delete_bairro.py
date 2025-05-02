from src.domain.use_cases.i_delete_bairro import IDeleteBairro
from src.data.interface.i_bairro_repository import IBairroRepository

class DeleteBairro(IDeleteBairro):

    def __init__(self, bairro_repository:IBairroRepository) -> None:
        self.__bairro_repository = bairro_repository
    
    def delete(self, name:str) -> None:
        try:
            self.__bairro_repository.delete(
                name=name
            )
        except Exception as e:
            raise e from e