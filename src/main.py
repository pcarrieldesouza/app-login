# app.py
from flask import Flask, request, session, render_template_string

app = Flask(__name__)
app.secret_key = "troque-este-segredo"

# "banco" simples (demo)
USERS = {
    "admin": "admin123",
    "joao":  "senha123",
    "maria": "123456",
}

PAGE = """
<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Login simples</title>
<style>
  :root{--bg:#0f172a;--panel:#111827;--text:#e5e7eb;--muted:#94a3b8;--ok:#22c55e;--err:#ef4444;}
  *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--text);font-family:system-ui,Segoe UI,Roboto,Arial}
  .wrap{max-width:360px;margin:6vh auto;padding:20px;background:var(--panel);border-radius:14px}
  h1{margin:0 0 12px;font-size:20px} label{font-size:14px;color:var(--muted)}
  input{width:100%;padding:10px;border-radius:10px;border:1px solid #1f2937;background:#0b1220;color:var(--text);margin-top:6px}
  .row{margin:10px 0}
  button{width:100%;padding:10px;border:0;border-radius:10px;background:#2563eb;color:#fff;cursor:pointer}
  .muted{color:var(--muted);font-size:12px;margin-top:6px}
  .err{color:var(--err);font-size:14px}
  .ok{color:var(--ok);font-size:14px}
</style>
</head>
<body>
  <div class="wrap">
    {% if not user %}
      <h1>Entrar</h1>
      {% if error %}<div class="err">{{ error }}</div>{% endif %}
      <form method="post" action="/login">
        <div class="row">
          <label>Usuário</label>
          <input name="username" autocomplete="username" autofocus>
        </div>
        <div class="row">
          <label>Senha</label>
          <input name="password" type="password" autocomplete="current-password">
        </div>
        <div class="row">
          <button>Entrar</button>
        </div>
      </form>
      <div class="muted">Dica: admin / admin123</div>
    {% else %}
      <h1>Bem-vindo, {{ user }}!</h1>
      <div class="ok">Login realizado com sucesso.</div>
      <form method="post" action="/logout" class="row">
        <button>Logout</button>
      </form>
      <p class="muted">Esta é a mesma página, só que autenticada.</p>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    # se logado, mostra "bem-vindo"; se não, mostra formulário
    return render_template_string(PAGE, user=session.get("user"), error=None)

@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username", "").strip()
    p = request.form.get("password", "")
    if u and USERS.get(u) == p:
        session["user"] = u
        return render_template_string(PAGE, user=u, error=None)
    return render_template_string(PAGE, user=None, error="Usuário ou a senha está invalidos.")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return render_template_string(PAGE, user=None, error=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
