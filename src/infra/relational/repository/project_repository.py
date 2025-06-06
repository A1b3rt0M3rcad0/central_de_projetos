#pylint:disable=W0611
from src.data.interface.i_project_repository import IProjectRepository
from typing import Optional, List, Dict
from src.domain.value_objects.monetary_value import MonetaryValue
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from datetime import datetime
from sqlalchemy.orm import joinedload, subqueryload

from src.domain.entities.project import ProjectEntity
from src.domain.entities.bairro import BairroEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.empresa import EmpresaEntity
from src.domain.entities.types import TypesEntity
from src.domain.entities.status import StatusEntity
from src.domain.entities.history_project import HistoryProjectEntity

from src.infra.relational.models.project import Project
from src.infra.relational.models.status import Status
from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.models.types import Types

# Errors
from src.errors.repository.not_exists_error.projects_does_not_exists import ProjectNotExists
from src.errors.repository.already_exists_error.project_already_exists import ProjectAlreadyExists
from src.errors.repository.error_on_delete.error_on_delete_project import ErrorOnDeleteProject
from src.errors.repository.error_on_insert.error_on_insert_project import ErrorOnInsertProject
from src.errors.repository.error_on_find.error_on_find_project import ErrorOnFindProject
from src.errors.repository.error_on_update.error_on_update_project import ErrorOnUpdateProject
from src.errors.repository.has_related_children.project_has_related_children import ProjectHasRelatedChildren
from sqlalchemy.exc import IntegrityError

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
            except IntegrityError as e:
                raise ProjectAlreadyExists(
                    message=f'Project project status_id={status_id}, name={name} already exists: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnInsertProject(
                    message=f'Error on insert project status_id={status_id}, name={name}: {str(e)}'
                ) from e
    
    def find(self, project_id:int) -> ProjectEntity:
        with self.__db_connection_handler as db:
            try:
                project = db.session.query(Project).where(
                    Project.id == project_id
                ).first()
                if not project:
                    raise ProjectNotExists(message=f'Project with id: {project_id} does not exists')
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
            except ProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on find project project_id={project_id}: {str(e)}'
                ) from e
    
    def find_all(self) -> List[ProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                projects = db.session.query(Project).all()
                if not projects:
                    raise ProjectNotExists('Projects does not exists')
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
            except ProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on find all projects: {str(e)}'
                ) from e
    
    def find_by_status(self, status_id:int) -> List[ProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                projects = db.session.query(Project).where(Project.status_id == status_id)
                if not projects:
                    raise ProjectNotExists(message=f'Projects with status_id: {status_id} does not exists')
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
            except ProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on find project by status status_id={status_id}: {str(e)}'
                ) from e
    
    def find_by_name(self, name:str) -> ProjectEntity:
        with self.__db_connection_handler as db:
            try:
                project = db.session.query(Project).where(
                    Project.name == name
                ).first()
                if not project:
                    raise ProjectNotExists(message=f'Project with name: {name}')
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
            except ProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on find project by name name={name}: {str(e)}'
                ) from e
    
    def find_all_from_project(self, project_id:int) -> ProjectEntity:
        with self.__db_connection_handler as db:
            try:
                project:Project = db.session.query(Project).where(Project.id == project_id).first()
                status:Status = db.session.query(Status).where(Status.id == project.status_id).first()
                project_fiscal:ProjectFiscal = db.session.query(ProjectFiscal).where(ProjectFiscal.project_id == project_id ).first()
                project_empresa:ProjectEmpresa = db.session.query(ProjectEmpresa).where(ProjectEmpresa.project_id == project_id ).first()
                project_bairro:ProjectBairro = db.session.query(ProjectBairro).where(ProjectBairro.project_id == project_id ).first()
                project_types:ProjectType = db.session.query(ProjectType).where(ProjectType.project_id == project_id ).first()
                history_project:HistoryProject = db.session.query(HistoryProject).where(HistoryProject.project_id == project).all()

                status_entity = None
                fiscal_entity = None
                empresa_entity = None
                bairro_entity = None
                types_entity = None
                history_project_list_entity = None

                if status is not None:
                    status_entity = StatusEntity(
                        status_id=status.id,
                        description=status.description,
                        created_at=status.created_at
                    )
                if project_fiscal is not None:
                    fiscal = db.session.query(Fiscal).where(Fiscal.id == project_fiscal.fiscal_id).first()
                    fiscal_entity = FiscalEntity(
                        fiscal_id=fiscal.id,
                        name=fiscal.name,
                        created_at=fiscal.created_at
                    )
                
                if project_empresa is not None:
                    empresa = db.session.query(Empresa).where(Empresa.id == project_empresa.empresa_id).first()
                    empresa_entity = EmpresaEntity(
                        empresa_id=empresa.id,
                        name=empresa.name,
                        created_at=empresa.created_at
                    )
                
                if project_bairro is not None:
                    bairro = db.session.query(Bairro).where(Bairro.id == project_bairro.bairro_id).first()
                    bairro_entity = BairroEntity(
                        bairro_id=bairro.id,
                        name=bairro.name,
                        created_at=bairro.created_at
                    )
                
                if project_types is not None:
                    types = db.session.query(Types).where(Types.id == project_types.type_id).first()
                    types_entity = TypesEntity(
                        types_id=types.id,
                        name=types.name,
                        created_at=types.created_at
                    )
                
                if history_project is not None:
                    history_project = db.session.query(HistoryProject).where(HistoryProject.project_id == project.id).all()
                    history_project_list_entity = [
                        HistoryProjectEntity(
                            history_project_id=history.id,
                            project_id=history.project_id,
                            description=history.description,
                            data_name=history.data_name,
                            updated_at=history.updated_at
                        )
                        for history in history_project
                    ]
                
                return ProjectEntity(
                    project_id=project.id,
                    andamento_do_projeto=project.andamento_do_projeto,
                    expected_completion_date=project.expected_completion_date,
                    end_date=project.end_date,
                    bairro=bairro_entity,
                    empresa=empresa_entity,
                    fiscal=fiscal_entity,
                    history_project=history_project_list_entity,
                    name=project.name,
                    start_date=project.start_date,
                    status=status_entity,
                    verba_disponivel=project.verba_disponivel,
                    status_id=project.status_id,
                    types=types_entity
                )
            
            except ProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on find project by id={id}: {str(e)}'
                ) from e
        
    def update(self, project_id:int, update_params:Dict) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(Project).where(Project.id == project_id).update(update_params)
                db.session.commit()
            except IntegrityError as e:
                raise ProjectAlreadyExists(
                    message=f'project project_id={project_id} with {update_params} already exists: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnUpdateProject(
                    message=f'Error on update project project_id={project_id}: {str(e)}'
                ) from e
    
    def delete(self, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                project = db.session.query(Project).where(Project.id == project_id).first()
                if not project:
                    raise ProjectNotExists(
                        message=f'Project project_id={project_id} not exists'
                    )
                db.session.query(Project).where(Project.id == project_id).delete()
                db.session.commit()
            except ProjectNotExists as e:
                raise e from e
            except IntegrityError as e:
                raise ProjectHasRelatedChildren(
                    message=f'Project project_id={project_id} has related children: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnDeleteProject(message=f'Error on delete project: {project_id}: {str(e)}') from e