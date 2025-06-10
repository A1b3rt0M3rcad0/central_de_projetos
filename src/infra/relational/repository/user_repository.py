from src.data.interface.i_user_repository import IUserRepository
from src.domain.value_objects.cpf import CPF
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.interface.i_salt import ISalt
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.domain.entities.user import UserEntity
from src.infra.relational.models.user import User
from typing import Optional, Dict

# Errors
from src.errors.repository.not_exists_error.user_not_exists import UserNotExists
from src.errors.repository.already_exists_error.user_already_exists import UserAlreadyExists
from src.errors.repository.error_on_insert.error_on_insert_user import ErrorOnInsertUser
from src.errors.repository.error_on_find.error_on_find_user import ErrorOnFindUser
from src.errors.repository.error_on_update.error_on_update_user import ErrorOnUpdateUser
from src.errors.repository.error_on_delete.error_on_delete_user import ErrorOnDeleteUser
from src.errors.repository.has_related_children.user_has_related_children import UserHasRelatedChildren
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class UserRepository(IUserRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, cpf:CPF, password:HashedPassword, salt:ISalt, role:Role, email:Email, name:Optional[str]=None) -> None:

        cpf_entry = cpf.value
        password_entry = password.hashed_password
        salt_entry = salt.salt
        role_entry = role.value
        email_entry = email.email
        name_entry = name

        with self.__db_connection_handler as db:
            try:
                db.session.add(
                    User(cpf=cpf_entry, password=password_entry, salt=salt_entry, role=role_entry, email=email_entry, name=name_entry)
                )
                db.session.commit()
            except IntegrityError as e:
                raise UserAlreadyExists(message=f"Usuário com CPF ou e-mail já existente: {e}") from e

            except Exception as e:
                raise ErrorOnInsertUser(f"Erro ao inserir usuário no banco de dados: {str(e)}") from e


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
                        created_at=result.created_at,
                        name = result.name
                    )
                raise UserNotExists(message=f'User with cpf "{cpf.value}" not founded')
            except UserNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindUser(f"Erro ao buscar usuário com CPF {cpf.value}: {e}") from e

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
                raise UserNotExists(message=f'User with email "{email.email}" not existes')
            except UserNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindUser(f"Erro ao buscar usuário com email {email.email}: {str(e)}") from e

    def update(self, cpf:CPF, update_params:Dict) -> None:
        cpf_entry = cpf.value
        with self.__db_connection_handler as db:
            try:
                user = db.session.query(User).where(User.cpf == cpf_entry).first()
                if not user:
                    raise UserNotExists(
                        message=f'user with cpf={cpf.value} not exists'
                    )
                db.session.query(User).where(User.cpf == cpf_entry).update(update_params)
                db.session.commit()
            except UserNotExists as e:
                raise e from e
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ErrorOnUpdateUser(f"Erro ao atualizar usuário com CPF {cpf.value}: {e}") from e

    
    def delete(self, cpf:CPF) -> None:
        cpf_entry = cpf.value
        with self.__db_connection_handler as db:
            try:
                user = db.session.query(User).filter(User.cpf == cpf_entry).first()
                if not user:
                    raise UserNotExists(
                        message=f'User with cpf={cpf.value} not exists'
                    )
                if user:
                    db.session.delete(user)
                    db.session.commit()
            except UserNotExists as e:
                raise e from e
            except IntegrityError as e:
                raise UserHasRelatedChildren(
                    message=f'Error on delete user cpf={cpf.value} because has related children'
                ) from e
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ErrorOnDeleteUser(f"Erro ao deletar usuário com CPF {cpf.value}: {e}") from e