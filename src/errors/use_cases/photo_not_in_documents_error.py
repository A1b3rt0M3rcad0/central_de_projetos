from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError

class PhotoNotInDocumentsError(BaseUseCaseError):
    
    def __init__(self, photo_name: str, *args, **kwargs) -> None:
        super().__init__(
            title='PhotoNotInDocumentsError',
            message=f"Photo '{photo_name}' must exist in additional_documents before updating work_project photo",
            *args,
            **kwargs
        ) 