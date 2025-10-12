"""Get Gantt Data Use Case"""
#pylint:disable=all
from datetime import datetime
from typing import Dict, Any, List
from src.domain.use_cases.i_get_gantt_data import IGetGanttData
from src.data.interface.i_project_repository import IProjectRepository
from src.data.interface.i_eap_repository import IEAPRepository
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError
from src.errors.eap.eap_not_found_error import EAPNotFoundError


class GetGanttData(IGetGanttData):
    """Use case para buscar dados formatados para Gantt Chart"""
    
    def __init__(
        self,
        project_repository: IProjectRepository,
        eap_repository: IEAPRepository
    ) -> None:
        self.__project_repository = project_repository
        self.__eap_repository = eap_repository
    
    def execute(self, project_id: int) -> Dict[str, Any]:
        """
        Busca todos os dados necessários para o Gantt Chart
        
        Args:
            project_id: ID do projeto
            
        Returns:
            Dict com dados formatados para Gantt
        """
        # Buscar projeto
        project = self.__project_repository.find(project_id)
        if not project:
            raise ProjectNotFoundError()
        
        # Buscar EAP do projeto
        eap = self.__eap_repository.find_by_project_id(project_id)
        if not eap:
            raise EAPNotFoundError(project_id)
        
        # Converter itens da EAP para formato Gantt
        tasks = self._convert_items_to_gantt_format(eap.items)
        
        # Calcular estatísticas
        statistics = self._calculate_statistics(tasks)
        
        # Preparar resposta
        return {
            'project': {
                'id': project.project_id,
                'name': project.name,
                'status': project.status.description if hasattr(project, 'status') and project.status else None,
                'start_date': project.start_date.isoformat() if project.start_date else None,
                'expected_completion_date': project.expected_completion_date.isoformat() if project.expected_completion_date else None,
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'verba_disponivel': float(project.verba_disponivel.value) if hasattr(project.verba_disponivel, 'value') else float(project.verba_disponivel) if project.verba_disponivel else 0,
                'andamento_do_projeto': project.andamento_do_projeto if project.andamento_do_projeto else None
            },
            'eap': {
                'id': eap.id,
                'name': eap.name,
                'description': eap.description,
                'total_budget': sum(float(t['budget']) for t in tasks if t['parent'] == 0),
                'created_at': eap.created_at.isoformat() if eap.created_at else None,
                'items': [self._item_entity_to_dict(item) for item in eap.items]
            },
            'tasks': tasks,
            'links': [],  # TODO: Implementar dependências
            'statistics': statistics
        }
    
    def _convert_items_to_gantt_format(self, items: List[Any]) -> List[Dict[str, Any]]:
        """
        Converte itens da EAP para formato Gantt recursivamente
        
        Args:
            items: Lista de itens da EAP
            
        Returns:
            Lista de tarefas no formato Gantt
        """
        gantt_tasks = []
        
        for item in items:
            # Calcular duração em dias
            if item.start_date and item.end_date:
                duration = (item.end_date - item.start_date).days
                duration = max(duration, 1)  # Mínimo 1 dia
            else:
                duration = 1
            
            # Formatar datas
            start_date = item.start_date.strftime("%Y-%m-%d") if item.start_date else None
            end_date = item.end_date.strftime("%Y-%m-%d") if item.end_date else None
            
            # Extrair valores com segurança dos Value Objects
            type_value = str(item.type.value) if hasattr(item.type, 'value') else str(item.type)
            status_value = str(item.status.value) if hasattr(item.status, 'value') else str(item.status)
            code_value = str(item.code.value) if hasattr(item.code, 'value') else str(item.code)
            budget_value = float(item.budget.value) if hasattr(item.budget, 'value') else float(item.budget) if item.budget else 0
            
            # Processar filhos recursivamente primeiro para calcular orçamento correto
            child_tasks = []
            if hasattr(item, 'children') and item.children:
                child_tasks = self._convert_items_to_gantt_format(item.children)
            
            # Calcular orçamento: se tem filhos, soma apenas dos filhos diretos; senão, valor próprio
            if child_tasks:
                # Filtrar apenas filhos diretos (não netos)
                direct_children = [t for t in child_tasks if t['parent'] == item.id]
                calculated_budget = sum(float(t['budget']) for t in direct_children)
            else:
                calculated_budget = budget_value
            
            gantt_task = {
                'id': item.id,
                'text': item.name,
                'start_date': start_date,
                'end_date': end_date,
                'duration': duration,
                'progress': item.progress / 100 if item.progress else 0,  # Converter 0-100 para 0-1
                'parent': item.parent_id if item.parent_id else 0,
                'item_type': type_value,
                'responsible': item.responsible,
                'budget': calculated_budget,
                'status': status_value,
                'description': item.description,
                'code': code_value,
                'open': True  # Expandir por padrão
            }
            
            gantt_tasks.append(gantt_task)
            gantt_tasks.extend(child_tasks)
        
        return gantt_tasks
    
    def _calculate_statistics(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula estatísticas das tarefas
        
        Args:
            tasks: Lista de tarefas
            
        Returns:
            Dict com estatísticas
        """
        total = len(tasks)
        completed = sum(1 for t in tasks if t['status'] == 'concluido')
        in_progress = sum(1 for t in tasks if t['status'] == 'em_andamento')
        not_started = sum(1 for t in tasks if t['status'] == 'nao_iniciado')
        
        # Calcular atrasadas (end_date < hoje e progress < 100%)
        today = datetime.now().date()
        overdue = 0
        for task in tasks:
            if task['end_date']:
                try:
                    end_date = datetime.strptime(task['end_date'], "%Y-%m-%d").date()
                    if end_date < today and task['progress'] < 1.0:
                        overdue += 1
                except (ValueError, TypeError):
                    pass
        
        # Calcular total de orçamento (apenas itens raiz para evitar somar duplicado)
        root_tasks = [t for t in tasks if t['parent'] == 0]
        total_budget = sum(float(t['budget']) for t in root_tasks)
        
        # Calcular progresso médio
        if total > 0:
            average_progress = sum(t['progress'] for t in tasks) / total
        else:
            average_progress = 0
        
        return {
            'total_tasks': total,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'overdue': overdue,
            'paused': sum(1 for t in tasks if t['status'] == 'pausado'),
            'cancelled': sum(1 for t in tasks if t['status'] == 'cancelado'),
            'blocked': sum(1 for t in tasks if t['status'] == 'bloqueado'),
            'total_budget': total_budget,
            'average_progress': round(average_progress * 100, 2)  # Em porcentagem
        }
    
    def _item_entity_to_dict(self, item) -> Dict[str, Any]:
        """Converte um item da EAP entity para dicionário com validação de atributos"""
        
        # Extrair valores com segurança
        code_value = str(item.code.value) if hasattr(item.code, 'value') else str(item.code)
        type_value = str(item.type.value) if hasattr(item.type, 'value') else str(item.type)
        status_value = str(item.status.value) if hasattr(item.status, 'value') else str(item.status)
        budget_value = float(item.budget.value) if hasattr(item.budget, 'value') else float(item.budget)
        
        # Processar filhos recursivamente
        children = [self._item_entity_to_dict(child) for child in getattr(item, 'children', [])]
        
        # Calcular orçamento: se tem filhos, soma apenas dos filhos diretos; senão, valor próprio
        if children:
            calculated_budget = sum(child['budget'] for child in children)
        else:
            calculated_budget = budget_value
        
        return {
            'id': item.id,
            'eap_id': item.eap_id,
            'code': code_value,
            'name': item.name,
            'description': item.description,
            'type': type_value,
            'parent_id': item.parent_id,
            'responsible': item.responsible,
            'start_date': item.start_date.isoformat() if item.start_date else None,
            'end_date': item.end_date.isoformat() if item.end_date else None,
            'budget': calculated_budget,
            'status': status_value,
            'progress': item.progress,
            'created_at': item.created_at.isoformat() if item.created_at else None,
            'updated_at': item.updated_at.isoformat() if item.updated_at else None,
            'children': children
        }

