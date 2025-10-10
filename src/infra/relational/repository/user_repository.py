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
from sqlalchemy import or_

# Import models to ensure SQLAlchemy can resolve relationships
# These imports are necessary for SQLAlchemy to properly configure relationships
# pylint: disable=unused-import
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.models.project import Project
from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.models.status import Status
from src.infra.relational.models.types import Types
from src.infra.relational.models.refresh_token import RefreshToken
from src.infra.relational.models.work_project import WorkProject
from src.infra.relational.models.eap import EAP, EAPItem
from src.infra.relational.models.notification import Notification

# Errors
from src.errors.repository.not_exists_error.user_not_exists import UserNotExists
from src.errors.repository.already_exists_error.user_already_exists import UserAlreadyExists
from src.errors.repository.error_on_insert.error_on_insert_user import ErrorOnInsertUser
from src.errors.repository.error_on_find.error_on_find_user import ErrorOnFindUser
from src.errors.repository.error_on_update.error_on_update_user import ErrorOnUpdateUser
from src.errors.repository.error_on_delete.error_on_delete_user import ErrorOnDeleteUser
from src.errors.repository.has_related_children.user_has_related_children import UserHasRelatedChildren
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from typing import List

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
                        role=Role(str(result.role)),
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
                        role=Role(str(result.role)),
                        email=Email(result.email),
                        created_at=result.created_at,
                        name=result.name
                    )
                raise UserNotExists(message=f'User with email "{email.email}" not existes')
            except UserNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindUser(f"Erro ao buscar usuário com email {email.email}: {str(e)}") from e
    
    def find_all(self) -> List[UserEntity]:
        try:
            with self.__db_connection_handler as db:
                result = db.session.query(User).all()
                if not any(result):
                    raise UserNotExists(message='Users not exists')
                return [
                    UserEntity(
                        cpf=CPF(user.cpf),
                        password=user.password, # bytes
                        salt=user.salt, # bytes
                        role=Role(user.role),
                        email=Email(user.email),
                        created_at=user.created_at,
                        name=user.name
                    )
                    for user in result
                ]
        except UserNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindUser(message="Error on find users") from e
    
    def find_all_by_role(self, role:Role) -> List[UserEntity]:
        try:
            with self.__db_connection_handler as db:
                result = db.session.query(User).where(User.role == role.value).all()
                if not any(result):
                    raise UserNotExists(message='Users not exists')
                return [
                    UserEntity(
                        cpf=CPF(user.cpf),
                        password=user.password, # bytes
                        salt=user.salt, # bytes
                        role=Role(str(user.role)),
                        email=Email(user.email),
                        created_at=user.created_at,
                        name=user.name
                    )
                    for user in result
                ]
        except UserNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindUser(message="Error on find users") from e
    
    def get_count_projects_by_user(self) -> Dict[str, int]:
        try:
            with self.__db_connection_handler as db:
                users:List[User] = db.session.query(User).where(User.role == 'VEREADOR').all()
                return {
                    user.name: len(user.user_projects)
                    for user in users
                }
        except Exception as e:
            raise ErrorOnFindUser(message="Error on get count projects by users") from e

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
            except (IntegrityError, AssertionError) as e:
                raise UserHasRelatedChildren(
                    message=f'Error on delete user cpf={cpf.value} because has related children'
                ) from e
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ErrorOnDeleteUser(f"Erro ao deletar usuário com CPF {cpf.value}: {e}") from e

    def find_all_with_pagination(self, page_size: int, page: int) -> List[UserEntity]:
        try:
            with self.__db_connection_handler as db:
                offset = (page - 1) * page_size
                users = db.session.query(User).offset(offset).limit(page_size).all()
                users_entities = [
                    UserEntity(
                        cpf=CPF(user.cpf),
                        password=user.password,
                        salt=user.salt,
                        role=Role(user.role),
                        email=Email(user.email),
                        created_at=user.created_at,
                        name=user.name,
                    )
                    for user in users
                ]
                return users_entities
        except Exception as e:
            raise ErrorOnFindUser(
                message=f'Error on find all users with pagination: {str(e)}'
            ) from e

    def count_all(self) -> int:
        try:
            with self.__db_connection_handler as db:
                count = db.session.query(User).count()
                return count
        except Exception as e:
            raise ErrorOnFindUser(
                message=f'Error on count all users: {str(e)}'
            ) from e

    def find_all_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[UserEntity]:
        try:
            with self.__db_connection_handler as db:
                offset = (page - 1) * page_size
                query = db.session.query(User)
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(
                        or_(
                            User.cpf.ilike(search_filter),
                            User.name.ilike(search_filter),
                            User.email.ilike(search_filter),
                            User.role.ilike(search_filter)
                        )
                    )
                
                users = query.offset(offset).limit(page_size).all()
                users_entities = [
                    UserEntity(
                        cpf=CPF(user.cpf),
                        password=user.password,
                        salt=user.salt,
                        role=Role(user.role),
                        email=Email(user.email),
                        created_at=user.created_at,
                        name=user.name,
                    )
                    for user in users
                ]
                return users_entities
        except Exception as e:
            raise ErrorOnFindUser(
                message=f'Error on find all users with pagination and filter: {str(e)}'
            ) from e

    def count_all_with_filter(self, search_term: str = None) -> int:
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(User)
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(
                        or_(
                            User.cpf.ilike(search_filter),
                            User.name.ilike(search_filter),
                            User.email.ilike(search_filter),
                            User.role.ilike(search_filter)
                        )
                    )
                
                count = query.count()
                return count
        except Exception as e:
            raise ErrorOnFindUser(
                message=f'Error on count all users with filter: {str(e)}'
            ) from e