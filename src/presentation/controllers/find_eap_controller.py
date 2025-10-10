from typing import Dict, Any, List

from src.domain.use_cases.i_find_eap import IFindEAP
from src.errors.eap.eap_not_found_error import EAPNotFoundError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class FindEAPController(ControllerInterface):  # pylint: disable=too-few-public-methods
    """Controller para busca de EAP"""
    
    def __init__(self, find_eap_case: IFindEAP):
        self.__find_eap_case = find_eap_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:  # pylint: disable=too-many-return-statements
        """
        Manipula a requisição de busca de EAP
        
        Args:
            http_request: Requisição HTTP
            
        Returns:
            HttpResponse: Resposta HTTP
        """
        try:
            # Verifica se há parâmetros de busca
            query_params = http_request.query_params or {}
            path_params = http_request.path_params or {}
            
            # Busca por ID específico
            if "eap_id" in query_params:
                eap_id = int(query_params["eap_id"])
                eap = self.__find_eap_case.find_by_id(eap_id)
                
                if not eap:
                    return HttpResponse(
                        status_code=404,
                        body={"error": f"EAP com ID {eap_id} não encontrada"}
                    )
                
                eap_data = self._entity_to_dict(eap)
                return HttpResponse(
                    status_code=200,
                    body={"eap": eap_data}
                )
            
            # Busca por projeto (path params tem prioridade)
            if "project_id" in path_params:
                project_id = int(path_params["project_id"])
                eap = self.__find_eap_case.find_by_project_id(project_id)
                
                if not eap:
                    return HttpResponse(
                        status_code=404,
                        body={"error": f"EAP do projeto {project_id} não encontrada"}
                    )
                
                eap_data = self._entity_to_dict(eap)
                return HttpResponse(
                    status_code=200,
                    body={"eap": eap_data}
                )
            
            # Busca por projeto (query params como fallback)
            if "project_id" in query_params:
                project_id = int(query_params["project_id"])
                eap = self.__find_eap_case.find_by_project_id(project_id)
                
                if not eap:
                    return HttpResponse(
                        status_code=404,
                        body={"error": f"EAP do projeto {project_id} não encontrada"}
                    )
                
                eap_data = self._entity_to_dict(eap)
                return HttpResponse(
                    status_code=200,
                    body={"eap": eap_data}
                )
            
            # Busca templates
            if "templates" in query_params and query_params["templates"].lower() == "true":
                eaps = self.__find_eap_case.find_templates()
                eaps_data = [self._entity_to_dict(eap) for eap in eaps]
                return HttpResponse(
                    status_code=200,
                    body={"eaps": eaps_data}
                )
            
            # Busca por nome
            if "name" in query_params:
                name = query_params["name"]
                eaps = self.__find_eap_case.find_by_name(name)
                eaps_data = [self._entity_to_dict(eap) for eap in eaps]
                return HttpResponse(
                    status_code=200,
                    body={"eaps": eaps_data}
                )
            
            # Busca todas com paginação
            limit = int(query_params.get("limit", 50))
            offset = int(query_params.get("offset", 0))
            
            eaps = self.__find_eap_case.find_all(limit=limit, offset=offset)
            eaps_data = [self._entity_to_dict(eap) for eap in eaps]
            
            return HttpResponse(
                status_code=200,
                body={"eaps": eaps_data}
            )
            
        except ValueError:
            return HttpResponse(
                status_code=400,
                body={"error": "Parâmetros inválidos"}
            )
        except Exception:
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
        
        # Calcula orçamento total da EAP
        total_budget = sum(float(item_data["budget"]) for item_data in items_dict.values())
        
        # Busca verba disponível do projeto se houver
        project_budget = None
        if eap.project_id:
            # Importa aqui para evitar dependência circular
            from src.infra.relational.models.project import Project
            from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
            
            try:
                with db_connection_handler_factory() as db:
                    project = db.session.query(Project).filter(Project.id == eap.project_id).first()
                    if project:
                        project_budget = float(project.verba_disponivel) if project.verba_disponivel else None
            except Exception:
                pass  # Ignora erros ao buscar projeto
        
        return {
            "id": eap.id,
            "name": eap.name,
            "description": eap.description,
            "project_id": eap.project_id,
            "project_budget": project_budget,
            "total_budget": total_budget,
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