from src.domain.value_objects.cpf import CPF
from src.data.interface.i_refresh_token_repository import IRefreshTokenRepository
from src.domain.use_cases.i_update_refresh_token import IUpdateRefreshToken

class UpdateRefreshToken(IUpdateRefreshToken):

    def __init__(self, refresh_token_repository:IRefreshTokenRepository) -> None:
        self.__refresh_token_repository = refresh_token_repository
    
    def update(self, user_cpf:CPF, new_token:str) -> None:
        try:
            self.__refresh_token_repository.update(
                user_cpf=user_cpf,
                new_token=new_token
            )
        except Exception as e:
            raise e from e