from abc import ABC, abstractmethod

class Document(ABC):

    @property
    @abstractmethod
    def content_type(self) -> str:pass

    @property
    @abstractmethod
    def name(self) -> str:pass
    
    @abstractmethod
    def value(self) -> bytes:pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        '''
        {
            'document': self.value(),
            'content_type': self.__content_type,
            'document_name': self.document_name,
            'name': self.__name
        }
        '''