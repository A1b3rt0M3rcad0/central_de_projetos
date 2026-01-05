from src.errors.eap.base_eap_error import BaseEAPError


class EAPItemNotFoundError(BaseEAPError):
    """Erro quando um item da EAP não é encontrado"""
    
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(
            status_code=404,
            message=f"Item da EAP com ID {item_id} não encontrado"
        )
