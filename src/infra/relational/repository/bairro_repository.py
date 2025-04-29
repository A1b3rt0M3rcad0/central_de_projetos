from src.domain.entities.bairro import BairroEntity
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.errors.repository.bairro_not_exists import BairroNotExists
from src.errors.repository.bairro_already_exists import BairroAlreadyExists
from src.data.interface.i_bairro_repository import IBairroRepository

class BairroRepository(IBairroRepository):

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                existing_bairro = db.session.query(Bairro).where(
                    Bairro.name == name
                ).first()
                if existing_bairro:
                    raise BairroAlreadyExists(f'Bairro with name "{name}" already exists')
                db.session.add(Bairro(name=name))
                db.session.commit()
        except Exception as e:
            raise e

    def find_by_name(self, name: str) -> BairroEntity:
        try:
            with self.__db_connection_handler as db:
                bairro = db.session.query(Bairro).where(
                    Bairro.name == name
                ).first()
                if bairro is None:
                    raise BairroNotExists(f'Bairro with name "{name}" does not exist')
                return BairroEntity(
                    bairro_id=bairro.id,
                    name=bairro.name,
                    created_at=bairro.created_at
                )
        except Exception as e:
            raise e

    def update(self, name: str, new_name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Bairro).where(
                    Bairro.name == name
                ).update({'name': new_name})
                db.session.commit()
        except Exception as e:
            raise e

    def delete(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Bairro).where(
                    Bairro.name == name
                ).delete()
                db.session.commit()
        except Exception as e:
            raise e