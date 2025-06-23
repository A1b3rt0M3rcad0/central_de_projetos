#pylint:disable=W0611
from typing import List
from sqlalchemy import and_

from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_project_type_repository import IProjectTypeRepository

# Entities
from src.domain.entities.project_type import ProjectTypeEntity
from src.domain.entities.types import TypesEntity
from src.domain.entities.project_types_count_by_bairro import ProjectTypesCountByBairro

from src.infra.relational.models.types import Types
from src.infra.relational.models.project import Project
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.models.project_bairro import ProjectBairro

# Errors
from src.errors.repository.already_exists_error.project_type_already_exists import ProjectTypeAlreadyExists
from src.errors.repository.not_exists_error.project_type_not_exists import ProjectTypeNotExists
from src.errors.repository.error_on_delete.error_on_delete_project_type import ErrorOnDeleteProjectType
from src.errors.repository.error_on_find.error_on_find_project_type import ErrorOnFindProjectType
from src.errors.repository.error_on_insert.error_on_insert_project_type import ErrorOnInsertProjectType
from src.errors.repository.error_on_update.error_on_update_project_type import ErrorOnUpdateProjectType
from src.errors.repository.has_related_children.project_type_has_related_children import ProjectTypeHasRelatedChildren
from sqlalchemy.exc import IntegrityError

