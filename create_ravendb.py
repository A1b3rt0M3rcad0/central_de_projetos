import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAVEN_URL = os.getenv("RAVEN_URL")
RAVEN_DATABASE = os.getenv("RAVEN_DATABASE")

if not RAVEN_URL or not RAVEN_DATABASE:
    raise RuntimeError("RAVEN_URL e RAVEN_DATABASE são obrigatórios")

url = f"{RAVEN_URL}/admin/databases"

payload = {
    "DatabaseName": RAVEN_DATABASE,
    "Settings": {}
}

response = requests.put(url, json=payload)

if response.status_code in (200, 201):
    print(f"✅ Database '{RAVEN_DATABASE}' criada com sucesso")
elif response.status_code == 409:
    print(f"ℹ️ Database '{RAVEN_DATABASE}' já existe")
else:
    print("❌ Erro ao criar database")
    print("Status:", response.status_code)
    print(response.text)
    response.raise_for_status()