from src.errors.repository.already_exists_error.__base_already_exists_error import BaseAlreadyExistsError

class ProjectFolderAlreadyExists(BaseAlreadyExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectFolderAlreadyExists',
            message=message,
            *args,
            **kwargs
        )

