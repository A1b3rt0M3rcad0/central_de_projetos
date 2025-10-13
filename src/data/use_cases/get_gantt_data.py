"""Get Gantt Data Use Case"""
from datetime import datetime
from typing import Dict, Any, List
from src.domain.use_cases.i_get_gantt_data import IGetGanttData
from src.data.interface.i_project_repository import IProjectRepository
from src.data.interface.i_eap_repository import IEAPRepository
from src.data.interface.i_eap_dependency_repository import IEAPDependencyRepository
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError
from src.errors.eap.eap_not_found_error import EAPNotFoundError


class GetGanttData(IGetGanttData):
    """Use case para buscar dados formatados para Gantt Chart"""
    
    def __init__(
        self,
        project_repository: IProjectRepository,
        eap_repository: IEAPRepository,
        dependency_repository: IEAPDependencyRepository = None
    ) -> None:
        self.__project_repository = project_repository
        self.__eap_repository = eap_repository
        self.__dependency_repository = dependency_repository
    
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
            raise ProjectNotFoundError(f"Projeto com ID {project_id} não encontrado")
        
        # Buscar EAP do projeto
        eap = self.__eap_repository.find_by_project_id(project_id)
        if not eap:
            raise EAPNotFoundError(project_id)
        
        # Construir hierarquia de itens
        # eap.items é uma lista plana de todos os itens, precisamos construir a árvore
        items_dict_flat = {item.id: self._item_entity_to_dict(item) for item in eap.items}
        
        # Construir hierarquia: adicionar filhos aos pais
        root_items = []
        for item_dict in items_dict_flat.values():
            parent_id = item_dict['parent_id']
            if parent_id is None:
                # Item raiz
                root_items.append(item_dict)
            else:
                # Item filho - adicionar ao pai
                if parent_id in items_dict_flat:
                    if 'children' not in items_dict_flat[parent_id] or not items_dict_flat[parent_id]['children']:
                        items_dict_flat[parent_id]['children'] = []
                    items_dict_flat[parent_id]['children'].append(item_dict)
        
        # Aplicar cálculos de execução de verba em todos os itens raiz (recursivo)
        self._apply_calculated_values(root_items)
        
        # Criar mapa de ID -> calculated_progress para usar no Gantt
        progress_map = self._create_progress_map(root_items)
        
        # Converter itens da EAP para formato Gantt usando o progresso calculado
        tasks = self._convert_items_to_gantt_format(eap.items, progress_map)
        
        # Calcular estatísticas
        statistics = self._calculate_statistics(tasks)
        
        # Buscar dependências (se repository disponível)
        links = []
        if self.__dependency_repository:
            try:
                links = self._build_dependency_links(eap.id)
            except Exception as e:
                # Se der erro ao buscar dependências, apenas loga e continua sem links
                print(f"⚠️ Erro ao buscar dependências: {e}")
                links = []
        
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
                'items': root_items
            },
            'tasks': tasks,
            'links': links,
            'statistics': statistics
        }
    
    def _apply_calculated_values(self, items: List[Dict[str, Any]]) -> None:
        """
        Aplica cálculos de executed_value e calculated_progress em todos os itens
        
        Args:
            items: Lista de itens (modificada in-place)
        """
        for item in items:
            # Calcular valores executados e progresso
            executed_value = self._calculate_total_executed_value(item)
            calculated_progress = self._calculate_item_progress(item)
            
            # Adicionar ao dicionário
            item['executed_value'] = executed_value
            item['calculated_progress'] = calculated_progress
            
            # Aplicar recursivamente aos filhos
            if item.get('children'):
                self._apply_calculated_values(item['children'])
    
    def _create_progress_map(self, items: List[Dict[str, Any]]) -> Dict[int, int]:
        """
        Cria um mapa de ID -> calculated_progress para todos os itens
        
        Args:
            items: Lista de itens com calculated_progress
            
        Returns:
            Dict mapeando item_id para calculated_progress
        """
        progress_map = {}
        
        def add_to_map(items_list):
            for item in items_list:
                progress_map[item['id']] = item.get('calculated_progress', item.get('progress', 0))
                if item.get('children'):
                    add_to_map(item['children'])
        
        add_to_map(items)
        return progress_map
    
    def _convert_items_to_gantt_format(self, items: List[Any], progress_map: Dict[int, int] = None) -> List[Dict[str, Any]]:
        """
        Converte itens da EAP para formato Gantt recursivamente
        
        Args:
            items: Lista de itens da EAP
            progress_map: Mapa de ID -> calculated_progress (opcional)
            
        Returns:
            Lista de tarefas no formato Gantt
        """
        if progress_map is None:
            progress_map = {}
        
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
                child_tasks = self._convert_items_to_gantt_format(item.children, progress_map)
            
            # Calcular orçamento: se tem filhos, soma apenas dos filhos diretos; senão, valor próprio
            if child_tasks:
                # Filtrar apenas filhos diretos (não netos)
                direct_children = [t for t in child_tasks if t['parent'] == item.id]
                calculated_budget = sum(float(t['budget']) for t in direct_children)
            else:
                calculated_budget = budget_value
            
            # Usar progresso calculado do mapa se disponível, senão usa o progresso direto
            progress_value = progress_map.get(item.id, item.progress)
            
            # Debug: verificar se está enviando o progresso correto
            if progress_value != item.progress:
                print(f"🔍 Backend - Task {item.id} ({item.name}): original={item.progress}%, calculated={progress_value}%")
            
            gantt_task = {
                'id': item.id,
                'text': item.name,
                'start_date': start_date,
                'end_date': end_date,
                'duration': duration,
                'progress': progress_value / 100 if progress_value else 0,  # Converter 0-100 para 0-1
                'calculated_progress': progress_value,  # Progresso calculado (0-100)
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
            'budget': budget_value,
            'status': status_value,
            'progress': item.progress,
            'created_at': item.created_at.isoformat() if item.created_at else None,
            'updated_at': item.updated_at.isoformat() if item.updated_at else None,
            'children': [],  # Será preenchido pela construção da hierarquia
            'executed_value': 0.0,  # Será calculado por _apply_calculated_values
            'calculated_progress': 0  # Será calculado por _apply_calculated_values
        }
    
    def _build_dependency_links(self, eap_id: int) -> List[Dict[str, Any]]:
        """
        Constrói lista de links (dependências) para o Gantt
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            Lista de links no formato do dhtmlx-gantt
        """
        if not self.__dependency_repository:
            return []
        
        # Busca todas as dependências da EAP
        dependencies = self.__dependency_repository.find_all_by_eap(eap_id)
        
        # Mapeia tipos de dependência para formato do Gantt
        # dhtmlx-gantt usa: "0" = FS, "1" = SS, "2" = FF, "3" = SF
        type_map = {
            'FS': '0',
            'SS': '1',
            'FF': '2',
            'SF': '3'
        }
        
        # Converte para formato do Gantt
        links = []
        for dep in dependencies:
            links.append({
                'id': dep.id,
                'source': dep.predecessor_id,  # De quem parte a seta
                'target': dep.successor_id,     # Para quem vai a seta
                'type': type_map.get(dep.dependency_type.value, '0')
            })
        
        return links

