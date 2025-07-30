import json
from fastapi.testclient import TestClient
from src.main.app import app

client = TestClient(app)

with open("docs/openapi.json", "w", encoding="utf-8") as f:
    json.dump(client.get("/openapi.json").json(), f, indent=2, ensure_ascii=False)