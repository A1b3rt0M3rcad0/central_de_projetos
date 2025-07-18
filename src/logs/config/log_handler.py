from src.data.interface.i_log_entry_repository import ILogEntryRepository
from src.infra.mongo.models.log_entry_model import LogEntryModel
from typing import List

class LogHandler:

    def __init__(self, log_entry_repository:ILogEntryRepository):
        self.__log_entry_repository = log_entry_repository
    
    def save(self, log:LogEntryModel) -> None:
        try:
            self.__log_entry_repository.save(log=log)
        except Exception as e:
            raise e from e
    
    def find_all(self, limit:int=100) -> List[LogEntryModel]:
        try:
            result = self.__log_entry_repository.find_all(limit=limit)
            return result
        except Exception as e:
            raise e from e