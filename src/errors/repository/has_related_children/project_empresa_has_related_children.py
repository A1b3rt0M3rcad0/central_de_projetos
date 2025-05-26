from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class ProjectEmpresaHasRelatedChildren(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title=self.__class__.__name__,
            message=message,
            *args,
            **kwargs
        )