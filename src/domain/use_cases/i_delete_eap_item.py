from abc import ABC, abstractmethod


class IDeleteEAPItem(ABC):
    """Interface para o caso de uso de exclusão de item da EAP"""
    
    @abstractmethod
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
        pass
