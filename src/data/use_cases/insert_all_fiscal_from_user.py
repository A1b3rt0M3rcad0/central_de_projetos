from src.domain.use_cases.i_insert_all_fiscal_from_user import IInsertAllFiscalFromFiscalUseCase
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.domain.value_objects.email import Email
from src.security.value_objects.hashed_password import HashedPassword

class InsertAllFiscalFromFiscalUseCase(IInsertAllFiscalFromFiscalUseCase):
    def __init__(self, fiscal_repository: IFiscalRepository):
        self.fiscal_repository = fiscal_repository

    def execute(self, name: str, email: Email, password: HashedPassword, phone: str) -> None:
        self.fiscal_repository.insert_all_from_fiscal(name, email, password, phone)
