from src.domain.use_cases.i_delete_eap_item import IDeleteEAPItem
from src.domain.use_cases.i_find_eap_item import IFindEAPItem
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.errors.eap.eap_item_not_found_error import EAPItemNotFoundError
from src.errors.eap.eap_item_has_children_error import EAPItemHasChildrenError


class DeleteEAPItem(IDeleteEAPItem):
    """Caso de uso para exclusão de item da EAP"""
    
    def __init__(self, eap_item_repository: IEAPItemRepository, find_eap_item_case: IFindEAPItem):
        self.__eap_item_repository = eap_item_repository
        self.__find_eap_item_case = find_eap_item_case
    
    def delete(self, item_id: int) -> None:
        """
        Exclui um item da EAP
        
        Args:
            item_id: ID do item a ser excluído
            
        Raises:
            EAPItemNotFoundError: Se o item não existir
            EAPItemHasChildrenError: Se o item tiver filhos
            EAPItemInProgressError: Se o item estiver em andamento
        """
        # Verifica se o item existe
        existing_item = self.__find_eap_item_case.find_by_id(item_id)
        if not existing_item:
            raise EAPItemNotFoundError(item_id)
        
        # Verifica se o item tem filhos
        children_count = self.__eap_item_repository.count_children(item_id)
        if children_count > 0:
            raise EAPItemHasChildrenError(item_id, children_count)
        
        # Verifica se o item está em andamento (não pode ser excluído)
        if existing_item.status.is_active():
            raise ValueError("Item em andamento não pode ser excluído")
        
        # Exclui o item
        self.__eap_item_repository.delete(item_id)
