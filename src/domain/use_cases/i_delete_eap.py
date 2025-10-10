from abc import ABC, abstractmethod


class IDeleteEAP(ABC):
    """Interface para o caso de uso de exclusão de EAP"""
    
    @abstractmethod
    def delete(self, eap_id: int) -> None:
        """
        Exclui uma EAP
        
        Args:
            eap_id: ID da EAP a ser excluída
            
        Raises:
            EAPNotFoundError: Se a EAP não existir
            EAPInUseError: Se a EAP estiver sendo usada por outros projetos
        """
        pass
