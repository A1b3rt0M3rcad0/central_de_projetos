from dotenv import load_dotenv
import os

class RedisUrlConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.__url: str = os.getenv("REDIS_URL")
        self.__port: int = os.getenv("REDIS_PORT")
        self.__username: str = os.getenv("REDIS_USERNAME")
        self.__password: str = os.getenv("REDIS_PASSWORD")
        self.__decode_responses: bool = os.getenv("REDIS_DECODE_RESPONSES")
        self.__socket_connect_timeout: float = float(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT"))
        self.__socket_timeout: float = float(os.getenv("REDIS_SOCKET_TIMEOUT"))

        if self.__decode_responses == 'True':
            self.__decode_responses = True
        elif self.__decode_responses == 'False' or self.__decode_responses is None:
            self.__decode_responses = False
        else:
            raise ValueError("REDIS_DECODE_RESPONSES must be True or False or None")
        if not any([self.__url, self.__port, self.__password, self.__decode_responses]):
            raise ValueError("Redis URL, port, password and decode_responses must be set")
    
    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def port(self) -> int:
        return self.__port
    
    @property
    def username(self) -> str:
        return self.__username
    
    @property
    def password(self) -> str:
        return self.__password
    
    @property
    def decode_responses(self) -> bool:
        return self.__decode_responses
    
    @property
    def socket_connect_timeout(self) -> float:
        return self.__socket_connect_timeout
    
    @property
    def socket_timeout(self) -> float:
        return self.__socket_timeout