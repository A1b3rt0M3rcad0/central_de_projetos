from src.errors.eap.base_eap_error import BaseEAPError


class InvalidEAPCodeError(BaseEAPError):
    """Erro quando o código da EAP é inválido"""
    
    def __init__(self, code: str, reason: str = ""):
        self.code = code
        self.reason = reason
        message = f"Código EAP inválido: {code}"
        if reason:
            message += f" - {reason}"
        super().__init__(
            status_code=400,
            message=message
        )
