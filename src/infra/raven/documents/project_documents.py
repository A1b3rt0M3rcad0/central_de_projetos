from typing import Dict

class ProjectDocuments:

    def __init__(self, name:str, description:str|None) -> None:
        self.name = name
        self.description = description
    
    def make_to_store(self, project_id:int) -> Dict:
        return {
            'entity': self,
            'key': self.__class__.__name__ +'/'+f'{project_id}'
        }