from src.domain.use_cases.i_update_fiscal_status import IUpdateFiscalStatus
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.errors.use_cases.fiscal_not_found_error import FiscalNotFoundError
from src.errors.use_cases.invalid_parameter_error import InvalidParameterError
from src.errors.repository.not_exists_error.fiscal_not_exists import FiscalNotExists

class UpdateFiscalStatus(IUpdateFiscalStatus):

    def __init__(self, fiscal_repository: IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository

    def update(self, fiscal_id: int, is_active: int) -> None:
        try:
            # Validar o valor de is_active
            if is_active not in [0, 1]:
                raise InvalidParameterError(
                    message=f'Invalid value for is_active: {is_active}. Must be 0 or 1.'
                )
            
            self.__fiscal_repository.update_status(
                fiscal_id=fiscal_id,
                is_active=is_active
            )
        except FiscalNotExists as e:
            raise FiscalNotFoundError(
                message=f'Fiscal with id {fiscal_id} not found'
            ) from e
        except InvalidParameterError as e:
            raise e
        except Exception as e:
            raise e from e

