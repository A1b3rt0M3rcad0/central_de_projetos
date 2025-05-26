from src.domain.entities.empresa import EmpresaEntity
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_empresa_repository import IEmpresaRepository

# Errors
from src.errors.repository.already_exists_error.empresa_already_exists import EmpresaAlreadyExists
from src.errors.repository.not_exists_error.empresa_not_exists import EmpresaNotExists
from src.errors.repository.error_on_insert.error_on_insert_empresa import ErrorOnInsertEmpresa
from src.errors.repository.error_on_find.error_on_find_empresa import ErrorOnFindEmpresa
from src.errors.repository.error_on_update.error_on_update_empresa import ErrorOnUpdateEmpresa
from src.errors.repository.error_on_delete.error_on_delete_empresa import ErrorOnDeleteEmpresa
from src.errors.repository.has_related_children.empresa_has_related_childre import EmpresaHasRelatedChildren
from sqlalchemy.exc import IntegrityError


class EmpresaRepository(IEmpresaRepository):
    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(Empresa(name=name))
                db.session.commit()
        except IntegrityError as e:
            raise EmpresaAlreadyExists(message=f'Empresa {name} already exists: {str(e)}') from e
        except Exception as e:
            raise ErrorOnInsertEmpresa(message=f'Error on insert empresa {name}: {str(e)}') from e

    def find_by_name(self, name: str) -> EmpresaEntity:
        try:
            with self.__db_connection_handler as db:
                empresa = db.session.query(Empresa).where(
                    Empresa.name == name
                ).first()
                if empresa is None:
                    raise EmpresaNotExists(message=f'Empresa with name "{name}" does not exist')
                return EmpresaEntity(
                    empresa_id=empresa.id,
                    name=empresa.name,
                    created_at=empresa.created_at
                )
        except EmpresaNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindEmpresa(message=f'Error on find empresa with name {name}: {str(e)}') from e

    def update(self, name: str, new_name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                bairro = db.session.query(Empresa).where(Empresa.name == name).first()
                if not bairro:
                    raise EmpresaNotExists(message=f'Empresa with name "{name}" does not exist')
                db.session.query(Empresa).where(
                    Empresa.name == name
                ).update({'name': new_name})
                db.session.commit()
        except EmpresaNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise EmpresaAlreadyExists(message=f'Empresa with name "{name}" already exists') from e
        except Exception as e:
            raise ErrorOnUpdateEmpresa(message=f'Error on update empresa name {name} -> {new_name}: {str(e)}') from e

    def delete(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                bairro = db.session.query(Empresa).where(
                    Empresa.name == name
                ).first()
                if not bairro:
                    raise EmpresaNotExists(message=f'Empresa with name "{name}" does not exist')
                db.session.query(Empresa).where(Empresa.name == name).delete()
                db.session.commit()
        except EmpresaNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise EmpresaHasRelatedChildren(f'Empresas {name} not deleted because has a related children: {str(e)}') from e
        except Exception as e:
            raise ErrorOnDeleteEmpresa(message=f'Error on delete empresa {name}: {str(e)}') from e