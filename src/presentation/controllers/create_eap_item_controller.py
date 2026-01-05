from typing import Dict, Any
from datetime import datetime

from src.domain.use_cases.i_create_eap_item import ICreateEAPItem
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_find_eap import IFindEAP
from src.domain.value_objects.eap_code import EAPCode
from src.domain.value_objects.eap_type import EAPType
from src.domain.value_objects.eap_status import EAPStatus
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.eap.eap_not_found_error import EAPNotFoundError
from src.errors.eap.eap_item_not_found_error import EAPItemNotFoundError
from src.errors.eap.invalid_eap_code_error import InvalidEAPCodeError
from src.errors.eap.duplicate_eap_code_error import DuplicateEAPCodeError
from src.errors.eap.budget_exceeded_error import BudgetExceededError
from src.errors.eap.invalid_date_range_error import InvalidDateRangeError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class CreateEAPItemController(ControllerInterface):  # pylint: disable=too-few-public-methods
    """Controller para criação de item da EAP"""
    
    def __init__(self, create_eap_item_case: ICreateEAPItem, create_history_case: ICreateHistoryProject, find_eap_case: IFindEAP):
        self.__create_eap_item_case = create_eap_item_case
        self.__create_history_case = create_history_case
        self.__find_eap_case = find_eap_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:  # pylint: disable=too-many-return-statements,too-many-branches
        """
        Manipula a requisição de criação de item da EAP
        
        Args:
            http_request: Requisição HTTP
            
        Returns:
            HttpResponse: Resposta HTTP
        """
        try:
            body = http_request.body
            
            # Validação dos campos obrigatórios
            required_fields = ["eap_id", "code", "name", "description", "type", "responsible", "start_date", "end_date", "budget"]
            for field in required_fields:
                if field not in body:
                    return HttpResponse(
                        status_code=400,
                        body={"error": f"Campo obrigatório: {field}"}
                    )
            
            # Extrai os dados da requisição
            eap_id = body["eap_id"]
            code = EAPCode(body["code"])
            name = body["name"]
            description = body["description"]
            eap_type = EAPType.from_string(body["type"])
            parent_id = body.get("parent_id")
            responsible = body["responsible"]
            
            # Parseia as datas no formato YYYY-MM-DD ou ISO format
            start_date_str = body["start_date"]
            end_date_str = body["end_date"]
            
            # Se vier no formato YYYY-MM-DD, converte para datetime sem timezone
            if len(start_date_str) == 10:  # Formato: YYYY-MM-DD
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            else:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            
            if len(end_date_str) == 10:  # Formato: YYYY-MM-DD
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            else:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            
            budget = MonetaryValue(body["budget"])
            status = EAPStatus.from_string(body.get("status", "nao_iniciado"))
            progress = body.get("progress", 0)
            
            # Cria o item da EAP
            item = self.__create_eap_item_case.create(
                eap_id=eap_id,
                code=code,
                name=name,
                description=description,
                eap_type=eap_type,
                parent_id=parent_id,
                responsible=responsible,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
                status=status,
                progress=progress
            )
            
            # Registra no histórico do projeto
            try:
                eap = self.__find_eap_case.find_by_id(eap_id)
                if eap and eap.project_id:
                    self.__create_history_case.create(
                        project_id=eap.project_id,
                        data_name="Item EAP",
                        description=f"Item EAP '{name}' (código {code}) criado"
                    )
            except Exception:
                # Se falhar ao criar histórico, não bloqueia a operação principal
                pass
            
            # Converte a entidade para dicionário
            item_data = self._item_to_dict(item)
            
            return HttpResponse(
                status_code=201,
                body={"item": item_data}
            )
            
        except EAPNotFoundError as e:
            return HttpResponse(
                status_code=e.status_code,
                body={"error": e.message}
            )
        except EAPItemNotFoundError as e:
            return HttpResponse(
                status_code=e.status_code,
                body={"error": e.message}
            )
        except InvalidEAPCodeError as e:
            return HttpResponse(
                status_code=e.status_code,
                body={"error": e.message}
            )
        except DuplicateEAPCodeError as e:
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
    
    def _item_to_dict(self, item) -> Dict[str, Any]:
        """Converte um item da EAP para dicionário"""
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