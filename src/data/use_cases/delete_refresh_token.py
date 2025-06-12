from src.data.interface.i_refresh_token_repository import IRefreshTokenRepository
from src.domain.use_cases.i_delete_refresh_token import IDeleteRefreshToken
from src.domain.value_objects.cpf import CPF

class DeleteRefreshToken(IDeleteRefreshToken):

    def __init__(self, refresh_token_repository:IRefreshTokenRepository) -> None:
        self.__refresh_token_repository = refresh_token_repository

    def  delete(self, cpf:CPF) -> None:
        try:
            self.__refresh_token_repository.delete(cpf)
        except Exception as e:
            raise e from e