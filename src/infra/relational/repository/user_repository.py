from src.data.interface.i_user_repository import IUserRepository
from src.domain.value_objects.cpf import CPF
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.interface.i_salt import ISalt
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.relational.models.user import User

class UserRepository(IUserRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, cpf:CPF, password:HashedPassword, salt:ISalt, role:Role, email:Email) -> None:

        cpf_entry = cpf.value
        password_entry = password.hashed_password
        salt_entry = salt.salt
        role_entry = role.value
        email_entry = email.email

        with self.__db_connection_handler as db:
            try:
                db.session.add(
                    User(cpf=cpf_entry, password=password_entry, salt=salt_entry, role=role_entry, email=email_entry)
                )
                db.session.commit()
            except Exception as e:
                raise e

    def find(self, cpf):
        return None

    def update(self, cpf, update_params):
        return None
    
    def delete(self, cpf):
        return None