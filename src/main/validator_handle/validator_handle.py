from typing import Type
from pydantic import BaseModel, ValidationError
from src.errors.http.http_unprocessable_entity import UnprocessalbeEntity

def validator_handler(schema_class: Type[BaseModel], data: dict) -> dict:
    try:
        return schema_class(**data).dict()
    except ValidationError as e:
        raise UnprocessalbeEntity(
            title='Unprocessable Entity',
            message=f"Invalid request format for {schema_class.__name__}.",
        ) from e