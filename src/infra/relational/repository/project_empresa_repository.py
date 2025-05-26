from typing import List
from sqlalchemy import and_

from src.domain.entities.project_empresa import ProjectEmpresaEntity
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_project_empresa_repository import IProjectEmpresaRepository

# Errors
from src.errors.repository.already_exists_error.project_empresa_already_exists import ProjectEmpresaAlreadyExists
from src.errors.repository.not_exists_error.project_empresa_not_exists import ProjectEmpresaNotExists
from src.errors.repository.error_on_delete.error_on_update_empresa_from_project import ErrorOnUpdateEmpresaFromProject
from src.errors.repository.error_on_delete.error_on_delete_project_empresa import ErrorOnDeleteProjectEmpresa
from src.errors.repository.error_on_insert.error_on_insert_project_empresa import ErrorOnInsertProjectEmpresa
from src.errors.repository.error_on_find.error_on_find_project_empresa import ErrorOnFindProjectEmpresa
from src.errors.repository.has_related_children.project_empresa_has_related_children import ProjectEmpresaHasRelatedChildren
from sqlalchemy.exc import IntegrityError

class ProjectEmpresaRepository(IProjectEmpresaRepository):

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, project_id: int, empresa_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(ProjectEmpresa(project_id=project_id, empresa_id=empresa_id))
                db.session.commit()
        except IntegrityError as e:
            raise ProjectEmpresaAlreadyExists(
                message=f'Association (project_id={project_id}, empresa_id={empresa_id}) already exists.'
            ) from e
        except Exception as e:
            raise ErrorOnInsertProjectEmpresa(message=f'Error on insert project empresa project_id={project_id}, empresa_id={empresa_id}: {str(e)}') from e

    def find(self, project_id: int, empresa_id: int) -> ProjectEmpresaEntity:
        try:
            with self.__db_connection_handler as db:
                assoc = db.session.query(ProjectEmpresa).filter(
                    and_(
                        ProjectEmpresa.project_id == project_id,
                        ProjectEmpresa.empresa_id == empresa_id
                    )
                ).first()
                if not assoc:
                    raise ProjectEmpresaNotExists(
                        message=f'No association found for project_id={project_id} and empresa_id={empresa_id}'
                    )
                return ProjectEmpresaEntity(
                    project_id=assoc.project_id,
                    empresa_id=assoc.empresa_id,
                    created_at=assoc.created_at
                )
        except ProjectEmpresaNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectEmpresa(message=f'Error on find project empresa project_id={project_id}, empresa_id={empresa_id}') from e

    def find_all_from_empresa(self, empresa_id: int) -> List[ProjectEmpresaEntity]:
        try:
            with self.__db_connection_handler as db:
                associations = db.session.query(ProjectEmpresa).filter(
                    ProjectEmpresa.empresa_id == empresa_id
                ).all()
                if not associations:
                    raise ProjectEmpresaNotExists(
                        message=f'No projects found for empresa_id={empresa_id}'
                    )
                return [
                    ProjectEmpresaEntity(
                        project_id=assoc.project_id,
                        empresa_id=assoc.empresa_id,
                        created_at=assoc.created_at
                    )
                    for assoc in associations
                ]
        except ProjectEmpresaNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectEmpresa(message=f'Error on find project empresa empresa_id={empresa_id}') from e

    def update_empresa(self, project_id: int, empresa_id: int, new_empresa_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectEmpresa).filter(
                    and_(
                        ProjectEmpresa.project_id == project_id,
                        ProjectEmpresa.empresa_id == empresa_id
                    )
                ).update({'empresa_id': new_empresa_id})
                db.session.commit()
        except IntegrityError as e:
            raise ProjectEmpresaAlreadyExists(f'Project empresa with project_id={project_id}, empresa_id={new_empresa_id} already exists: {str(e)}') from e
        except Exception as e:
            raise ErrorOnUpdateEmpresaFromProject(
                message=f'Error updating project {project_id} from empresa {empresa_id} to {new_empresa_id}'
            ) from e

    def delete(self, project_id: int, empresa_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_empresa = db.session.query(ProjectEmpresa).filter(
                    and_(
                        ProjectEmpresa.project_id == project_id,
                        ProjectEmpresa.empresa_id == empresa_id
                    )
                ).first()
                if not project_empresa:
                    raise ProjectEmpresaNotExists(message=f'Project empresa project_id={project_id}, empresa_id={empresa_id} does not exists')
                db.session.query(ProjectEmpresa).filter(
                    and_(
                        ProjectEmpresa.project_id == project_id,
                        ProjectEmpresa.empresa_id == empresa_id
                    )
                ).delete()
                db.session.commit()
        except IntegrityError as e:
            raise ProjectEmpresaHasRelatedChildren(message=f'Project empresa project_id={project_id}, empresa_id={empresa_id} has related children: {str(e)}') from e
        except ProjectEmpresaAlreadyExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnDeleteProjectEmpresa(
                message=f'Error deleting association (project_id={project_id}, empresa_id={empresa_id}): {e}'
            ) from e
    
    def delete_all_from_project(self, project_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_empresa = db.session.query(ProjectEmpresa).filter(
                    and_(
                        ProjectEmpresa.project_id == project_id
                    )
                ).all()
                if not any(project_empresa):
                    raise ProjectEmpresaNotExists(message=f'Project empresa from project project_id={project_id} does not exists')
                db.session.query(ProjectEmpresa).filter(
                    ProjectEmpresa.project_id == project_id,
                ).delete()
                db.session.commit()
        except IntegrityError as e:
            raise ProjectEmpresaHasRelatedChildren(message=f'Project empresa from project project_id={project_id} has related children: {str(e)}') from e
        except ProjectEmpresaNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnDeleteProjectEmpresa(
                message=f'Error deleting association (project_id={project_id}): {e}'
            ) from e