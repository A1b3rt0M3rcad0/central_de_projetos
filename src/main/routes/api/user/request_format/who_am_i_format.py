from pydantic import BaseModel

class WhoAmIFormat(BaseModel):
    token: str 