import sqlite3
from backend.conexao import conectar

def inserir_usuario(nome: str, login: str, senha: str, funcao: str) -> int:
    """
    Insere um novo usuário no banco e retorna seu ID.
    A senha é armazenada em texto plano para fins acadêmicos.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, login, senha, funcao) VALUES (?, ?, ?, ?);",
            (nome, login, senha, funcao)
        )
        return cursor.lastrowid

def listar_usuarios() -> list[dict]:
    """
    Retorna a lista de todos os usuários cadastrados.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario AS id, nome, login, senha, funcao FROM usuarios;")
        return [dict(row) for row in cursor.fetchall()]

def autenticar_usuario(login: str, senha: str) -> dict | None:
    """
    Consulta o banco de dados e retorna o dicionário contendo os dados do usuário
    (id, nome, login, funcao) se o login e a senha coincidirem. Retorna None caso contrário.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario AS id, nome, login, funcao FROM usuarios WHERE login = ? AND senha = ?;",
            (login, senha)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
