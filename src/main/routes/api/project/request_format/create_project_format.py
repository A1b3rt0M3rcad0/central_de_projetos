from pydantic import BaseModel

class CreateProjectFormat(BaseModel):
    status_id:int
    name:str
    verba_disponivel:float|None
    andamento_do_projeto:str|None
    start_date:str|None
    expected_completion_date:str|None
    end_date:str|None