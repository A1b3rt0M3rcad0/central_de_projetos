from typing import Dict, Any
from datetime import datetime

from src.domain.use_cases.i_update_eap_item import IUpdateEAPItem
from src.domain.value_objects.eap_status import EAPStatus
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.eap.eap_item_not_found_error import EAPItemNotFoundError
from src.errors.eap.invalid_status_transition_error import InvalidStatusTransitionError
from src.errors.eap.budget_exceeded_error import BudgetExceededError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class UpdateEAPItemController(ControllerInterface):
    """Controller para atualização de item da EAP"""
    
    def __init__(self, update_eap_item_case: IUpdateEAPItem):
        self.__update_eap_item_case = update_eap_item_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Manipula a requisição de atualização de item da EAP
        
        Args:
            http_request: Requisição HTTP
            
        Returns:
            HttpResponse: Resposta HTTP
        """
        try:
            body = http_request.body
            path_params = http_request.path_params
            
            # Extrai o ID do item dos path params
            item_id = int(path_params.get("item_id"))
            
            # Extrai os dados opcionais da requisição
            name = body.get("name")
            description = body.get("description")
            responsible = body.get("responsible")
            start_date = body.get("start_date")
            end_date = body.get("end_date")
            budget_value = body.get("budget")
            status_value = body.get("status")
            progress = body.get("progress")
            
            # Converte datas se fornecidas
            if start_date:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if end_date:
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            
            # Converte budget para MonetaryValue se fornecido
            budget = MonetaryValue(float(budget_value)) if budget_value is not None else None
            
            # Converte status para EAPStatus se fornecido
            status = EAPStatus.from_string(status_value) if status_value is not None else None
            
            # Atualiza o item
            item = self.__update_eap_item_case.update(
                item_id=item_id,
                name=name,
                description=description,
                responsible=responsible,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
                status=status,
                progress=progress
            )
            
            # Converte a entidade para dicionário
            item_data = self._entity_to_dict(item)
            
            return HttpResponse(
                status_code=200,
                body={"item": item_data}
            )
            
        except EAPItemNotFoundError as e:
            return HttpResponse(
                status_code=e.status_code,
                body={"error": e.message}
            )
        except InvalidStatusTransitionError as e:
            return HttpResponse(
                status_code=e.status_code,
                body={"error": e.message}
            )
        except BudgetExceededError as e:
            return HttpResponse(
                status_code=e.status_code,
                body={"error": e.message}
            )
        except ValueError as e:
            return HttpResponse(
                status_code=400,
                body={"error": str(e)}
            )
        except Exception as e:
            return HttpResponse(
                status_code=500,
                body={"error": "Erro interno do servidor"}
            )
    
    def _entity_to_dict(self, item) -> Dict[str, Any]:
        """Converte uma entidade de item EAP para dicionário"""
        return {
            "id": item.id,
            "eap_id": item.eap_id,
            "code": str(item.code),
            "name": item.name,
            "description": item.description,
            "type": item.type.value,
            "parent_id": item.parent_id,
            "responsible": item.responsible,
            "start_date": item.start_date.isoformat() if item.start_date else None,
            "end_date": item.end_date.isoformat() if item.end_date else None,
            "budget": float(item.budget.value),
            "status": item.status.value,
            "progress": item.progress,
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None
        }