class ProjectTypeRepository(IProjectTypeRepository):
    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, project_id: int, type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(ProjectType(project_id=project_id, type_id=type_id))
                db.session.commit()
        except IntegrityError as e:
            raise ProjectTypeAlreadyExists(
                message=f'ProjectType with (project_id: {project_id}, type_id: {type_id}) already exists: {e}'
            ) from e
        except Exception as e:
            raise ErrorOnInsertProjectType(
                message=f'Error on insert project type project_id={project_id}, type_id={type_id}: {str(e)}'
            ) from e

    def find(self, project_id: int, type_id: int) -> ProjectTypeEntity:
        try:
            with self.__db_connection_handler as db:
                relation = db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).first()
                if not relation:
                    raise ProjectTypeNotExists(
                        message=f'No ProjectType with (project_id: {project_id}, type_id: {type_id}) found'
                    )
                return ProjectTypeEntity(
                    project_id=relation.project_id,
                    type_id=relation.type_id,
                    created_at=relation.created_at
                )
        except ProjectTypeNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectType(
                message=f'Error on find project type project_id={project_id}, type_id={type_id}: {str(e)}'
            ) from e


    def find_all_from_type(self, type_id: int) -> List[ProjectTypeEntity]:
        try:
            with self.__db_connection_handler as db:
                relations = db.session.query(ProjectType).where(
                    ProjectType.type_id == type_id
                ).all()
                if not relations:
                    raise ProjectTypeNotExists(
                        message=f'No projects found for type_id: {type_id}'
                    )
                return [
                    ProjectTypeEntity(
                        project_id=relation.project_id,
                        type_id=relation.type_id,
                        created_at=relation.created_at
                    ) for relation in relations
                ]
        except ProjectTypeNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectType(
                message=f'Error on find project_type with type_id={type_id}: {str(e)}'
            ) from e
    
    def get_project_types_count_by_bairro(self) -> ProjectTypesCountByBairro:
        try:
            with self.__db_connection_handler as db:
                projects: List[Project] = db.session.query(Project).all()
                project_types: List[ProjectType] = db.session.query(ProjectType).all()
                types: List[Types] = db.session.query(Types).all()
                bairros: List[Bairro] = db.session.query(Bairro).all()
                project_bairros: List[ProjectBairro] = db.session.query(ProjectBairro).all()

                types_look_up = {t.id: t for t in types}
                bairro_lookup = {b.id: b.name for b in bairros}

                # Mapeamento: project_id -> bairro_id (único bairro por projeto assumido)
                project_to_bairro = {pb.project_id: pb.bairro_id for pb in project_bairros}

                # Agrupar project_types por project_id
                project_type_lookup = {}
                for pt in project_types:
                    if pt.project_id not in project_type_lookup:
                        project_type_lookup[pt.project_id] = []
                    project_type_lookup[pt.project_id].append(pt)

                # Construir a estrutura desejada
                types_count_by_bairro = {}
                for project in projects:
                    bairro_id = project_to_bairro.get(project.id)
                    if bairro_id is None:
                        # Ignorar projetos sem bairro associado
                        continue

                    bairro_name = bairro_lookup.get(bairro_id, "Desconhecido")

                    if bairro_id not in types_count_by_bairro:
                        types_count_by_bairro[bairro_id] = {bairro_name: {}}

                    for pt in project_type_lookup.get(project.id, []):
                        type_id = pt.type_id
                        type_name = types_look_up[type_id].name

                        if type_name not in types_count_by_bairro[bairro_id][bairro_name]:
                            types_count_by_bairro[bairro_id][bairro_name][type_name] = 0

                        types_count_by_bairro[bairro_id][bairro_name][type_name] += 1

                return {
                    "types": [
                        TypesEntity(
                            types_id=type_model.id,
                            name=type_model.name,
                            created_at=type_model.created_at
                        )
                        for type_model in types
                    ],
                    "types_count_by_bairro": types_count_by_bairro
                }
        except Exception as e:
            raise ErrorOnFindProjectType(
                message=f'Error on {self.get_project_types_count_by_bairro.__name__}: {str(e)}'
            ) from e

    def update_type(self, project_id: int, type_id: int, new_type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_type = db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).first()
                if not project_type:
                    raise ProjectTypeNotExists(
                        message=f'Project type project_id={project_id}, type_id={type_id} not exists'
                    )
                db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).update({'type_id': new_type_id})
                db.session.commit()
        except ProjectTypeNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectTypeAlreadyExists(
                message=f'Project type project_id={project_id}, type_id={new_type_id} already exists'
            ) from e
        except Exception as e:
            raise ErrorOnUpdateProjectType(
                message=f'Error updating ProjectType (project_id: {project_id}, type_id: {type_id}) to {new_type_id}'
            ) from e

    def delete(self, project_id: int, type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_type = db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).first()
                if not project_type:
                    raise ProjectTypeNotExists(
                        message=f'Project type project_id={project_id}, type_id={type_id} not exists'
                    )
                db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).delete()
                db.session.commit()
        except ProjectTypeNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectTypeHasRelatedChildren(
                message=f'Project type from project project_id={project_id}, type_id={type_id} has related children'
            ) from e
        except Exception as e:
            raise ErrorOnDeleteProjectType(
                message=f'Error deleting ProjectType (project_id: {project_id}, type_id: {type_id}): {e}'
            ) from e

    def delete_all_from_project(self, project_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_type = db.session.query(ProjectType).where(
                    ProjectType.project_id == project_id,
                ).all()
                if not any(project_type):
                    raise ProjectTypeNotExists(
                        message=f'Project Type from project project_id={project_id} not exists'
                    )
                db.session.query(ProjectType).where(
                    ProjectType.project_id == project_id,
                ).delete()
                db.session.commit()
        except ProjectTypeNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectTypeHasRelatedChildren(
                message=f'Project type from project_id={project_id} has related children: {str(e)}'
            ) from e
        except Exception as e:
            raise ErrorOnDeleteProjectType(
                message=f'Error deleting ProjectType (project_id: {project_id}): {e}'
            ) from e
    
    def select_all_from_project(self, project_id:int) -> List[ProjectTypeEntity]:
        try:
            with self.__db_connection_handler as db:
                relations = db.session.query(ProjectType).where(
                    ProjectType.project_id == project_id,
                ).all()
                if not any(relations):
                    raise ProjectTypeNotExists(
                        message=f'Project type from project project_id={project_id} does not exists'
                    )
                return [
                    ProjectTypeEntity(
                        project_id=relation.project_id,
                        type_id=relation.type_id,
                        created_at=relation.created_at
                    ) for relation in relations
                ]
        except ProjectTypeNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectType(
                message=f'Error on find all from project project_id={project_id}: {str(e)}'
            ) from e