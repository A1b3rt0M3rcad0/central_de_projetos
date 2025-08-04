from typing import Dict

class ProjectDocumentsFiscal:

    def __init__(self, name:str|None="", description:str|None=None) -> None:
        self.name = name
        self.description = description
    
    def make_to_store(self, work_project_id:int) -> Dict:
        return {
            'entity': self,
            'key': self.__class__.__name__ +'/'+f'{work_project_id}'
        }