from src.domain.use_cases.i_update_refresh_token_fiscal import IUpdateRefreshTokenFiscal
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.domain.value_objects.email import Email

class UpdateRefreshTokenFiscal(IUpdateRefreshTokenFiscal):

    def __init__(self, fiscal_repository: IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository

    def update(self, fiscal_email: Email, new_token: str) -> None:
        try:
            # Find the fiscal by email to get the fiscal_id
            fiscal = self.__fiscal_repository.find_by_email(fiscal_email)
            self.__fiscal_repository.insert_refresh_token(
                fiscal_id=fiscal.fiscal_id,
                refresh_token=new_token
            )
        except Exception as e:
            raise e from e 