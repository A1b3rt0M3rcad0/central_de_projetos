#pylint:disable=W0611
from src.data.interface.i_project_repository import IProjectRepository
from typing import Optional, List, Dict
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.errors.repository.not_exists_error.projects_does_not_exists import ProjectsDoesNotExists
from src.errors.repository.error_on_delete.error_on_delete_project import ErrorOnDeleteProject
from datetime import datetime

from src.infra.relational.models.project import Project
from src.infra.relational.models.status import Status

class ProjectRepository(IProjectRepository):
    
    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, 
               status_id:int,
               name:str|None=None, 
               verba_disponivel:Optional[MonetaryValue]=None, 
               andamento_do_projeto:Optional[str]=None, 
               start_date:Optional[datetime]=None, 
               expected_completion_date:Optional[datetime]=None, 
               end_date:Optional[datetime]=None,
               ) -> None:
        with self.__db_connection_handler as db:
            status_id_entry = status_id
            name_entry = name
            verba_disponivel_entry = verba_disponivel.value
            andamento_do_projeto_entry = andamento_do_projeto
            start_date_entry = start_date
            expected_completion_date_entry = expected_completion_date
            end_date_entry = end_date
            try:
                db.session.add(Project(
                    status_id=status_id_entry,
                    name=name_entry,
                    verba_disponivel=verba_disponivel_entry,
                    andamento_do_projeto=andamento_do_projeto_entry,
                    start_date = start_date_entry,
                    expected_completion_date = expected_completion_date_entry,
                    end_date = end_date_entry

                ))
                db.session.commit()
            except Exception as e:
                raise e
    
    def find(self, project_id:int) -> ProjectEntity:
        with self.__db_connection_handler as db:
            try:
                project = db.session.query(Project).where(
                    Project.id == project_id
                ).first()
                if not project:
                    raise ProjectsDoesNotExists(message=f'Project with id: {project_id} does not exists')
                return ProjectEntity(
                    project_id=project.id,
                    andamento_do_projeto=project.andamento_do_projeto,
                    start_date=project.start_date,
                    expected_completion_date=project.expected_completion_date,
                    verba_disponivel=project.verba_disponivel,
                    status_id=project.status_id,
                    end_date=project.end_date,
                    name=project.name
                )
            except Exception as e:
                raise e
    
    ## Refatorar no futuro, para utilizar chunks (pages), carregando um numero determinado de projetos por yield
    def find_all(self) -> List[ProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                projects = db.session.query(Project).all()
                if not projects:
                    raise ProjectsDoesNotExists('Projects does not exists')
                project_list = [
                    ProjectEntity(
                    project_id=project.id,
                    andamento_do_projeto=project.andamento_do_projeto,
                    start_date=project.start_date,
                    expected_completion_date=project.expected_completion_date,
                    verba_disponivel=project.verba_disponivel,
                    status_id=project.status_id,
                    end_date=project.end_date,
                    name=project.name
                    ) for project in projects
                ]
                return project_list
            except Exception as e:
                raise e
    
    def find_by_status(self, status_id:int) -> List[ProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                projects = db.session.query(Project).where(Project.status_id == status_id)
                if not projects:
                    raise ProjectsDoesNotExists(message=f'Projects with status_id: {status_id} does not exists')
                project_list = [
                    ProjectEntity(
                    project_id=project.id,
                    andamento_do_projeto=project.andamento_do_projeto,
                    start_date=project.start_date,
                    expected_completion_date=project.expected_completion_date,
                    verba_disponivel=project.verba_disponivel,
                    status_id=project.status_id,
                    end_date=project.end_date,
                    name=project.name
                    ) for project in projects
                ]
                return project_list
            except Exception as e:
                raise e
    
    def find_by_name(self, name:str) -> ProjectEntity:
        with self.__db_connection_handler as db:
            try:
                project = db.session.query(Project).where(
                    Project.name == name
                ).first()
                if not project:
                    raise ProjectsDoesNotExists(message=f'Project with name: {name}')
                return ProjectEntity(
                    project_id=project.id,
                    andamento_do_projeto=project.andamento_do_projeto,
                    start_date=project.start_date,
                    expected_completion_date=project.expected_completion_date,
                    verba_disponivel=project.verba_disponivel,
                    status_id=project.status_id,
                    end_date=project.end_date,
                    name=project.name
                )
            except Exception as e:
                raise e
        
    def update(self, project_id:int, update_params:Dict) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(Project).where(Project.id == project_id).update(update_params)
                db.session.commit()
            except Exception as e:
                raise e
    
    def delete(self, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(Project).where(Project.id == project_id).delete()
                db.session.commit()
            except Exception as e:
                raise ErrorOnDeleteProject(message=f'Error on delete project: {project_id}: {e}') from e