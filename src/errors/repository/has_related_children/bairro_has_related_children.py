from src.errors.repository.has_related_children.__base_has_related_children import BaseHasRelatedChildren

class BairroHasRelatedChildren(BaseHasRelatedChildren):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title=self.__class__.__name__,
            message=message,
            *args,
            **kwargs
        )