from typing import Dict, Any
from datetime import datetime

from src.domain.use_cases.i_update_eap_item import IUpdateEAPItem
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_find_eap import IFindEAP
from src.domain.value_objects.eap_status import EAPStatus
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.eap.eap_item_not_found_error import EAPItemNotFoundError
from src.errors.eap.invalid_status_transition_error import InvalidStatusTransitionError
from src.errors.eap.budget_exceeded_error import BudgetExceededError
from src.errors.eap.invalid_date_range_error import InvalidDateRangeError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class UpdateEAPItemController(ControllerInterface):  # pylint: disable=too-few-public-methods
    """Controller para atualização de item da EAP"""
    
    def __init__(self, update_eap_item_case: IUpdateEAPItem, create_history_case: ICreateHistoryProject, find_eap_case: IFindEAP):
        self.__update_eap_item_case = update_eap_item_case
        self.__create_history_case = create_history_case
        self.__find_eap_case = find_eap_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:  # pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
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
            start_date_str = body.get("start_date")
            end_date_str = body.get("end_date")
            budget_value = body.get("budget")
            status_value = body.get("status")
            progress = body.get("progress")
            
            # Converte datas se fornecidas
            start_date = None
            end_date = None
            
            if start_date_str:
                # Se vier no formato YYYY-MM-DD, converte para datetime sem timezone
                if len(start_date_str) == 10:  # Formato: YYYY-MM-DD
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                else:
                    start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            
            if end_date_str:
                # Se vier no formato YYYY-MM-DD, converte para datetime sem timezone
                if len(end_date_str) == 10:  # Formato: YYYY-MM-DD
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                else:
                    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            
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
            
            # Registra no histórico do projeto
            try:
                eap = self.__find_eap_case.find_by_id(item.eap_id)
                if eap and eap.project_id:
                    # Monta descrição com campos alterados
                    changes = []
                    if name: changes.append(f"nome para '{name}'")
                    if status: changes.append(f"status para '{status.value}'")
                    if progress is not None: changes.append(f"progresso para {progress}%")
                    if budget: changes.append(f"orçamento para R$ {float(budget.value):.2f}")
                    
                    changes_text = ", ".join(changes) if changes else "atualizado"
                    self.__create_history_case.create(
                        project_id=eap.project_id,
                        data_name="Item EAP",
                        description=f"Item EAP '{item.name}' (código {item.code}) {changes_text}"
                    )
            except Exception:
                # Se falhar ao criar histórico, não bloqueia a operação principal
                pass
            
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
        except InvalidDateRangeError as e:
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

