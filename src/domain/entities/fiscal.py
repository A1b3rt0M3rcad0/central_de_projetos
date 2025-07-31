from datetime import datetime
from src.domain.value_objects.email import Email

class FiscalEntity:

    def __init__(self, 
                 fiscal_id:int, 
                 name:str, 
                 created_at:datetime,
                 password:bytes=None,
                 salt:bytes=None,
                 email:Email=None,
                 phone:str=None,
                 refresh_token:str=None) -> None:
        self.fiscal_id = fiscal_id
        self.name = name
        self.created_at = created_at
        self.password = password
        self.salt = salt
        self.email = email
        self.phone = phone
        self.refresh_token = refresh_token
