from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
try:
    response = client.post("/api/register", json={"username": "test_register_2", "password": "123"})
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
