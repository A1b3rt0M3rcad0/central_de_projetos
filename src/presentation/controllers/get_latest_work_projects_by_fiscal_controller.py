#pylint:disable=W0611
from src.domain.use_cases.i_get_latest_work_projects_by_fiscal import IGetLatestWorkProjectsByFiscal
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from datetime import datetime
from typing import Optional

class GetLatestWorkProjectsByFiscalController(ControllerInterface):

    def __init__(self, get_latest_work_projects_by_fiscal_case: IGetLatestWorkProjectsByFiscal) -> None:
        self.__get_latest_work_projects_by_fiscal_case = get_latest_work_projects_by_fiscal_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            # Obter dados do path_params e body
            path_params = http_request.path_params or {}
            body = http_request.body or {}
            query_params = http_request.query_params or {}
            
            # Dados da paginação
            page = int(path_params.get('page'))
            page_size = int(path_params.get('page_size'))
            
            # Obter fiscal_id do body (injetado pela rota)
            fiscal_id = body.get('fiscal_id')
            
            if not fiscal_id:
                return HttpResponse(
                    status_code=400,
                    body={'error': 'fiscal_id is required'}
                )
            
            # Processar filtros de data opcionais
            start_date = None
            end_date = None
            
            start_date_str = query_params.get('start_date')
            end_date_str = query_params.get('end_date')
            
            if start_date_str:
                try:
                    start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                except ValueError:
                    return HttpResponse(
                        status_code=400,
                        body={'error': 'start_date must be in ISO format (YYYY-MM-DDTHH:MM:SS)'}
                    )
            
            if end_date_str:
                try:
                    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                except ValueError:
                    return HttpResponse(
                        status_code=400,
                        body={'error': 'end_date must be in ISO format (YYYY-MM-DDTHH:MM:SS)'}
                    )
            
            result = self.__get_latest_work_projects_by_fiscal_case.get_latest_by_fiscal(
                fiscal_id=fiscal_id,
                page=page,
                page_size=page_size,
                start_date=start_date,
                end_date=end_date
            )
            
            work_projects_data = []
            for work_project in result['data']:
                work_project_data = {
                    'id': work_project.id,
                    'project_id': work_project.project_id,
                    'fiscal_id': work_project.fiscal_id,
                    'title': work_project.title,
                    'description': work_project.description,
                    'photo_name': work_project.photo_name,
                    'additional_documents': work_project.additional_documents,
                    'created_at': work_project.created_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.created_at else work_project.created_at,
                    'updated_at': work_project.updated_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.updated_at else work_project.updated_at,
                    'fiscal': {
                        'id': work_project.fiscal.fiscal_id,
                        'name': work_project.fiscal.name,
                        'created_at': work_project.fiscal.created_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.fiscal.created_at else work_project.fiscal.created_at
                    } if work_project.fiscal else None,
                    'project': {
                        'id': work_project.project.project_id,
                        'status_id': work_project.project.status_id,
                        'name': work_project.project.name,
                        'andamento_do_projeto': work_project.project.andamento_do_projeto,
                        'verba_disponivel': float(work_project.project.verba_disponivel.value) if work_project.project.verba_disponivel else None,
                        'start_date': work_project.project.start_date.strftime(r'%d/%m/%Y') if work_project.project.start_date else work_project.project.start_date,
                        'expected_completion_date': work_project.project.expected_completion_date.strftime(r'%d/%m/%Y') if work_project.project.expected_completion_date else work_project.project.expected_completion_date,
                        'end_date': work_project.project.end_date.strftime(r'%d/%m/%Y') if work_project.project.end_date else work_project.project.end_date
                    } if work_project.project else None
                }
                work_projects_data.append(work_project_data)
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Latest Work Projects Founded',
                    'total': result['total'],
                    'page': page,
                    'page_size': page_size,
                    'fiscal_id': fiscal_id,
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None,
                    'content': work_projects_data
                }
            )
        except Exception as e:
            raise e from e 