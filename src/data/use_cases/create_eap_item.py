from datetime import datetime
from typing import Optional

from src.domain.entities.eap import EAPItemEntity
from src.domain.use_cases.i_create_eap_item import ICreateEAPItem
from src.domain.use_cases.i_find_eap import IFindEAP
from src.domain.use_cases.i_find_eap_item import IFindEAPItem
from src.data.interface.i_eap_item_repository import IEAPItemRepository
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


def _normalize_datetime(dt: datetime) -> datetime:
    """Remove timezone information from datetime for comparison"""
    if dt is None:
        return None
    # Converte para date (apenas dia/mês/ano, sem hora) para comparação
    # Isso resolve problemas de timezone
    if hasattr(dt, 'date'):
        return dt.date()
    return dt


class CreateEAPItem(ICreateEAPItem):
    """Caso de uso para criação de item da EAP"""
    
    def __init__(self, eap_item_repository: IEAPItemRepository, find_eap_case: IFindEAP, find_eap_item_case: IFindEAPItem):
        self.__eap_item_repository = eap_item_repository
        self.__find_eap_case = find_eap_case
        self.__find_eap_item_case = find_eap_item_case
    
    def create(self, eap_id: int, code: EAPCode, name: str, description: str, 
               eap_type: EAPType, parent_id: Optional[int], responsible: str,
               start_date: datetime, end_date: datetime, budget: MonetaryValue,
               status: EAPStatus = EAPStatus.NAO_INICIADO, progress: int = 0) -> EAPItemEntity:
        """
        Cria um novo item na EAP
        
        Args:
            eap_id: ID da EAP
            code: Código hierárquico do item
            name: Nome do item
            description: Descrição do item
            eap_type: Tipo do item (fase, entrega, atividade, tarefa)
            parent_id: ID do item pai (None para itens raiz)
            responsible: Responsável pelo item
            start_date: Data de início
            end_date: Data de fim
            budget: Orçamento do item
            status: Status inicial do item
            progress: Progresso inicial (0-100)
            
        Returns:
            EAPItemEntity: O item criado
            
        Raises:
            EAPNotFoundError: Se a EAP não existir
            EAPItemNotFoundError: Se o item pai não existir
            InvalidEAPCodeError: Se o código for inválido
            InvalidEAPTypeError: Se o tipo não for válido para a hierarquia
            DuplicateEAPCodeError: Se o código já existir na EAP
        """
        # Verifica se a EAP existe
        eap = self.__find_eap_case.find_by_id(eap_id)
        if not eap:
            raise EAPNotFoundError(eap_id)
        
        # Verifica se o código já existe na EAP
        if self.__eap_item_repository.exists_by_code(eap_id, str(code)):
            raise DuplicateEAPCodeError(str(code), eap_id)
        
        # Se há um item pai, verifica se ele existe e se o tipo é válido
        if parent_id is not None:
            parent_item = self.__find_eap_item_case.find_by_id(parent_id)
            if not parent_item:
                raise EAPItemNotFoundError(parent_id)
            
            # Verifica se o item pai pertence à mesma EAP
            if parent_item.eap_id != eap_id:
                raise ValueError("Item pai deve pertencer à mesma EAP")
            
            # Verifica se o tipo é válido para a hierarquia
            if not parent_item.type.is_valid_child_type(eap_type):
                raise ValueError(f"Tipo {eap_type} não é válido como filho de {parent_item.type}")
            
            # Verifica se o código é consistente com a hierarquia
            expected_parent_code = str(parent_item.code)
            if not str(code).startswith(expected_parent_code + '.'):
                raise InvalidEAPCodeError(str(code), "Código não é consistente com a hierarquia")
            
            # Validação de datas: verifica se as datas do filho estão dentro do período do pai
            # Normaliza as datas para comparação (remove timezone)
            child_start = _normalize_datetime(start_date)
            child_end = _normalize_datetime(end_date)
            parent_start = _normalize_datetime(parent_item.start_date)
            parent_end = _normalize_datetime(parent_item.end_date)
            
            if child_start < parent_start or child_end > parent_end:
                raise InvalidDateRangeError(
                    child_name=name,
                    parent_name=parent_item.name,
                    child_start=start_date,
                    child_end=end_date,
                    parent_start=parent_item.start_date,
                    parent_end=parent_item.end_date
                )
            
            # Validação de orçamento: verifica se o orçamento dos filhos não excede o do pai
            current_children_budget = self.__eap_item_repository.get_children_budget_total(parent_id)
            new_total_budget = current_children_budget + float(budget.value)
            
            if new_total_budget > float(parent_item.budget.value):
                raise BudgetExceededError(
                    parent_name=parent_item.name,
                    parent_budget=float(parent_item.budget.value),
                    children_budget=new_total_budget
                )
        else:
            # Para itens raiz, verifica se o tipo é válido
            if eap_type not in EAPType.get_root_types():
                raise ValueError(f"Tipo {eap_type} não é válido para itens raiz")
        
        # Valida o progresso
        if progress < 0 or progress > 100:
            raise ValueError("Progresso deve estar entre 0 e 100")
        
        # Valida as datas
        if _normalize_datetime(start_date) > _normalize_datetime(end_date):
            raise ValueError("Data de início não pode ser posterior à data de fim")
        
        # Cria o novo item
        now = datetime.now()
        new_item = EAPItemEntity(
            id=None,
            eap_id=eap_id,
            code=code,
            name=name,
            description=description,
            type=eap_type,
            parent_id=parent_id,
            responsible=responsible,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            status=status,
            progress=progress,
            created_at=now,
            updated_at=now
        )
        
        # Salva o item
        return self.__eap_item_repository.create(new_item)
