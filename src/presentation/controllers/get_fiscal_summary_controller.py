#pylint:disable=all
from src.domain.use_cases.i_get_fiscal_summary import IGetFiscalSummary
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from datetime import datetime
from typing import Optional

class GetFiscalSummaryController(ControllerInterface):

    def __init__(self, get_fiscal_summary: IGetFiscalSummary) -> None:
        self.__get_fiscal_summary = get_fiscal_summary
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            # Obter dados do body (injetado pela rota)
            body = http_request.body or {}
            query_params = http_request.query_params or {}
            
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
            
            # Obter limit das query params
            limit = query_params.get('limit', 5)
            try:
                limit = int(limit)
                if limit < 1:
                    limit = 5
            except (ValueError, TypeError):
                limit = 5
            
            result = self.__get_fiscal_summary.get_summary(
                fiscal_id=fiscal_id,
                start_date=start_date,
                end_date=end_date,
                limit=limit
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal Summary Retrieved Successfully',
                    'fiscal_id': fiscal_id,
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None,
                    'content': result
                }
            )
        except Exception as e:
            raise e from e 