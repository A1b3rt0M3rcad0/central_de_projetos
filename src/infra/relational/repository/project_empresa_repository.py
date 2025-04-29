from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from src.domain.entities.project_empresa import ProjectEmpresaEntity
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler

from src.errors.repository.project_empresa_already_exists import ProjectEmpresaAlreadyExists
from src.errors.repository.projects_from_empresa_does_not_exists import ProjectsFromEmpresaDoesNotExists
from src.errors.repository.error_on_update_empresa_from_project import ErrorOnUpdateEmpresaFromProject
from src.errors.repository.error_on_delete_project_empresa import ErrorOnDeleteProjectEmpresa

from src.data.interface.i_project_empresa_repository import IProjectEmpresaRepository


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
            raise e

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
                    raise ProjectsFromEmpresaDoesNotExists(
                        message=f'No association found for project_id={project_id} and empresa_id={empresa_id}'
                    )
                return ProjectEmpresaEntity(
                    project_id=assoc.project_id,
                    empresa_id=assoc.empresa_id,
                    created_at=assoc.created_at
                )
        except Exception as e:
            raise e

    def find_all_from_empresa(self, empresa_id: int) -> List[ProjectEmpresaEntity]:
        try:
            with self.__db_connection_handler as db:
                associations = db.session.query(ProjectEmpresa).filter(
                    ProjectEmpresa.empresa_id == empresa_id
                ).all()
                if not associations:
                    raise ProjectsFromEmpresaDoesNotExists(
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
        except Exception as e:
            raise e

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
        except Exception as e:
            raise ErrorOnUpdateEmpresaFromProject(
                message=f'Error updating project {project_id} from empresa {empresa_id} to {new_empresa_id}'
            ) from e

    def delete(self, project_id: int, empresa_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectEmpresa).filter(
                    and_(
                        ProjectEmpresa.project_id == project_id,
                        ProjectEmpresa.empresa_id == empresa_id
                    )
                ).delete()
                db.session.commit()
        except Exception as e:
            raise ErrorOnDeleteProjectEmpresa(
                message=f'Error deleting association (project_id={project_id}, empresa_id={empresa_id}): {e}'
            ) from e