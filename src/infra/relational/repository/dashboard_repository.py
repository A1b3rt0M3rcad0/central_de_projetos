#pylint:disable=not-callable,unused-import
from src.infra.relational.models.project import Project
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.models.user import User
from src.infra.relational.models.types import Types
from src.infra.relational.models.status import Status
from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.eap import EAP, EAPItem
from src.data.interface.i_dashboard_repository import IDashboardRepository
from src.errors.dashboard_errors import ErrorOnGetDashboardData
from sqlalchemy import func
from typing import Dict, Any, List


class DashboardRepository(IDashboardRepository):
    """Repositório otimizado de dashboard com queries SQL otimizadas"""
    
    def __init__(self, db_connection_handler):
        self.__db_connection_handler = db_connection_handler
    
    def get_counts_summary(self, excluded_status: List[int] = None) -> Dict[str, int]:
        """Retorna contagens gerais em uma única query"""
        try:
            
            with self.__db_connection_handler as db:
                # Query unificada para contagens
                total_bairros = db.session.query(func.count(Bairro.id)).scalar()
                total_empresas = db.session.query(func.count(Empresa.id)).scalar()
                total_fiscais = db.session.query(func.count(Fiscal.id)).scalar()
                
                # Contagem de projetos com filtro de status excluídos
                project_query = db.session.query(func.count(Project.id))
                if excluded_status:
                    project_query = project_query.filter(~Project.status_id.in_(excluded_status))
                total_projects = project_query.scalar()
                
                return {
                    'projects': total_projects or 0,
                    'bairros': total_bairros or 0,
                    'empresas': total_empresas or 0,
                    'fiscais': total_fiscais or 0
                }
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get counts summary: {str(exception)}'
            ) from exception
    
    def get_projects_by_bairro(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por bairro"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Bairro.name.label('nome'),
                    func.count(ProjectBairro.project_id).label('quantidade')
                ).join(
                    ProjectBairro, Bairro.id == ProjectBairro.bairro_id
                ).join(
                    Project, ProjectBairro.project_id == Project.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Bairro.name).order_by(func.count(ProjectBairro.project_id).desc())
                
                results = query.all()
                return [{'nome': r.nome, 'quantidade': r.quantidade} for r in results]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by bairro: {str(exception)}'
            ) from exception
    
    def get_budget_by_bairro(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna orçamento por bairro"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Bairro.name.label('nome'),
                    func.sum(Project.verba_disponivel).label('orcamento')
                ).join(
                    ProjectBairro, Bairro.id == ProjectBairro.bairro_id
                ).join(
                    Project, ProjectBairro.project_id == Project.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Bairro.name).order_by(func.sum(Project.verba_disponivel).desc())
                
                results = query.all()
                return [{'nome': r.nome, 'orcamento': float(r.orcamento) if r.orcamento else 0} for r in results]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get budget by bairro: {str(exception)}'
            ) from exception
    
    def get_projects_by_fiscal(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por fiscal"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Fiscal.name.label('nome'),
                    func.count(ProjectFiscal.project_id).label('projetos')
                ).join(
                    ProjectFiscal, Fiscal.id == ProjectFiscal.fiscal_id
                ).join(
                    Project, ProjectFiscal.project_id == Project.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Fiscal.name).order_by(func.count(ProjectFiscal.project_id).desc())
                
                results = query.all()
                return [{'nome': r.nome, 'projetos': r.projetos} for r in results]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by fiscal: {str(exception)}'
            ) from exception
    
    def get_projects_by_empresa(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por empresa"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Empresa.name.label('nome'),
                    func.count(ProjectEmpresa.project_id).label('projetos')
                ).join(
                    ProjectEmpresa, Empresa.id == ProjectEmpresa.empresa_id
                ).join(
                    Project, ProjectEmpresa.project_id == Project.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Empresa.name).order_by(func.count(ProjectEmpresa.project_id).desc())
                
                results = query.all()
                return [{'nome': r.nome, 'projetos': r.projetos} for r in results]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by empresa: {str(exception)}'
            ) from exception
    
    def get_projects_by_user(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por usuário"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    User.name.label('nome'),
                    func.count(UserProject.project_id).label('projetos')
                ).join(
                    UserProject, User.cpf == UserProject.user_cpf
                ).join(
                    Project, UserProject.project_id == Project.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(User.name).order_by(func.count(UserProject.project_id).desc())
                
                results = query.all()
                return [{'nome': r.nome, 'projetos': r.projetos} for r in results]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by user: {str(exception)}'
            ) from exception
    
    def get_all_types(self) -> List[Dict[str, Any]]:
        """Retorna lista de todos os tipos"""
        try:
            with self.__db_connection_handler as db:
                types = db.session.query(Types).all()
                return [
                    {
                        'id': tipo.id,
                        'name': tipo.name,
                        'created_at': tipo.created_at.strftime(r'%d/%m/%Y') if tipo.created_at else None
                    }
                    for tipo in types
                ]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get all types: {str(exception)}'
            ) from exception
    
    def get_projects_by_bairro_and_type(self, excluded_status: List[int] = None) -> Dict[str, Any]:
        """Retorna contagem de projetos por bairro e tipo no formato esperado pelo frontend"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Bairro.id.label('bairro_id'),
                    Bairro.name.label('bairro_name'),
                    Types.name.label('tipo'),
                    func.count(Project.id).label('quantidade')
                ).join(
                    ProjectBairro, Bairro.id == ProjectBairro.bairro_id
                ).join(
                    Project, ProjectBairro.project_id == Project.id
                ).join(
                    ProjectType, Project.id == ProjectType.project_id
                ).join(
                    Types, ProjectType.type_id == Types.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Bairro.id, Bairro.name, Types.name)
                
                results = query.all()
                
                # Estruturar dados no formato esperado: {bairro_id: {bairro_name: {tipo: count}}}
                data = {}
                for r in results:
                    if r.bairro_id not in data:
                        data[r.bairro_id] = {r.bairro_name: {}}
                    
                    # Pegar o nome do bairro (é sempre o mesmo para este ID)
                    bairro_data = list(data[r.bairro_id].values())[0]
                    bairro_data[r.tipo] = r.quantidade
                
                return data
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by bairro and type: {str(exception)}'
            ) from exception
    
    def get_all_bairros(self) -> List[Dict[str, Any]]:
        """Retorna lista de todos os bairros"""
        try:
            with self.__db_connection_handler as db:
                bairros = db.session.query(Bairro).all()
                return [
                    {
                        'id': bairro.id,
                        'name': bairro.name,
                        'created_at': bairro.created_at.strftime(r'%d/%m/%Y') if bairro.created_at else None
                    }
                    for bairro in bairros
                ]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get all bairros: {str(exception)}'
            ) from exception
    
    def get_projects_by_bairro_and_status(self, excluded_status: List[int] = None) -> Dict[str, Any]:
        """Retorna contagem de projetos por bairro e status no formato esperado pelo frontend"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Bairro.id.label('bairro_id'),
                    Bairro.name.label('bairro_name'),
                    Status.description.label('status'),
                    func.count(Project.id).label('quantidade')
                ).join(
                    ProjectBairro, Bairro.id == ProjectBairro.bairro_id
                ).join(
                    Project, ProjectBairro.project_id == Project.id
                ).join(
                    Status, Project.status_id == Status.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Bairro.id, Bairro.name, Status.description)
                
                results = query.all()
                
                # Estruturar dados no formato esperado: {bairro_id: {bairro_name: {status: count}}}
                data = {}
                for r in results:
                    if r.bairro_id not in data:
                        data[r.bairro_id] = {r.bairro_name: {}}
                    
                    # Pegar o nome do bairro (é sempre o mesmo para este ID)
                    bairro_data = list(data[r.bairro_id].values())[0]
                    bairro_data[r.status] = r.quantidade
                
                return data
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by bairro and status: {str(exception)}'
            ) from exception
    
    def get_projects_by_type(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por tipo"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Types.name.label('tipo'),
                    func.count(ProjectType.project_id).label('quantidade')
                ).join(
                    ProjectType, Types.id == ProjectType.type_id
                ).join(
                    Project, ProjectType.project_id == Project.id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Types.name).order_by(func.count(ProjectType.project_id).desc())
                
                results = query.all()
                return [{'tipo': r.tipo, 'quantidade': r.quantidade} for r in results]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by type: {str(exception)}'
            ) from exception
    
    def get_projects_by_status(self, excluded_status: List[int] = None) -> List[Dict[str, Any]]:
        """Retorna contagem de projetos por status"""
        try:
            with self.__db_connection_handler as db:
                query = db.session.query(
                    Status.description.label('status'),
                    func.count(Project.id).label('quantidade')
                ).join(
                    Project, Status.id == Project.status_id
                )
                
                if excluded_status:
                    query = query.filter(~Project.status_id.in_(excluded_status))
                
                query = query.group_by(Status.description).order_by(func.count(Project.id).desc())
                
                results = query.all()
                return [{'status': r.status, 'quantidade': r.quantidade} for r in results]
        except Exception as exception:
            raise ErrorOnGetDashboardData(
                message=f'Error on get projects by status: {str(exception)}'
            ) from exception

