from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Bairro(BaseModel):
    id:int
    name:str

class Empresa(BaseModel):
    id:int
    name:str

class Fiscal(BaseModel):
    id:int
    name:str

class Type(BaseModel):
    id:int
    name:str

class Vereador(BaseModel):
    id:int
    name:str

class FindAssociationProjectsContet(BaseModel):
    bairro:List[Bairro]
    empresa:List[Empresa]
    fiscal:List[Fiscal]
    type:List[Type]
    vereador:List[Vereador]

class FindAssociationProjectsResponse(BaseResponse[FindAssociationProjectsContet]):
    ...