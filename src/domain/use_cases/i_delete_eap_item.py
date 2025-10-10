from abc import ABC, abstractmethod


class IDeleteEAPItem(ABC):
    """Interface para o caso de uso de exclusão de item da EAP"""
    
    @abstractmethod
    def delete(self, item_id: int) -> None:
        """
        Exclui um item da EAP e todos os seus filhos (exclusão em cascata)
        
        Args:
            item_id: ID do item a ser excluído
            
        Raises:
            EAPItemNotFoundError: Se o item não existir
        """
        pass
