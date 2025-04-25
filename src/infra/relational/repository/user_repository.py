from src.data.interface.i_user_repository import IUserRepository
from src.domain.value_objects.cpf import CPF
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.interface.i_salt import ISalt
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.domain.entities.user import UserEntity
from src.infra.relational.models.user import User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.errors.repository.cpf_or_email_already_exists import CPFOrEmailAlreadyExists
from typing import Optional, Dict

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
            except IntegrityError as e:
                db.session.rollback()
                raise CPFOrEmailAlreadyExists(message=f"Usuário com CPF ou e-mail já existente: {e}") from e

            except SQLAlchemyError as e:
                db.session.rollback()
                raise RuntimeError(f"Erro ao inserir usuário no banco de dados: {e}") from e


    def find(self, cpf:CPF) -> Optional[UserEntity]:
        cpf_entry = cpf.value

        with self.__db_connection_handler as db:
            try:
                result = db.session.query(User).where(User.cpf == cpf_entry).first()
                if result:
                    return UserEntity(
                        cpf=CPF(result.cpf),
                        password=result.password, # bytes
                        salt=result.salt, # bytes
                        role=Role(result.role),
                        email=Email(result.email),
                        created_at=result.created_at
                    )
                return None 
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar usuário com CPF {cpf.value}: {e}") from e

    def find_by_email(self, email:Email) -> Optional[UserEntity]:
        email_entry = email.email

        with self.__db_connection_handler as db:
            try:
                result = db.session.query(User).where(User.email == email_entry).first()
                if result:
                    return UserEntity(
                        cpf=CPF(result.cpf),
                        password=result.password, # bytes
                        salt=result.salt, # bytes
                        role=Role(result.role),
                        email=Email(result.email),
                        created_at=result.created_at
                    )
                return None 
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar usuário com email {email.email}: {e}") from e

    def update(self, cpf:CPF, update_params:Dict) -> None:
        cpf_entry = cpf.value
        with self.__db_connection_handler as db:
            try:
                db.session.query(User).where(User.cpf == cpf_entry).update(update_params)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                raise RuntimeError(f"Erro ao atualizar usuário com CPF {cpf.value}: {e}") from e

    
    def delete(self, cpf:CPF) -> None:
        cpf_entry = cpf.value
        with self.__db_connection_handler as db:
            try:
                user = db.session.query(User).filter(User.cpf == cpf_entry).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                raise RuntimeError(f"Erro ao deletar usuário com CPF {cpf.value}: {e}") from e