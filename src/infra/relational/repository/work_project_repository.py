#pylint:disable=W0611,R0912,R0915
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from typing import List, Dict, Union
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from datetime import datetime
from sqlalchemy.orm import joinedload

from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.project import ProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.value_objects.monetary_value import MonetaryValue

from src.infra.relational.models.work_project import WorkProject
from src.infra.relational.models.project import Project
from src.infra.relational.models.fiscal import Fiscal

# Errors
from src.errors.repository.not_exists_error.work_project_not_exists import WorkProjectNotExists
from src.errors.repository.already_exists_error.work_project_already_exists import WorkProjectAlreadyExists
from src.errors.repository.error_on_delete.error_on_delete_work_project import ErrorOnDeleteWorkProject
from src.errors.repository.error_on_insert.error_on_insert_work_project import ErrorOnInsertWorkProject
from src.errors.repository.error_on_find.error_on_find_work_project import ErrorOnFindWorkProject
from src.errors.repository.error_on_update.error_on_update_work_project import ErrorOnUpdateWorkProject
from sqlalchemy.exc import IntegrityError

class WorkProjectRepository(IWorkProjectRepository):
    
    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, project_id:int, fiscal_id:int, title:str, description:str, photo_name:str, additional_documents:str=None) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.add(WorkProject(
                    project_id=project_id,
                    fiscal_id=fiscal_id,
                    title=title,
                    description=description,
                    photo_name=photo_name,
                    additional_documents=additional_documents
                ))
                db.session.commit()
            except IntegrityError as e:
                raise WorkProjectAlreadyExists(
                    message=f'WorkProject with project_id={project_id}, fiscal_id={fiscal_id}, title={title} already exists: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnInsertWorkProject(
                    message=f'Error on insert work_project project_id={project_id}, fiscal_id={fiscal_id}, title={title}: {str(e)}'
                ) from e
    
    def find(self, work_project_id:int) -> WorkProjectEntity:
        with self.__db_connection_handler as db:
            try:
                work_project = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).where(
                    WorkProject.id == work_project_id
                ).first()
                
                if not work_project:
                    raise WorkProjectNotExists(message=f'WorkProject with id: {work_project_id} does not exists')
                
                return WorkProjectEntity(
                    id=work_project.id,
                    project_id=work_project.project_id,
                    fiscal_id=work_project.fiscal_id,
                    title=work_project.title,
                    description=work_project.description,
                    photo_name=work_project.photo_name,
                    additional_documents=work_project.additional_documents,
                    created_at=work_project.created_at,
                    updated_at=work_project.updated_at,
                    fiscal=FiscalEntity(
                        fiscal_id=work_project.fiscal.id,
                        name=work_project.fiscal.name,
                        created_at=work_project.fiscal.created_at
                    ),
                    project=ProjectEntity(
                        project_id=work_project.project.id,
                        status_id=work_project.project.status_id,
                        name=work_project.project.name,
                        andamento_do_projeto=work_project.project.andamento_do_projeto,
                        verba_disponivel=MonetaryValue(work_project.project.verba_disponivel),
                        start_date=work_project.project.start_date,
                        expected_completion_date=work_project.project.expected_completion_date,
                        end_date=work_project.project.end_date
                    )
                )
            except WorkProjectNotExists:
                raise
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on find work_project with id: {work_project_id}: {str(e)}'
                ) from e
    
    def find_all(self) -> List[WorkProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                work_projects = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).all()
                
                return [
                    WorkProjectEntity(
                        id=wp.id,
                        project_id=wp.project_id,
                        fiscal_id=wp.fiscal_id,
                        title=wp.title,
                        description=wp.description,
                        photo_name=wp.photo_name,
                        additional_documents=wp.additional_documents,
                        created_at=wp.created_at,
                        updated_at=wp.updated_at,
                        fiscal=FiscalEntity(
                            fiscal_id=wp.fiscal.id,
                            name=wp.fiscal.name,
                            created_at=wp.fiscal.created_at
                        ),
                        project=ProjectEntity(
                            project_id=wp.project.id,
                            status_id=wp.project.status_id,
                            name=wp.project.name,
                            andamento_do_projeto=wp.project.andamento_do_projeto,
                            verba_disponivel=MonetaryValue(wp.project.verba_disponivel),
                            start_date=wp.project.start_date,
                            expected_completion_date=wp.project.expected_completion_date,
                            end_date=wp.project.end_date
                        )
                    ) for wp in work_projects
                ]
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on find all work_projects: {str(e)}'
                ) from e
    
    def find_by_project(self, project_id:int) -> List[WorkProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                work_projects = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).where(
                    WorkProject.project_id == project_id
                ).all()
                
                return [
                    WorkProjectEntity(
                        id=wp.id,
                        project_id=wp.project_id,
                        fiscal_id=wp.fiscal_id,
                        title=wp.title,
                        description=wp.description,
                        photo_name=wp.photo_name,
                        additional_documents=wp.additional_documents,
                        created_at=wp.created_at,
                        updated_at=wp.updated_at,
                        fiscal=FiscalEntity(
                            fiscal_id=wp.fiscal.id,
                            name=wp.fiscal.name,
                            created_at=wp.fiscal.created_at
                        ),
                        project=ProjectEntity(
                            project_id=wp.project.id,
                            status_id=wp.project.status_id,
                            name=wp.project.name,
                            andamento_do_projeto=wp.project.andamento_do_projeto,
                            verba_disponivel=MonetaryValue(wp.project.verba_disponivel),
                            start_date=wp.project.start_date,
                            expected_completion_date=wp.project.expected_completion_date,
                            end_date=wp.project.end_date
                        )
                    ) for wp in work_projects
                ]
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on find work_projects by project_id: {project_id}: {str(e)}'
                ) from e
    
    def find_by_fiscal(self, fiscal_id:int) -> List[WorkProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                work_projects = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).where(
                    WorkProject.fiscal_id == fiscal_id
                ).all()
                
                return [
                    WorkProjectEntity(
                        id=wp.id,
                        project_id=wp.project_id,
                        fiscal_id=wp.fiscal_id,
                        title=wp.title,
                        description=wp.description,
                        photo_name=wp.photo_name,
                        additional_documents=wp.additional_documents,
                        created_at=wp.created_at,
                        updated_at=wp.updated_at,
                        fiscal=FiscalEntity(
                            fiscal_id=wp.fiscal.id,
                            name=wp.fiscal.name,
                            created_at=wp.fiscal.created_at
                        ),
                        project=ProjectEntity(
                            project_id=wp.project.id,
                            status_id=wp.project.status_id,
                            name=wp.project.name,
                            andamento_do_projeto=wp.project.andamento_do_projeto,
                            verba_disponivel=MonetaryValue(wp.project.verba_disponivel),
                            start_date=wp.project.start_date,
                            expected_completion_date=wp.project.expected_completion_date,
                            end_date=wp.project.end_date
                        )
                    ) for wp in work_projects
                ]
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on find work_projects by fiscal_id: {fiscal_id}: {str(e)}'
                ) from e
    
    def find_by_project_and_fiscal(self, project_id:int, fiscal_id:int) -> List[WorkProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                work_projects = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).where(
                    WorkProject.project_id == project_id,
                    WorkProject.fiscal_id == fiscal_id
                ).all()
                
                return [
                    WorkProjectEntity(
                        id=wp.id,
                        project_id=wp.project_id,
                        fiscal_id=wp.fiscal_id,
                        title=wp.title,
                        description=wp.description,
                        photo_name=wp.photo_name,
                        additional_documents=wp.additional_documents,
                        created_at=wp.created_at,
                        updated_at=wp.updated_at,
                        fiscal=FiscalEntity(
                            fiscal_id=wp.fiscal.id,
                            name=wp.fiscal.name,
                            created_at=wp.fiscal.created_at
                        ),
                        project=ProjectEntity(
                            project_id=wp.project.id,
                            status_id=wp.project.status_id,
                            name=wp.project.name,
                            andamento_do_projeto=wp.project.andamento_do_projeto,
                            verba_disponivel=MonetaryValue(wp.project.verba_disponivel),
                            start_date=wp.project.start_date,
                            expected_completion_date=wp.project.expected_completion_date,
                            end_date=wp.project.end_date
                        )
                    ) for wp in work_projects
                ]
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on find work_projects by project_id: {project_id} and fiscal_id: {fiscal_id}: {str(e)}'
                ) from e
    
    def find_by_title(self, title:str) -> WorkProjectEntity:
        with self.__db_connection_handler as db:
            try:
                work_project = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).where(
                    WorkProject.title == title
                ).first()
                
                if not work_project:
                    raise WorkProjectNotExists(message=f'WorkProject with title: {title} does not exists')
                
                return WorkProjectEntity(
                    id=work_project.id,
                    project_id=work_project.project_id,
                    fiscal_id=work_project.fiscal_id,
                    title=work_project.title,
                    description=work_project.description,
                    photo_name=work_project.photo_name,
                    additional_documents=work_project.additional_documents,
                    created_at=work_project.created_at,
                    updated_at=work_project.updated_at,
                    fiscal=FiscalEntity(
                        fiscal_id=work_project.fiscal.id,
                        name=work_project.fiscal.name,
                        created_at=work_project.fiscal.created_at
                    ),
                    project=ProjectEntity(
                        project_id=work_project.project.id,
                        status_id=work_project.project.status_id,
                        name=work_project.project.name,
                        andamento_do_projeto=work_project.project.andamento_do_projeto,
                        verba_disponivel=MonetaryValue(work_project.project.verba_disponivel),
                        start_date=work_project.project.start_date,
                        expected_completion_date=work_project.project.expected_completion_date,
                        end_date=work_project.project.end_date
                    )
                )
            except WorkProjectNotExists:
                raise
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on find work_project with title: {title}: {str(e)}'
                ) from e
    
    def find_by_title_and_fiscal(self, title:str, fiscal_id:int) -> WorkProjectEntity:
        with self.__db_connection_handler as db:
            try:
                work_project = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).where(
                    WorkProject.title == title,
                    WorkProject.fiscal_id == fiscal_id
                ).first()
                
                if not work_project:
                    raise WorkProjectNotExists(message=f'WorkProject with title: {title} and fiscal_id: {fiscal_id} does not exists')
                
                return WorkProjectEntity(
                    id=work_project.id,
                    project_id=work_project.project_id,
                    fiscal_id=work_project.fiscal_id,
                    title=work_project.title,
                    description=work_project.description,
                    photo_name=work_project.photo_name,
                    additional_documents=work_project.additional_documents,
                    created_at=work_project.created_at,
                    updated_at=work_project.updated_at,
                    fiscal=FiscalEntity(
                        fiscal_id=work_project.fiscal.id,
                        name=work_project.fiscal.name,
                        created_at=work_project.fiscal.created_at
                    ),
                    project=ProjectEntity(
                        project_id=work_project.project.id,
                        status_id=work_project.project.status_id,
                        name=work_project.project.name,
                        andamento_do_projeto=work_project.project.andamento_do_projeto,
                        verba_disponivel=MonetaryValue(work_project.project.verba_disponivel),
                        start_date=work_project.project.start_date,
                        expected_completion_date=work_project.project.expected_completion_date,
                        end_date=work_project.project.end_date
                    )
                )
            except WorkProjectNotExists:
                raise
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on find work_project with title: {title} and fiscal_id: {fiscal_id}: {str(e)}'
                ) from e
    
    def count_work_projects(self) -> Dict[str, int]:
        with self.__db_connection_handler as db:
            try:
                total_count = db.session.query(WorkProject).count()
                return {"total": total_count}
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on count work_projects: {str(e)}'
                ) from e
    
    def get_work_projects_with_pagination(self, page:int, page_size:int) -> Dict[str, Union[int, WorkProjectEntity]]:
        with self.__db_connection_handler as db:
            try:
                offset = (page - 1) * page_size
                
                total_count = db.session.query(WorkProject).count()
                
                work_projects = db.session.query(WorkProject).options(
                    joinedload(WorkProject.project),
                    joinedload(WorkProject.fiscal)
                ).offset(offset).limit(page_size).all()
                
                work_project_entities = [
                    WorkProjectEntity(
                        id=wp.id,
                        project_id=wp.project_id,
                        fiscal_id=wp.fiscal_id,
                        title=wp.title,
                        description=wp.description,
                        photo_name=wp.photo_name,
                        additional_documents=wp.additional_documents,
                        created_at=wp.created_at,
                        updated_at=wp.updated_at,
                        fiscal=FiscalEntity(
                            fiscal_id=wp.fiscal.id,
                            name=wp.fiscal.name,
                            created_at=wp.fiscal.created_at
                        ),
                        project=ProjectEntity(
                            project_id=wp.project.id,
                            status_id=wp.project.status_id,
                            name=wp.project.name,
                            andamento_do_projeto=wp.project.andamento_do_projeto,
                            verba_disponivel=MonetaryValue(wp.project.verba_disponivel),
                            start_date=wp.project.start_date,
                            expected_completion_date=wp.project.expected_completion_date,
                            end_date=wp.project.end_date
                        )
                    ) for wp in work_projects
                ]
                
                return {
                    "total": total_count,
                    "data": work_project_entities
                }
            except Exception as e:
                raise ErrorOnFindWorkProject(
                    message=f'Error on get work_projects with pagination: {str(e)}'
                ) from e
    
    def update(self, work_project_id:int, update_params:Dict) -> None:
        with self.__db_connection_handler as db:
            try:
                work_project = db.session.query(WorkProject).where(
                    WorkProject.id == work_project_id
                ).first()
                
                if not work_project:
                    raise WorkProjectNotExists(message=f'WorkProject with id: {work_project_id} does not exists')
                
                for key, value in update_params.items():
                    if hasattr(work_project, key):
                        setattr(work_project, key, value)
                
                work_project.updated_at = datetime.now()
                db.session.commit()
            except WorkProjectNotExists:
                raise
            except Exception as e:
                raise ErrorOnUpdateWorkProject(
                    message=f'Error on update work_project with id: {work_project_id}: {str(e)}'
                ) from e
    
    def delete(self, work_project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                work_project = db.session.query(WorkProject).where(
                    WorkProject.id == work_project_id
                ).first()
                
                if not work_project:
                    raise WorkProjectNotExists(message=f'WorkProject with id: {work_project_id} does not exists')
                
                db.session.delete(work_project)
                db.session.commit()
            except WorkProjectNotExists:
                raise
            except Exception as e:
                raise ErrorOnDeleteWorkProject(
                    message=f'Error on delete work_project with id: {work_project_id}: {str(e)}'
                ) from e 