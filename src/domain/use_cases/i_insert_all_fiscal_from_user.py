from abc import ABC, abstractmethod
from src.domain.value_objects.email import Email
from src.security.value_objects.hashed_password import HashedPassword

class IInsertAllFiscalFromFiscalUseCase(ABC):
    @abstractmethod
    def execute(self, name: str, email: Email, password: HashedPassword, phone: str) -> None:
        pass
