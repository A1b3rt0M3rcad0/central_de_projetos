#pylint:disable=W0611,R0912,R0915
from src.data.interface.i_project_repository import IProjectRepository
from typing import Optional, List, Dict, Union
from src.domain.value_objects.monetary_value import MonetaryValue
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from datetime import datetime
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import or_

from src.domain.entities.project import ProjectEntity
from src.domain.entities.bairro import BairroEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.empresa import EmpresaEntity
from src.domain.entities.types import TypesEntity
from src.domain.entities.status import StatusEntity
from src.domain.entities.history_project import HistoryProjectEntity
from src.domain.entities.user import UserEntity
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role

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
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.user import User

# Import additional models to ensure SQLAlchemy can resolve relationships
# These imports are necessary for SQLAlchemy to properly configure relationships
# pylint: disable=unused-import
from src.infra.relational.models.refresh_token import RefreshToken
from src.infra.relational.models.work_project import WorkProject
from src.infra.relational.models.eap import EAP, EAPItem

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
                project = db.session.query(Project).options(
                    joinedload(Project.status),
                    joinedload(Project.project_bairros).joinedload(ProjectBairro.bairro),
                    joinedload(Project.project_empresas).joinedload(ProjectEmpresa.empresa)
                ).where(
                    Project.id == project_id
                ).first()
                if not project:
                    raise ProjectNotExists(message=f'Project with id: {project_id} does not exists')
                
                return ProjectEntity(
                    project_id=project.id,
                    andamento_do_projeto=project.andamento_do_projeto,
                    start_date=project.start_date,
                    expected_completion_date=project.expected_completion_date,
                    verba_disponivel=MonetaryValue(project.verba_disponivel),
                    status_id=project.status_id,
                    end_date=project.end_date,
                    name=project.name,
                    status=StatusEntity(
                        status_id=project.status.id,
                        description=project.status.description,
                        created_at=project.status.created_at
                    ) if project.status else None,
                    bairro=BairroEntity(
                        bairro_id=project.project_bairros[0].bairro.id,
                        name=project.project_bairros[0].bairro.name,
                        created_at=project.project_bairros[0].bairro.created_at
                    ) if project.project_bairros and len(project.project_bairros) > 0 else None,
                    empresa=EmpresaEntity(
                        empresa_id=project.project_empresas[0].empresa.id,
                        name=project.project_empresas[0].empresa.name,
                        created_at=project.project_empresas[0].empresa.created_at
                    ) if project.project_empresas and len(project.project_empresas) > 0 else None
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
    
    def count_projects(self) -> Dict[str, int]:
        try:
            with self.__db_connection_handler as db:
                projects:List[Project] = db.session.query(Project).all()
                return {
                    "projects": len(projects)
                }
        except Exception as e:
            raise ErrorOnFindProject(
                    message=f'Error on count projects: {str(e)}'
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
                
                project = db.session.query(Project).where(
                    Project.id == project_id
                ).first()
                if not project:
                    raise ProjectNotExists(message=f'Project with id: {project_id} does not exists')
                
                project_fiscals:List[ProjectFiscal] = db.session.query(ProjectFiscal).where(ProjectFiscal.project_id == project_id ).all()
                project_empresas:List[ProjectEmpresa] = db.session.query(ProjectEmpresa).where(ProjectEmpresa.project_id == project_id ).all()
                project_bairros:List[ProjectBairro] = db.session.query(ProjectBairro).where(ProjectBairro.project_id == project_id ).all()
                project_types_list:List[ProjectType] = db.session.query(ProjectType).where(ProjectType.project_id == project_id ).all()
                history_project:HistoryProject = db.session.query(HistoryProject).where(HistoryProject.project_id == project_id).all()

                status_entity = None
                fiscal_entity = None
                empresa_entity = None
                bairro_entity = None
                types_entity = None
                history_project_list_entity = None

                if project is not None:
                    status:Status = db.session.query(Status).where(Status.id == project.status_id).first()
                    status_entity = StatusEntity(
                        status_id=status.id,
                        description=status.description,
                        created_at=status.created_at
                    )
                
                # Buscar fiscais associados ao projeto
                if project_fiscals:
                    if len(project_fiscals) == 1:
                        # Se há apenas um fiscal, manter compatibilidade com código existente
                        fiscal:Fiscal = db.session.query(Fiscal).where(Fiscal.id == project_fiscals[0].fiscal_id).first()
                        if fiscal:
                            fiscal_entity = FiscalEntity(
                                fiscal_id=fiscal.id,
                                name=fiscal.name,
                                created_at=fiscal.created_at
                            )
                    else:
                        # Se há múltiplos fiscais, criar lista
                        fiscal_entities = []
                        for project_fiscal in project_fiscals:
                            fiscal:Fiscal = db.session.query(Fiscal).where(Fiscal.id == project_fiscal.fiscal_id).first()
                            if fiscal:
                                fiscal_entities.append(FiscalEntity(
                                    fiscal_id=fiscal.id,
                                    name=fiscal.name,
                                    created_at=fiscal.created_at
                                ))
                        fiscal_entity = fiscal_entities
                
                # Buscar empresas associadas ao projeto
                if project_empresas:
                    if len(project_empresas) == 1:
                        # Se há apenas uma empresa, manter compatibilidade com código existente
                        empresa:Empresa = db.session.query(Empresa).where(Empresa.id == project_empresas[0].empresa_id).first()
                        if empresa:
                            empresa_entity = EmpresaEntity(
                                empresa_id=empresa.id,
                                name=empresa.name,
                                created_at=empresa.created_at
                            )
                    else:
                        # Se há múltiplas empresas, criar lista
                        empresa_entities = []
                        for project_empresa in project_empresas:
                            empresa:Empresa = db.session.query(Empresa).where(Empresa.id == project_empresa.empresa_id).first()
                            if empresa:
                                empresa_entities.append(EmpresaEntity(
                                    empresa_id=empresa.id,
                                    name=empresa.name,
                                    created_at=empresa.created_at
                                ))
                        empresa_entity = empresa_entities
                
                # Buscar bairros associados ao projeto
                if project_bairros:
                    if len(project_bairros) == 1:
                        # Se há apenas um bairro, manter compatibilidade com código existente
                        bairro:Bairro = db.session.query(Bairro).where(Bairro.id == project_bairros[0].bairro_id).first()
                        if bairro:
                            bairro_entity = BairroEntity(
                                bairro_id=bairro.id,
                                name=bairro.name,
                                created_at=bairro.created_at
                            )
                    else:
                        # Se há múltiplos bairros, criar lista
                        bairro_entities = []
                        for project_bairro in project_bairros:
                            bairro:Bairro = db.session.query(Bairro).where(Bairro.id == project_bairro.bairro_id).first()
                            if bairro:
                                bairro_entities.append(BairroEntity(
                                    bairro_id=bairro.id,
                                    name=bairro.name,
                                    created_at=bairro.created_at
                                ))
                        bairro_entity = bairro_entities
                
                # Buscar tipos associados ao projeto
                if project_types_list:
                    if len(project_types_list) == 1:
                        # Se há apenas um tipo, manter compatibilidade com código existente
                        types:Types = db.session.query(Types).where(Types.id == project_types_list[0].type_id).first()
                        if types:
                            types_entity = TypesEntity(
                                types_id=types.id,
                                name=types.name,
                                created_at=types.created_at
                            )
                    else:
                        # Se há múltiplos tipos, criar lista
                        types_entities = []
                        for project_type in project_types_list:
                            types:Types = db.session.query(Types).where(Types.id == project_type.type_id).first()
                            if types:
                                types_entities.append(TypesEntity(
                                    types_id=types.id,
                                    name=types.name,
                                    created_at=types.created_at
                                ))
                        types_entity = types_entities
                
                if history_project is not None:
                    history_project:HistoryProject = db.session.query(HistoryProject).where(HistoryProject.project_id == project.id).all()
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
                    message=f'Error on find project by id={project_id}: {e}'
                ) from e
    
    def find_all_projects_with_basic_details(self) -> List[ProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                projects = db.session.query(Project).all()
                if not projects:
                    raise ProjectNotExists(message='Projects do not exist')

                project_entities = []
                for project in projects:
                    status_entity = None
                    empresa_entity = None
                    fiscal_entity = None
                    bairro_entity = None
                    types_entity = None

                    status: Status = db.session.query(Status).where(Status.id == project.status_id).first()
                    if status:
                        status_entity = StatusEntity(
                            status_id=status.id,
                            description=status.description,
                            created_at=status.created_at
                        )

                    project_empresa = db.session.query(ProjectEmpresa).where(ProjectEmpresa.project_id == project.id).first()
                    if project_empresa:
                        empresa = db.session.query(Empresa).where(Empresa.id == project_empresa.empresa_id).first()
                        if empresa:
                            empresa_entity = EmpresaEntity(
                                empresa_id=empresa.id,
                                name=empresa.name,
                                created_at=empresa.created_at
                            )

                    project_fiscal = db.session.query(ProjectFiscal).where(ProjectFiscal.project_id == project.id).first()
                    if project_fiscal:
                        fiscal = db.session.query(Fiscal).where(Fiscal.id == project_fiscal.fiscal_id).first()
                        if fiscal:
                            fiscal_entity = FiscalEntity(
                                fiscal_id=fiscal.id,
                                name=fiscal.name,
                                created_at=fiscal.created_at
                            )

                    project_bairro = db.session.query(ProjectBairro).where(ProjectBairro.project_id == project.id).first()
                    if project_bairro:
                        bairro = db.session.query(Bairro).where(Bairro.id == project_bairro.bairro_id).first()
                        if bairro:
                            bairro_entity = BairroEntity(
                                bairro_id=bairro.id,
                                name=bairro.name,
                                created_at=bairro.created_at
                            )

                    project_type = db.session.query(ProjectType).where(ProjectType.project_id == project.id).first()
                    if project_type:
                        types = db.session.query(Types).where(Types.id == project_type.type_id).first()
                        if types:
                            types_entity = TypesEntity(
                                types_id=types.id,
                                name=types.name,
                                created_at=types.created_at
                            )

                    project_entity = ProjectEntity(
                        project_id=project.id,
                        andamento_do_projeto=project.andamento_do_projeto,
                        start_date=project.start_date,
                        expected_completion_date=project.expected_completion_date,
                        end_date=project.end_date,
                        name=project.name,
                        verba_disponivel=project.verba_disponivel,
                        status_id=project.status_id,
                        status=status_entity,
                        empresa=empresa_entity,
                        fiscal=fiscal_entity,
                        bairro=bairro_entity,
                        types=types_entity
                    )

                    project_entities.append(project_entity)

                return project_entities

            except ProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on find all projects with basic details: {e}'
                ) from e
    
    def get_projects_with_pagination(self, page:int, page_size:int) -> Dict[str, Union[int, ProjectEntity]]:
        with self.__db_connection_handler as db:
            try:
                query = db.session.query(Project)
                total = query.count()
                total_pages = (total + page_size - 1) // page_size
                offset = (page - 1) * page_size
                projects:List[Project] = query.offset(offset).limit(page_size).all()
                project_entities = [ProjectEntity(
                    project_id=p.id,
                    verba_disponivel=MonetaryValue(p.verba_disponivel),
                    andamento_do_projeto=p.andamento_do_projeto,
                    expected_completion_date=p.expected_completion_date,
                    start_date=p.start_date,
                    end_date=p.end_date,
                    status_id=p.status_id,
                    name=p.name,
                    bairro=(
                        BairroEntity(
                            bairro_id=p.project_bairros[0].bairro.id,
                            name=p.project_bairros[0].bairro.name,
                            created_at=p.project_bairros[0].bairro.created_at
                        ) if p.project_bairros and len(p.project_bairros) > 0 else None
                    ),
                    empresa=(
                        EmpresaEntity(
                            empresa_id=p.project_empresas[0].empresa.id,
                            name=p.project_empresas[0].empresa.name,
                            created_at=p.project_empresas[0].empresa.created_at
                        ) if p.project_empresas and len(p.project_empresas) > 0 else None
                    ),
                    fiscal=(
                        FiscalEntity(
                            fiscal_id=p.project_fiscals[0].fiscal.id,
                            name=p.project_fiscals[0].fiscal.name,
                            created_at=p.project_fiscals[0].fiscal.created_at
                        ) if p.project_fiscals and len(p.project_fiscals) > 0 else None
                    ),
                    types=(
                        TypesEntity(
                            types_id=p.project_types[0].types.id,
                            name=p.project_types[0].types.name,
                            created_at=p.project_types[0].types.created_at
                        ) if p.project_types and len(p.project_types) > 0 else None
                    ),
                    status=(
                        StatusEntity(
                            status_id=p.status.id,
                            description=p.status.description,
                            created_at=p.status.created_at
                        ) if p.status else None
                    )
                ) for p in projects]

                return {
                    "page": page,
                    "page_size": page_size,
                    "total_items": total,
                    "total_pages": total_pages,
                    "projects": project_entities
                }
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on get projects from page: {page}: {str(e)}'
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

    def get_projects_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[ProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                offset = (page - 1) * page_size
                query = db.session.query(Project).options(
                    joinedload(Project.project_bairros).joinedload(ProjectBairro.bairro),
                    joinedload(Project.project_empresas).joinedload(ProjectEmpresa.empresa),
                    joinedload(Project.project_fiscals).joinedload(ProjectFiscal.fiscal),
                    joinedload(Project.project_types).joinedload(ProjectType.types),
                    joinedload(Project.user_projects).joinedload(UserProject.user),
                    joinedload(Project.status)
                )
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(
                        or_(
                            Project.name.ilike(search_filter),
                            Project.andamento_do_projeto.ilike(search_filter)
                        )
                    )
                
                projects = query.offset(offset).limit(page_size).all()
                
                project_entities = []
                for p in projects:
                    project_entities.append(ProjectEntity(
                        project_id=p.id,
                        verba_disponivel=MonetaryValue(p.verba_disponivel),
                        andamento_do_projeto=p.andamento_do_projeto,
                        expected_completion_date=p.expected_completion_date,
                        start_date=p.start_date,
                        end_date=p.end_date,
                        status_id=p.status_id,
                        name=p.name,
                        bairro=(
                            BairroEntity(
                                bairro_id=p.project_bairros[0].bairro.id,
                                name=p.project_bairros[0].bairro.name,
                                created_at=p.project_bairros[0].bairro.created_at
                            ) if p.project_bairros and len(p.project_bairros) > 0 else None
                        ),
                        empresa=(
                            EmpresaEntity(
                                empresa_id=p.project_empresas[0].empresa.id,
                                name=p.project_empresas[0].empresa.name,
                                created_at=p.project_empresas[0].empresa.created_at
                            ) if p.project_empresas and len(p.project_empresas) > 0 else None
                        ),
                        fiscal=(
                            FiscalEntity(
                                fiscal_id=p.project_fiscals[0].fiscal.id,
                                name=p.project_fiscals[0].fiscal.name,
                                created_at=p.project_fiscals[0].fiscal.created_at
                            ) if p.project_fiscals and len(p.project_fiscals) > 0 else None
                        ),
                        types=(
                            TypesEntity(
                                types_id=p.project_types[0].types.id,
                                name=p.project_types[0].types.name,
                                created_at=p.project_types[0].types.created_at
                            ) if p.project_types and len(p.project_types) > 0 else None
                        ),
                        status=(
                            StatusEntity(
                                status_id=p.status.id,
                                description=p.status.description,
                                created_at=p.status.created_at
                            ) if p.status else None
                        )
                    ))
                
                return project_entities
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on get projects with pagination and filter: {str(e)}'
                ) from e

    def count_projects_with_filter(self, search_term: str = None) -> int:
        with self.__db_connection_handler as db:
            try:
                query = db.session.query(Project)
                
                # Aplicar filtro de busca se fornecido
                if search_term and search_term.strip():
                    search_filter = f"%{search_term.strip()}%"
                    query = query.filter(
                        or_(
                            Project.name.ilike(search_filter),
                            Project.andamento_do_projeto.ilike(search_filter)
                        )
                    )
                
                count = query.count()
                return count
            except Exception as e:
                raise ErrorOnFindProject(
                    message=f'Error on count projects with filter: {str(e)}'
                ) from e