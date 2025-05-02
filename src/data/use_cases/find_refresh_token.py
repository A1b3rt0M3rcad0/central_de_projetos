from src.domain.use_cases.i_find_refresh_token import IFindRefreshToken
from src.data.interface.i_refresh_token_repository import IRefreshTokenRepository
from src.domain.value_objects.cpf import CPF
from src.domain.entities.refresh_token import RefreshTokenEntity

class FindRefreshToken(IFindRefreshToken):

    def __init__(self, refresh_token_repository:IRefreshTokenRepository) -> None:
        self.__refresh_token_repository = refresh_token_repository
    
    def find(self, user_cpf:CPF) -> RefreshTokenEntity:
        try:
            result = self.__refresh_token_repository.find(user_cpf=user_cpf)
            return result
        except Exception as e:
            raise e from e