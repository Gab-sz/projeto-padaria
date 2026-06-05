import os
import sqlite3
from contextlib import contextmanager

# Define o caminho absoluto para o banco de dados baseado na localização deste arquivo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'banco', 'padaria.db')

@contextmanager
def conectar():
    """
    Gerenciador de contexto para conexão segura com o banco de dados SQLite.
    Garante que PRAGMA foreign_keys = ON esteja ativado, realiza commit
    em caso de sucesso, rollback em exceções e fecha a conexão no final.
    """
    conexao = sqlite3.connect(DB_PATH)
    try:
        conexao.execute("PRAGMA foreign_keys = ON;")
        yield conexao
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        raise e
    finally:
        conexao.close()

def testar_conexao() -> bool:
    """
    Valida a conexão com o banco de dados executando uma consulta de teste.
    Retorna True em caso de sucesso e False caso contrário.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sqlite_version();")
            cursor.fetchone()
        return True
    except Exception:
        return False
