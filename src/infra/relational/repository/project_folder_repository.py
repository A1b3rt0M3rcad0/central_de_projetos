#pylint:disable=W0611
from typing import List
from sqlalchemy import and_

from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_project_folder_repository import IProjectFolderRepository

# Entities
from src.domain.entities.project_folder import ProjectFolderEntity

from src.infra.relational.models.project_folder import ProjectFolder
from src.infra.relational.models.folder import Folder
from src.infra.relational.models.project import Project

# Errors
from src.errors.repository.already_exists_error.project_folder_already_exists import ProjectFolderAlreadyExists
from src.errors.repository.not_exists_error.project_folder_not_exists import ProjectFolderNotExists
from src.errors.repository.error_on_delete.error_on_delete_project_folder import ErrorOnDeleteProjectFolder
from src.errors.repository.error_on_find.error_on_find_project_folder import ErrorOnFindProjectFolder
from src.errors.repository.error_on_insert.error_on_insert_project_folder import ErrorOnInsertProjectFolder
from sqlalchemy.exc import IntegrityError

class ProjectFolderRepository(IProjectFolderRepository):
    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, project_id: int, folder_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                # Verificar se a associação já existe
                existing = db.session.query(ProjectFolder).where(
                    and_(
                        ProjectFolder.project_id == project_id,
                        ProjectFolder.folder_id == folder_id
                    )
                ).first()
                if existing:
                    raise ProjectFolderAlreadyExists(
                        message=f'ProjectFolder with (project_id: {project_id}, folder_id: {folder_id}) already exists'
                    )
                
                # Criar nova associação (ID será gerado automaticamente pelo autoincrement)
                db.session.add(ProjectFolder(
                    project_id=project_id,
                    folder_id=folder_id
                ))
                db.session.commit()
        except ProjectFolderAlreadyExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectFolderAlreadyExists(
                message=f'ProjectFolder with (project_id: {project_id}, folder_id: {folder_id}) already exists: {e}'
            ) from e
        except Exception as e:
            raise ErrorOnInsertProjectFolder(
                message=f'Error on insert project folder project_id={project_id}, folder_id={folder_id}: {str(e)}'
            ) from e

    def find(self, project_id: int, folder_id: int) -> ProjectFolderEntity:
        try:
            with self.__db_connection_handler as db:
                relation = db.session.query(ProjectFolder).where(
                    and_(
                        ProjectFolder.project_id == project_id,
                        ProjectFolder.folder_id == folder_id
                    )
                ).first()
                if not relation:
                    raise ProjectFolderNotExists(
                        message=f'No ProjectFolder with (project_id: {project_id}, folder_id: {folder_id}) found'
                    )
                return ProjectFolderEntity(
                    id_=relation.id,
                    project_id=relation.project_id,
                    folder_id=relation.folder_id,
                    created_at=relation.created_at,
                    updated_at=relation.updated_at
                )
        except ProjectFolderNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectFolder(
                message=f'Error on find project folder project_id={project_id}, folder_id={folder_id}: {str(e)}'
            ) from e

    def find_all_from_folder(self, folder_id: int) -> List[ProjectFolderEntity]:
        try:
            with self.__db_connection_handler as db:
                relations = db.session.query(ProjectFolder).where(
                    ProjectFolder.folder_id == folder_id
                ).all()
                if not relations:
                    raise ProjectFolderNotExists(
                        message=f'No projects found for folder_id: {folder_id}'
                    )
                return [
                    ProjectFolderEntity(
                        id_=relation.id,
                        project_id=relation.project_id,
                        folder_id=relation.folder_id,
                        created_at=relation.created_at,
                        updated_at=relation.updated_at
                    ) for relation in relations
                ]
        except ProjectFolderNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectFolder(
                message=f'Error on find project_folder with folder_id={folder_id}: {str(e)}'
            ) from e
    
    def find_all_from_project(self, project_id: int) -> List[ProjectFolderEntity]:
        try:
            with self.__db_connection_handler as db:
                relations = db.session.query(ProjectFolder).where(
                    ProjectFolder.project_id == project_id,
                ).all()
                if not any(relations):
                    raise ProjectFolderNotExists(
                        message=f'Project folder from project project_id={project_id} does not exists'
                    )
                return [
                    ProjectFolderEntity(
                        id_=relation.id,
                        project_id=relation.project_id,
                        folder_id=relation.folder_id,
                        created_at=relation.created_at,
                        updated_at=relation.updated_at
                    ) for relation in relations
                ]
        except ProjectFolderNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectFolder(
                message=f'Error on find all from project project_id={project_id}: {str(e)}'
            ) from e

    def delete(self, project_id: int, folder_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_folder = db.session.query(ProjectFolder).where(
                    and_(
                        ProjectFolder.project_id == project_id,
                        ProjectFolder.folder_id == folder_id
                    )
                ).first()
                if not project_folder:
                    raise ProjectFolderNotExists(
                        message=f'Project folder project_id={project_id}, folder_id={folder_id} not exists'
                    )
                db.session.query(ProjectFolder).where(
                    and_(
                        ProjectFolder.project_id == project_id,
                        ProjectFolder.folder_id == folder_id
                    )
                ).delete()
                db.session.commit()
        except ProjectFolderNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnDeleteProjectFolder(
                message=f'Error deleting ProjectFolder (project_id: {project_id}, folder_id: {folder_id}): {e}'
            ) from e
    
    def delete_all_from_project(self, project_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_folders = db.session.query(ProjectFolder).where(
                    ProjectFolder.project_id == project_id,
                ).all()
                # Não lançar exceção se não houver pastas - apenas deletar se existir
                if any(project_folders):
                    db.session.query(ProjectFolder).where(
                        ProjectFolder.project_id == project_id,
                    ).delete()
                    db.session.commit()
        except Exception as e:
            raise ErrorOnDeleteProjectFolder(
                message=f'Error deleting ProjectFolder (project_id: {project_id}): {e}'
            ) from e
    
    def delete_all_from_folder(self, folder_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_folders = db.session.query(ProjectFolder).where(
                    ProjectFolder.folder_id == folder_id,
                ).all()
                if not any(project_folders):
                    raise ProjectFolderNotExists(
                        message=f'Project Folder from folder folder_id={folder_id} not exists'
                    )
                db.session.query(ProjectFolder).where(
                    ProjectFolder.folder_id == folder_id,
                ).delete()
                db.session.commit()
        except ProjectFolderNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnDeleteProjectFolder(
                message=f'Error deleting ProjectFolder (folder_id: {folder_id}): {e}'
            ) from e

