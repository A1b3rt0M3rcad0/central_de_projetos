from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from ..entities.eap import EAPItemEntity
from ..value_objects.eap_code import EAPCode
from ..value_objects.eap_type import EAPType
from ..value_objects.eap_status import EAPStatus
from ..value_objects.monetary_value import MonetaryValue


class ICreateEAPItem(ABC):
    """Interface para o caso de uso de criação de item da EAP"""
    
    @abstractmethod
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
        pass
