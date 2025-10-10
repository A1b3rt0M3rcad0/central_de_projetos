from src.errors.eap.base_eap_error import BaseEAPError


class EAPItemHasChildrenError(BaseEAPError):
    """Erro quando um item da EAP tem filhos e não pode ser excluído"""
    
    def __init__(self, item_id: int, children_count: int):
        self.item_id = item_id
        self.children_count = children_count
        super().__init__(
            status_code=409,
            message=f"Item da EAP {item_id} possui {children_count} filhos e não pode ser excluído"
        )
