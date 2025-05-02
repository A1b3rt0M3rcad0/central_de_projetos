from src.domain.use_cases.i_update_bairro_name import IUpdateBairroName
from src.data.interface.i_bairro_repository import IBairroRepository

class UpdateBairroName(IUpdateBairroName):

    def __init__(self, bairro_repository:IBairroRepository) -> None:
        self.__bairro_repository = bairro_repository
    
    def update(self, name:str, new_name:str) -> None:
        try:
            self.__bairro_repository.update(
                name=name,
                new_name=new_name
            )
        except Exception as e:
            raise e from e