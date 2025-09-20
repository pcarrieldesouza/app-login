import pytest
from src.main import app  # importa o app definido no main.py

#Teste Unitários 5 testes
@pytest.fixture()
def client():
    app.config.update(TESTING=True, SECRET_KEY="testing-secret")
    with app.test_client() as client:
        yield client

def test_pytest_esta_funcionando():
    assert 1 + 1 == 2

def test_index_mostra_formulario_quando_deslogado(client):
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Entrar" in html
    assert "Bem-vindo" not in html

def test_login_sucesso_mostra_bemvindo_e_sessao(client):
    resp = client.post("/login", data={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Bem-vindo, admin!" in html
    with client.session_transaction() as sess:
        assert sess.get("user") == "admin"

def test_login_falha_mostra_erro(client):
    resp = client.post("/login", data={"username": "admin", "password": "errada"})
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Usuário ou senha inválido." in html
    with client.session_transaction() as sess:
        assert sess.get("user") is None

def test_logout_limpa_sessao(client):
    client.post("/login", data={"username": "maria", "password": "123456"})
    with client.session_transaction() as sess:
        assert sess.get("user") == "maria"
    resp = client.post("/logout")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Entrar" in html
    assert "Bem-vindo" not in html
    with client.session_transaction() as sess:
        assert sess.get("user") is None
