from src.domain.entities.folder import FolderEntity
from src.infra.relational.models.folder import Folder
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler

from src.data.interface.i_folder_repository import IFolderRepository
from typing import List, Optional

# Errors
from src.errors.repository.not_exists_error.folder_not_exists import FolderNotExists
from src.errors.repository.already_exists_error.folder_already_exists import FolderAlreadyExists
from src.errors.repository.error_on_delete.error_on_delete_folder import ErrorOnDeleteFolder
from src.errors.repository.error_on_insert.error_on_insert_folder import ErrorOnInsertFolder
from src.errors.repository.error_on_find.error_on_find_folder import ErrorOnFindFolder
from src.errors.repository.error_on_update.error_on_update_folder import ErrorOnUpdateFolder
from src.errors.repository.has_related_children.folder_has_related_children import FolderHasRelatedChildren
from sqlalchemy.exc import IntegrityError

# Import models to ensure SQLAlchemy can resolve relationships
from src.infra.relational.models.project_folder import ProjectFolder

class FolderRepository(IFolderRepository):

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                existing_folder = db.session.query(Folder).where(
                    Folder.name == name
                ).first()
                if existing_folder:
                    raise FolderAlreadyExists(f'Folder with name "{name}" already exists')
                
                db.session.add(Folder(name=name))
                db.session.commit()
        except FolderAlreadyExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnInsertFolder(
                message=f'Error on insert folder name={name}: {str(e)}'
            ) from e

    def find_by_id(self, folder_id: int) -> FolderEntity:
        try:
            with self.__db_connection_handler as db:
                folder_instance = db.session.query(Folder).where(
                    Folder.id == folder_id
                ).first()
                if folder_instance is None:
                    raise FolderNotExists(f'Folder with id "{folder_id}" does not exist')
                return FolderEntity(
                    folder_id=folder_instance.id,
                    name=folder_instance.name,
                    created_at=folder_instance.created_at,
                    updated_at=folder_instance.updated_at
                )
        except FolderNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindFolder(
                message=f'Error on find folder by id folder_id={folder_id}: {str(e)}'
            ) from e
    
    def find_by_name(self, name: str) -> Optional[FolderEntity]:
        try:
            with self.__db_connection_handler as db:
                folder_instance = db.session.query(Folder).where(
                    Folder.name == name
                ).first()
                if folder_instance is None:
                    return None
                return FolderEntity(
                    folder_id=folder_instance.id,
                    name=folder_instance.name,
                    created_at=folder_instance.created_at,
                    updated_at=folder_instance.updated_at
                )
        except Exception as e:
            raise ErrorOnFindFolder(
                message=f'Error on find folder by name name={name}: {str(e)}'
            ) from e
    
    def find_all(self) -> List[FolderEntity]:
        try:
            with self.__db_connection_handler as db:
                folders = db.session.query(Folder).all()
                folder_entities = [
                    FolderEntity(
                        folder_id=folder.id,
                        name=folder.name,
                        created_at=folder.created_at,
                        updated_at=folder.updated_at
                    )
                    for folder in folders
                ]
                return folder_entities
        except Exception as e:
            raise ErrorOnFindFolder(
                message=f'Error on find all folders: {str(e)}'
            ) from e

    def update(self, folder_id: int, new_name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                folder = db.session.query(Folder).where(
                    Folder.id == folder_id
                ).first()
                if not folder:
                    raise FolderNotExists(
                        message=f'Folder with id={folder_id} not exists'
                    )
                db.session.query(Folder).where(
                    Folder.id == folder_id
                ).update({'name': new_name})
                db.session.commit()
        except FolderNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnUpdateFolder(
                message=f'Error on update folder from id={folder_id} to name={new_name}: {str(e)}'
            ) from e

    def delete(self, folder_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                folder = db.session.query(Folder).where(
                    Folder.id == folder_id
                ).first()
                if not folder:
                    raise FolderNotExists(
                        message=f'Folder with id={folder_id} not exists'
                    )
                
                # Deletar todas as associações ProjectFolder antes de deletar a pasta
                db.session.query(ProjectFolder).where(
                    ProjectFolder.folder_id == folder_id
                ).delete()
                
                # Agora deletar a pasta
                db.session.query(Folder).where(
                    Folder.id == folder_id
                ).delete()
                db.session.commit()
        except FolderNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise FolderHasRelatedChildren(
                message='the registry cannot be deleted because it has related children'
            ) from e
        except Exception as e:
            raise ErrorOnDeleteFolder(
                message=f'Error on delete folder id={folder_id}: {str(e)}'
            ) from e

    def find_all_with_pagination(self, page_size: int, page: int) -> List[FolderEntity]:
        try:
            with self.__db_connection_handler as db:
                offset = (page - 1) * page_size
                folders = db.session.query(Folder).offset(offset).limit(page_size).all()
                folder_entities = [
                    FolderEntity(
                        folder_id=folder.id,
                        name=folder.name,
                        created_at=folder.created_at,
                        updated_at=folder.updated_at
                    )
                    for folder in folders
                ]
                return folder_entities
        except Exception as e:
            raise ErrorOnFindFolder(
                message=f'Error on find all folders with pagination: {str(e)}'
            ) from e

    def count_all(self) -> int:
        try:
            with self.__db_connection_handler as db:
                count = db.session.query(Folder).count()
                return count
        except Exception as e:
            raise ErrorOnFindFolder(
                message=f'Error on count all folders: {str(e)}'
            ) from e

    def find_all_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[FolderEntity]:
        try:
            with self.__db_connection_handler as db:
                offset = (page - 1) * page_size
                query = db.session.query(Folder)
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(Folder.name.ilike(search_filter))
                
                folders = query.offset(offset).limit(page_size).all()
                folder_entities = [
                    FolderEntity(
                        folder_id=folder.id,
                        name=folder.name,
                        created_at=folder.created_at,
                        updated_at=folder.updated_at
                    )
                    for folder in folders
                ]
                return folder_entities
        except Exception as e:
            raise ErrorOnFindFolder(
                message=f'Error on find all folders with pagination and filter: {str(e)}'
            ) from e

    def count_all_with_filter(self, search_term: str = None) -> int:
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(Folder)
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(Folder.name.ilike(search_filter))
                
                count = query.count()
                return count
        except Exception as e:
            raise ErrorOnFindFolder(
                message=f'Error on count all folders with filter: {str(e)}'
            ) from e

