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
    
    def _calculate_executed_value(self, item_dict: Dict[str, Any]) -> float:
        """
        Calcula o valor executado de um item (orçamento × progresso)
        
        Args:
            item_dict: Dicionário do item
            
        Returns:
            float: Valor executado
        """
        budget = float(item_dict.get("budget", 0))
        progress = float(item_dict.get("progress", 0)) / 100.0
        return budget * progress
    
    def _calculate_total_executed_value(self, item_dict: Dict[str, Any]) -> float:
        """
        Calcula o valor executado total de um item e seus filhos recursivamente
        
        Args:
            item_dict: Dicionário do item
            
        Returns:
            float: Valor executado total (incluindo filhos)
        """
        # Se não tem filhos, calcula só o próprio valor executado
        if not item_dict.get("children") or len(item_dict["children"]) == 0:
            return self._calculate_executed_value(item_dict)
        
        # Se tem filhos, soma o valor executado de todos os filhos
        total = 0.0
        for child in item_dict["children"]:
            total += self._calculate_total_executed_value(child)
        return total
    
    def _calculate_item_progress(self, item_dict: Dict[str, Any]) -> int:
        """
        Calcula o progresso real de um item baseado no valor executado dos filhos
        
        Args:
            item_dict: Dicionário do item
            
        Returns:
            int: Progresso calculado (0-100)
        """
        # Se não tem filhos, usa o progresso próprio
        if not item_dict.get("children") or len(item_dict["children"]) == 0:
            return item_dict.get("progress", 0)
        
        # Se tem filhos, calcula o progresso baseado no valor executado
        total_budget = float(item_dict.get("budget", 0))
        
        # Se não tem orçamento definido, não pode calcular progresso
        if total_budget == 0:
            return 0
        
        # Soma o valor executado de todos os filhos
        total_executed_value = 0.0
        for child in item_dict["children"]:
            total_executed_value += self._calculate_total_executed_value(child)
        
        # Calcula o percentual de execução baseado no orçamento total do pai
        progress_percentage = (total_executed_value / total_budget) * 100
        
        return round(min(progress_percentage, 100))  # Máximo 100%
    
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
        
        # Calcula valores executados e progresso para cada item
        for item_data in items_dict.values():
            executed_value = self._calculate_total_executed_value(item_data)
            calculated_progress = self._calculate_item_progress(item_data)
            
            item_data["executed_value"] = executed_value
            item_data["calculated_progress"] = calculated_progress
        
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
            "children": [],  # Será preenchido pela lógica de hierarquia
            "executed_value": 0.0,  # Será calculado pela lógica de execução
            "calculated_progress": 0  # Será calculado pela lógica de progresso
        }