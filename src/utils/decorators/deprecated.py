from functools import wraps
from src.logs.log_internal import log_internal

def deprecated(reason: str = "This function/method is obsolete."):
    """
    Decorator para marcar funções/métodos como obsoletos.
    Loga o uso e emite um aviso de DeprecationWarning.

    Args:
        reason (str): Motivo da depreciação.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_internal(
                logger_name="deprecated_logger",
                level="WARNING",
                message=f"[DEPRECATED] {func.__qualname__} is deprecated: {reason}",
                func_name=func.__qualname__
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
