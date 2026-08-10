from app import db, Autenticacao, User, app
from werkzeug.security import check_password_hash

app.app_context().push()

users = User.query.all()
print("=== USUÁRIOS ===")
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

auths = Autenticacao.query.all()
print("\n=== AUTENTICAÇÕES ===")
for auth in auths:
    print(f"ID: {auth.id}, Usuario ID: {auth.usuario_id}, Email: {auth.email}")
    print(f"Senha Hash: {auth.senha_hash}")
    resultado = check_password_hash(auth.senha_hash, "password123")
    print(f"check_password_hash('password123'): {resultado}")