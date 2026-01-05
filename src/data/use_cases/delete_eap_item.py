from src.domain.use_cases.i_delete_eap_item import IDeleteEAPItem
from src.domain.use_cases.i_find_eap_item import IFindEAPItem
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.errors.eap.eap_item_not_found_error import EAPItemNotFoundError


class DeleteEAPItem(IDeleteEAPItem):
    """Caso de uso para exclusão de item da EAP (com exclusão em cascata)"""
    
    def __init__(self, eap_item_repository: IEAPItemRepository, find_eap_item_case: IFindEAPItem):
        self.__eap_item_repository = eap_item_repository
        self.__find_eap_item_case = find_eap_item_case
    
    def delete(self, item_id: int) -> None:
        """
        Exclui um item da EAP e todos os seus filhos (exclusão em cascata)
        
        Args:
            item_id: ID do item a ser excluído
            
        Raises:
            EAPItemNotFoundError: Se o item não existir
        """
        # Verifica se o item existe
        existing_item = self.__find_eap_item_case.find_by_id(item_id)
        if not existing_item:
            raise EAPItemNotFoundError(item_id)
        
        # Exclui o item (a exclusão em cascata é feita no repositório)
        self.__eap_item_repository.delete(item_id)
