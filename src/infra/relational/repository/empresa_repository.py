from src.domain.entities.empresa import EmpresaEntity
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.errors.repository.empresa_already_exists import EmpresaAlreadyExists
from src.errors.repository.empresa_not_exists import EmpresaNotExists
from src.data.interface.i_empresa_repository import IEmpresaRepository


class EmpresaRepository(IEmpresaRepository):
    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                existing_empresa = db.session.query(Empresa).where(
                    Empresa.name == name
                ).first()
                if existing_empresa:
                    raise EmpresaAlreadyExists(f'Empresa with name "{name}" already exists')
                db.session.add(Empresa(name=name))
                db.session.commit()
        except Exception as e:
            raise e

    def find_by_name(self, name: str) -> EmpresaEntity:
        try:
            with self.__db_connection_handler as db:
                empresa = db.session.query(Empresa).where(
                    Empresa.name == name
                ).first()
                if empresa is None:
                    raise EmpresaNotExists(f'Empresa with name "{name}" does not exist')
                return EmpresaEntity(
                    empresa_id=empresa.id,
                    name=empresa.name,
                    created_at=empresa.created_at
                )
        except Exception as e:
            raise e

    def update(self, name: str, new_name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Empresa).where(
                    Empresa.name == name
                ).update({'name': new_name})
                db.session.commit()
        except Exception as e:
            raise e

    def delete(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Empresa).where(
                    Empresa.name == name
                ).delete()
                db.session.commit()
        except Exception as e:
            raise e
