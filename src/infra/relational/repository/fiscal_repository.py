from src.domain.entities.fiscal import FiscalEntity
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_fiscal_repository import IFiscalRepository

# Import models to ensure SQLAlchemy can resolve relationships
# These imports are necessary for SQLAlchemy to properly configure relationships
# pylint: disable=unused-import
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
from src.infra.relational.models.user import User
from src.infra.relational.models.work_project import WorkProject
from src.infra.relational.models.eap import EAP, EAPItem
from src.infra.relational.models.eap_item_dependency import EAPItemDependency

# Domain
from src.domain.value_objects.email import Email
from src.security.value_objects.hashed_password import HashedPassword

# Errors
from src.errors.repository.not_exists_error.fiscal_not_exists import FiscalNotExists
from src.errors.repository.already_exists_error.fiscal_already_exists import FiscalAlreadyExists
from src.errors.repository.error_on_insert.error_on_insert_fiscal import ErrorOnInsertFiscal
from src.errors.repository.error_on_insert.error_on_insert_refresh_token import ErrorOnInsertRefreshToken
from src.errors.repository.error_on_find.error_on_find_fiscal import ErrorOnFindFiscal
from src.errors.repository.error_on_update.error_on_update_fiscal import ErroronUpdateFiscal
from src.errors.repository.error_on_delete.error_on_delete_fiscal import ErrorOnDeleteFiscal
from src.errors.repository.has_related_children.fiscal_has_related_children import FiscalHasRelatedChildren
from sqlalchemy.exc import IntegrityError

from typing import List, Dict

