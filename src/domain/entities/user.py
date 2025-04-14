from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role
from datetime import datetime

class UserEntity:

    def __init__(self, cpf:CPF, password:bytes, salt:bytes, role:Role, email:Email, created_at:datetime) -> None:
        self.cpf = cpf
        self.password = password
        self.salt = salt
        self.role = role
        self.email = email
        self.created_at = created_at