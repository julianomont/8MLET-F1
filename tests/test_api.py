from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """Testa o endpoint de saúde da API."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "saudável"
    assert "database" in data

def test_login_admin():
    """Testa o login com usuário admin."""
    # Credenciais padrão do admin
    login_data = {
        "username": "admin",
        "password": "admin-8MLET"
    }
    # O endpoint espera form-data para OAuth2PasswordRequestForm
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