class FiscalRepository(IFiscalRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(
                    Fiscal(name=name)
                )
                db.session.commit()
        except IntegrityError as e:
            raise FiscalAlreadyExists(message=f'Fiscal {name} already exists: {str(e)}') from e
        except Exception as e:
            raise ErrorOnInsertFiscal(message=f'Error on insert fiscal {name}: {str(e)}') from e
    
    def insert_all_from_fiscal(self, name:str, email:Email, password:HashedPassword, phone:str) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.add(
                    Fiscal(
                        name=name,
                        email=email.email,
                        password=password.hashed_password,
                        salt=password.salt,
                        phone=phone
                    )
                )
                db.session.commit()
            except Exception as e:
                raise ErrorOnInsertFiscal(message=f'Error on insert Fiscal: {name}: {str(e)}') from e
    
    def insert_refresh_token(self, fiscal_id:int, refresh_token:str) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(Fiscal).where(Fiscal.id == fiscal_id).update({'refresh_token':refresh_token})
                db.session.commit()
            except Exception as e:
                raise ErrorOnInsertRefreshToken(message=f'Error on insert refresh token: {str(e)}') from e

    def find_by_name(self, name:str) -> FiscalEntity:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).first()
                if fiscal is None:
                    raise FiscalNotExists(message=f'The fiscal with name {name} does not exists')
                return FiscalEntity(
                    fiscal_id=fiscal.id,
                    name=fiscal.name,
                    created_at=fiscal.created_at,
                    email=fiscal.email,
                    phone=fiscal.phone,
                    password=fiscal.password,
                    salt=fiscal.salt,
                    refresh_token=fiscal.refresh_token,
                    is_active=fiscal.is_active
                )
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindFiscal(message=f'Error on find fiscal by name {name}: {str(e)}') from e
     
    def find_by_id(self, fiscal_id:int) -> FiscalEntity:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(
                    Fiscal.id == fiscal_id
                ).first()
                if fiscal is None:
                    raise FiscalNotExists(message=f'The fiscal with id {fiscal_id} does not exists')
                return FiscalEntity(
                    fiscal_id=fiscal.id,
                    name=fiscal.name,
                    created_at=fiscal.created_at,
                    email=fiscal.email,
                    phone=fiscal.phone,
                    password=fiscal.password,
                    salt=fiscal.salt,
                    refresh_token=fiscal.refresh_token,
                    is_active=fiscal.is_active
                )
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindFiscal(message=f'Error on find fiscal by id {fiscal_id}: {str(e)}') from e
    
    def find_by_email(self, email:Email) -> FiscalEntity:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(
                    Fiscal.email == email.email
                ).first()
                if fiscal is None:
                    raise FiscalNotExists(message=f'The fiscal with email {email.email} does not exists')
                return FiscalEntity(
                    fiscal_id=fiscal.id,
                    name=fiscal.name,
                    phone=fiscal.phone,
                    email=fiscal.email,
                    password=fiscal.password,
                    salt=fiscal.salt,
                    refresh_token=fiscal.refresh_token,
                    created_at=fiscal.created_at,
                    is_active=fiscal.is_active
                )
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindFiscal(message=f'Error on find fiscal by email {email.email}: {str(e)}') from e
    
    def find_all(self) -> List[FiscalEntity]:
        try:
            with self.__db_connection_handler as db:
                fiscais:List[Fiscal] = db.session.query(Fiscal).all()
                if not any(fiscais):
                    raise FiscalNotExists(message='Not exists fiscal')
                result = [
                    FiscalEntity(
                        fiscal_id=fiscal.id,
                        name=fiscal.name,
                        email=Email(email=fiscal.email) if fiscal.email else None,
                        phone=fiscal.phone,
                        created_at=fiscal.created_at,
                        is_active=fiscal.is_active
                    )
                     for fiscal in fiscais
                ]
                return result
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindFiscal(message='Error on find all fiscal') from e
    
    def count_fiscals(self) -> Dict[str, int]:
        try:
            with self.__db_connection_handler as db:
                fiscals:List[Fiscal] = db.session.query(Fiscal).all()
                return {
                   'fiscals': len(fiscals)
                }
        except Exception as e:
            raise ErrorOnFindFiscal(message='Error on count all fiscal') from e

    def update(self, name:str, new_name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(Fiscal.name == name).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with name {name} does not exists')
                db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).update({'name':new_name})
                db.session.commit()
        except FiscalNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise FiscalAlreadyExists(message=f'Fiscal with name {new_name} already exists: {str(e)}') from e
        except Exception as e:
            raise ErroronUpdateFiscal(message=f'Error on update fiscal {name} -> {new_name}: {str(e)}') from e

    def update_email(self, name:str, email:Email) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(Fiscal.name == name).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with name {name} does not exists')
                
                # Atualizar o campo diretamente no objeto
                fiscal.email = email.email
                
                db.session.commit()
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErroronUpdateFiscal(message=f'Error on update email for fiscal {name}: {str(e)}') from e

    def update_password(self, name:str, password:HashedPassword) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(Fiscal.name == name).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with name {name} does not exists')
                
                # Atualizar os campos diretamente no objeto
                fiscal.password = password.hashed_password
                fiscal.salt = password.salt
                
                db.session.commit()
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErroronUpdateFiscal(message=f'Error on update password for fiscal {name}: {str(e)}') from e

    def update_phone(self, name:str, phone:str) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(Fiscal.name == name).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with name {name} does not exists')
                
                # Atualizar o campo diretamente no objeto
                fiscal.phone = phone
                
                db.session.commit()
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErroronUpdateFiscal(message=f'Error on update phone for fiscal {name}: {str(e)}') from e
    
    def delete(self, name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(Fiscal.name == name).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with name {name} does not exists')
                db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).delete()
                db.session.commit()
        except FiscalNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise FiscalHasRelatedChildren(f'Fiscal {name} not deleted because has a related children: {str(e)}') from e
        except Exception as e:
            raise ErrorOnDeleteFiscal(message=f'Error on delete fiscal {name}: {str(e)}') from e

    def find_all_with_pagination(self, page_size: int, page: int) -> List[FiscalEntity]:
        try:
            with self.__db_connection_handler as db:
                offset = (page - 1) * page_size
                fiscais = db.session.query(Fiscal).offset(offset).limit(page_size).all()
                fiscais_entities = [
                    FiscalEntity(
                        fiscal_id=fiscal.id,
                        name=fiscal.name,
                        email=Email(email=fiscal.email) if fiscal.email else None,
                        phone=fiscal.phone,
                        created_at=fiscal.created_at,
                        is_active=fiscal.is_active
                    )
                    for fiscal in fiscais
                ]
                return fiscais_entities
        except Exception as e:
            raise ErrorOnFindFiscal(
                message=f'Error on find all fiscais with pagination: {str(e)}'
            ) from e

    def count_all(self) -> int:
        try:
            with self.__db_connection_handler as db:
                count = db.session.query(Fiscal).count()
                return count
        except Exception as e:
            raise ErrorOnFindFiscal(
                message=f'Error on count all fiscais: {str(e)}'
            ) from e

    def find_all_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[FiscalEntity]:
        try:
            with self.__db_connection_handler as db:
                offset = (page - 1) * page_size
                query = db.session.query(Fiscal)
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(Fiscal.name.ilike(search_filter))
                
                fiscais = query.offset(offset).limit(page_size).all()
                fiscais_entities = [
                    FiscalEntity(
                        fiscal_id=fiscal.id,
                        name=fiscal.name,
                        created_at=fiscal.created_at,
                        password=fiscal.password,
                        salt=fiscal.salt,
                        email=Email(fiscal.email) if fiscal.email else None,
                        phone=fiscal.phone,
                        refresh_token=fiscal.refresh_token,
                        is_active=fiscal.is_active
                    )
                    for fiscal in fiscais
                ]
                return fiscais_entities
        except Exception as e:
            raise ErrorOnFindFiscal(
                message=f'Error on find all fiscais with pagination and filter: {str(e)}'
            ) from e

    def count_all_with_filter(self, search_term: str = None) -> int:
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(Fiscal)
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(Fiscal.name.ilike(search_filter))
                
                count = query.count()
                return count
        except Exception as e:
            raise ErrorOnFindFiscal(
                message=f'Error on count all fiscais with filter: {str(e)}'
            ) from e

    def update_status(self, fiscal_id: int, is_active: int) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).filter(Fiscal.id == fiscal_id).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with id {fiscal_id} not found')
                
                fiscal.is_active = is_active
                db.session.commit()
        except FiscalNotExists as e:
            raise e
        except Exception as e:
            raise ErroronUpdateFiscal(
                message=f'Error on update status for fiscal {fiscal_id}: {str(e)}'
            ) from e