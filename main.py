#pylint:disable=W0611,R1719
from src.main.app import app
import uvicorn
import dotenv
import os

if __name__ == "__main__":
    dotenv.load_dotenv()
    HOMOLOG = os.getenv("HOMOLOGACAO")
    uvicorn.run(
        "main:app",
        reload=True if HOMOLOG == "True" else False
    )