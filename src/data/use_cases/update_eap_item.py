from datetime import datetime
from typing import Optional

from src.domain.entities.eap import EAPItemEntity
from src.domain.use_cases.i_update_eap_item import IUpdateEAPItem
from src.domain.use_cases.i_find_eap_item import IFindEAPItem
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.domain.value_objects.eap_status import EAPStatus
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.eap.eap_item_not_found_error import EAPItemNotFoundError
from src.errors.eap.invalid_status_transition_error import InvalidStatusTransitionError
from src.errors.eap.budget_exceeded_error import BudgetExceededError
from src.errors.eap.invalid_date_range_error import InvalidDateRangeError


def _normalize_datetime(dt: datetime) -> datetime:
    """Remove timezone information from datetime for comparison"""
    if dt is None:
        return None
    # Converte para date (apenas dia/mês/ano, sem hora) para comparação
    # Isso resolve problemas de timezone
    if hasattr(dt, 'date'):
        return dt.date()
    return dt


class UpdateEAPItem(IUpdateEAPItem):
    """Caso de uso para atualização de item da EAP"""
    
    def __init__(self, eap_item_repository: IEAPItemRepository, find_eap_item_case: IFindEAPItem):
        self.__eap_item_repository = eap_item_repository
        self.__find_eap_item_case = find_eap_item_case
    
    # pylint: disable=too-many-branches
    def update(self, item_id: int, name: Optional[str] = None, description: Optional[str] = None,
               responsible: Optional[str] = None, start_date: Optional[datetime] = None,
               end_date: Optional[datetime] = None, budget: Optional[MonetaryValue] = None,
               status: Optional[EAPStatus] = None, progress: Optional[int] = None) -> EAPItemEntity:
        """
        Atualiza um item da EAP
        
        Args:
            item_id: ID do item
            name: Novo nome do item (opcional)
            description: Nova descrição do item (opcional)
            responsible: Novo responsável (opcional)
            start_date: Nova data de início (opcional)
            end_date: Nova data de fim (opcional)
            budget: Novo orçamento (opcional)
            status: Novo status (opcional)
            progress: Novo progresso (opcional)
            
        Returns:
            EAPItemEntity: O item atualizado
            
        Raises:
            EAPItemNotFoundError: Se o item não existir
            ValueError: Se os dados fornecidos forem inválidos
            InvalidStatusTransitionError: Se a transição de status for inválida
        """
        # Busca o item existente
        existing_item = self.__find_eap_item_case.find_by_id(item_id)
        if not existing_item:
            raise EAPItemNotFoundError(item_id)
        
        # Valida os novos dados
        if name is not None and not name.strip():
            raise ValueError("Nome do item não pode estar vazio")
        
        if description is not None and not description.strip():
            raise ValueError("Descrição do item não pode estar vazia")
        
        if responsible is not None and not responsible.strip():
            raise ValueError("Responsável não pode estar vazio")
        
        if progress is not None and (progress < 0 or progress > 100):
            raise ValueError("Progresso deve estar entre 0 e 100")
        
        # Valida transição de status
        if status is not None and status != existing_item.status:
            if not existing_item.status.can_transition_to(status):
                raise InvalidStatusTransitionError(str(existing_item.status), str(status))
        
        # Valida as datas
        start_date_to_use = start_date if start_date is not None else existing_item.start_date
        end_date_to_use = end_date if end_date is not None else existing_item.end_date
        
        # Normaliza as datas para comparação
        if _normalize_datetime(start_date_to_use) > _normalize_datetime(end_date_to_use):
            raise ValueError("Data de início não pode ser posterior à data de fim")
        
        # Validação de datas com o pai: se as datas estão sendo alteradas e o item tem pai
        if existing_item.parent_id is not None and (start_date is not None or end_date is not None):
            parent_item = self.__find_eap_item_case.find_by_id(existing_item.parent_id)
            if parent_item:
                # Normaliza as datas para comparação (remove timezone)
                child_start = _normalize_datetime(start_date_to_use)
                child_end = _normalize_datetime(end_date_to_use)
                parent_start = _normalize_datetime(parent_item.start_date)
                parent_end = _normalize_datetime(parent_item.end_date)
                
                if child_start < parent_start or child_end > parent_end:
                    raise InvalidDateRangeError(
                        child_name=name if name is not None else existing_item.name,
                        parent_name=parent_item.name,
                        child_start=start_date_to_use,
                        child_end=end_date_to_use,
                        parent_start=parent_item.start_date,
                        parent_end=parent_item.end_date
                    )
        
        # Validação de orçamento: se o orçamento está sendo alterado e o item tem pai
        if budget is not None and existing_item.parent_id is not None:
            # Busca o item pai
            parent_item = self.__find_eap_item_case.find_by_id(existing_item.parent_id)
            if parent_item:
                # Calcula o orçamento atual dos filhos (excluindo o item sendo atualizado)
                current_children_budget = self.__eap_item_repository.get_children_budget_total(existing_item.parent_id)
                current_item_budget = float(existing_item.budget.value)
                other_children_budget = current_children_budget - current_item_budget
                new_total_budget = other_children_budget + float(budget.value)
                
                if new_total_budget > float(parent_item.budget.value):
                    raise BudgetExceededError(
                        parent_name=parent_item.name,
                        parent_budget=float(parent_item.budget.value),
                        children_budget=new_total_budget
                    )
        
        # Cria uma nova instância com os dados atualizados
        updated_item = EAPItemEntity(
            id=existing_item.id,
            eap_id=existing_item.eap_id,
            code=existing_item.code,
            name=name if name is not None else existing_item.name,
            description=description if description is not None else existing_item.description,
            type=existing_item.type,
            parent_id=existing_item.parent_id,
            responsible=responsible if responsible is not None else existing_item.responsible,
            start_date=start_date_to_use,
            end_date=end_date_to_use,
            budget=budget if budget is not None else existing_item.budget,
            status=status if status is not None else existing_item.status,
            progress=progress if progress is not None else existing_item.progress,
            created_at=existing_item.created_at,
            updated_at=datetime.now()
        )
        
        # Salva as alterações
        return self.__eap_item_repository.update(updated_item)
