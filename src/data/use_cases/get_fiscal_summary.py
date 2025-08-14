from src.domain.use_cases.i_get_fiscal_summary import IGetFiscalSummary
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from typing import Dict, Any, Optional
from datetime import datetime

class GetFiscalSummary(IGetFiscalSummary):
    
    def __init__(
        self, 
        fiscal_repository: IFiscalRepository,
        project_fiscal_repository: IProjectFiscalRepository,
        work_project_repository: IWorkProjectRepository
    ) -> None:
        self.__fiscal_repository = fiscal_repository
        self.__project_fiscal_repository = project_fiscal_repository
        self.__work_project_repository = work_project_repository
    
    def get_summary(
        self, 
        fiscal_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        try:
            # Buscar dados do fiscal
            fiscal_entity = self.__fiscal_repository.find_by_id(fiscal_id)
            
            # Buscar projetos vinculados
            try:
                projects_linked = self.__project_fiscal_repository.find_all_from_fiscal(fiscal_id)
                total_projetos_vinculados = len(projects_linked)
            except Exception:
                # Se não há projetos vinculados, retorna 0
                total_projetos_vinculados = 0
            
            # Buscar total de fiscalizações
            work_projects_data = self.__work_project_repository.get_work_projects_with_pagination_by_fiscal(
                fiscal_id=fiscal_id,
                page=1,
                page_size=1  # Só precisamos do total
            )
            total_fiscalizacoes = work_projects_data['total']
            
            # Buscar fiscalizações no período
            work_projects_period = self.__work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter(
                fiscal_id=fiscal_id,
                page=1,
                page_size=1,  # Só precisamos do total
                start_date=start_date,
                end_date=end_date
            )
            fiscalizacoes_no_periodo = work_projects_period['total']
            
            # Buscar todas as fiscalizações para calcular distribuição por projeto e última atividade
            all_work_projects = self.__work_project_repository.find_by_fiscal(fiscal_id)
            
            # Calcular última atividade (mais recente entre created_at e updated_at)
            last_activity_at = None
            documentos_enviados = 0
            
            for wp in all_work_projects:
                # Atualizar última atividade - usar o mais recente entre created_at e updated_at
                wp_activity = wp.updated_at if wp.updated_at else wp.created_at
                if wp_activity:
                    if not last_activity_at or wp_activity > last_activity_at:
                        last_activity_at = wp_activity
                
                # Contar documentos
                if wp.photo_name:
                    documentos_enviados += 1
                if wp.additional_documents:
                    documentos_enviados += len(wp.additional_documents)
            
            # Buscar últimas fiscalizações (limitado pelo parâmetro limit) para exibição - SEM filtro de data
            latest_work_projects = self.__work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter(
                fiscal_id=fiscal_id,
                page=1,
                page_size=limit,
                start_date=None,  # Sem filtro de data para mostrar as últimas gerais
                end_date=None
            )
            
            # Processar últimas fiscalizações para exibição
            ultimas_fiscalizacoes = []
            
            for wp in latest_work_projects['data']:
                ultimas_fiscalizacoes.append({
                    'id': wp.id,
                    'title': wp.title,
                    'project_id': wp.project.project_id if wp.project else None,
                    'project_name': wp.project.name if wp.project else None,
                    'created_at': wp.created_at.strftime(r'%d/%m/%Y %H:%M:%S') if wp.created_at else None
                })
            
            # Buscar todas as fiscalizações para calcular distribuição por projeto
            all_work_projects = self.__work_project_repository.find_by_fiscal(fiscal_id)
            
            # Calcular distribuição por projeto
            fiscalizacoes_por_projeto = {}
            for wp in all_work_projects:
                project_id = wp.project.project_id if wp.project else None
                project_name = wp.project.name if wp.project else None
                
                if project_id not in fiscalizacoes_por_projeto:
                    fiscalizacoes_por_projeto[project_id] = {
                        'project_id': project_id,
                        'project_name': project_name,
                        'count': 0
                    }
                fiscalizacoes_por_projeto[project_id]['count'] += 1
            
            # Converter para lista e ordenar por count
            fiscalizacoes_por_projeto_list = list(fiscalizacoes_por_projeto.values())
            fiscalizacoes_por_projeto_list.sort(key=lambda x: x['count'], reverse=True)
            
            return {
                'fiscal': {
                    'id': fiscal_entity.fiscal_id,
                    'name': fiscal_entity.name,
                    'email': fiscal_entity.email,
                    'phone': fiscal_entity.phone
                },
                'total_projetos_vinculados': total_projetos_vinculados,
                'total_fiscalizacoes': total_fiscalizacoes,
                'fiscalizacoes_no_periodo': fiscalizacoes_no_periodo,
                'last_activity_at': last_activity_at.strftime(r'%d/%m/%Y %H:%M:%S') if last_activity_at else None,
                'fiscalizacoes_por_projeto': fiscalizacoes_por_projeto_list,
                'ultimas_fiscalizacoes': ultimas_fiscalizacoes,
                'documentos_enviados': documentos_enviados
            }
        except Exception as e:
            raise e from e 