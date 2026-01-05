import os
from dotenv import load_dotenv

class CORSConfig:
    def __init__(self):
        load_dotenv()
        self.__cors_origins = os.getenv("CORS_ORIGINS")
        self.__cors_origins_list = [origin.strip() for origin in self.__cors_origins.split(",") if origin.strip()]

    @property
    def cors_origins_list(self):
        return self.__cors_origins_list