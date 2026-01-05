from typing import Dict, Any

from src.domain.use_cases.i_update_eap import IUpdateEAP
from src.errors.eap.eap_not_found_error import EAPNotFoundError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class UpdateEAPController(ControllerInterface):
    """Controller para atualização de EAP"""
    
    def __init__(self, update_eap_case: IUpdateEAP):
        self.__update_eap_case = update_eap_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Manipula a requisição de atualização de EAP
        
        Args:
            http_request: Requisição HTTP
            
        Returns:
            HttpResponse: Resposta HTTP
        """
        try:
            body = http_request.body
            path_params = http_request.path_params
            
            # Extrai o ID da EAP dos path params
            eap_id = int(path_params.get("eap_id"))
            
            # Extrai os dados opcionais da requisição
            name = body.get("name")
            description = body.get("description")
            
            # Atualiza a EAP
            eap = self.__update_eap_case.update(
                eap_id=eap_id,
                name=name,
                description=description
            )
            
            # Converte a entidade para dicionário
            eap_data = self._entity_to_dict(eap)
            
            return HttpResponse(
                status_code=200,
                body={"eap": eap_data}
            )
            
        except EAPNotFoundError as e:
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
    
    def _entity_to_dict(self, eap) -> Dict[str, Any]:
        """Converte uma entidade EAP para dicionário"""
        # Organiza os itens em estrutura hierárquica
        items_dict = {}
        for item in eap.items:
            items_dict[item.id] = self._item_to_dict(item)
        
        # Organiza a hierarquia
        root_items = []
        for item_data in items_dict.values():
            if item_data["parent_id"] is None:
                root_items.append(item_data)
            else:
                parent = items_dict.get(item_data["parent_id"])
                if parent:
                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(item_data)
        
        return {
            "id": eap.id,
            "name": eap.name,
            "description": eap.description,
            "project_id": eap.project_id,
            "is_template": eap.is_template,
            "template_source_id": eap.template_source_id,
            "created_by": eap.created_by,
            "created_at": eap.created_at.isoformat() if eap.created_at else None,
            "updated_at": eap.updated_at.isoformat() if eap.updated_at else None,
            "items": root_items
        }
    
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
            "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            "children": []  # Será preenchido pela lógica de hierarquia
        }
