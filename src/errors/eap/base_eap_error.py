from src.errors.http.__http_base_error import HttpBaseError


class BaseEAPError(HttpBaseError):
    """Classe base para todos os erros relacionados ao EAP"""
    
    def __init__(self, status_code: int, message: str):
        super().__init__(
            status_code=status_code,
            title="EAP Error",
            message=message
        )
