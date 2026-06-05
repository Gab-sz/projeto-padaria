import sqlite3
import time
from backend.conexao import conectar

def inserir_despesa(id_categoria_financeira: int, id_usuario: int, descricao: str, valor_despesa: float) -> int:
    """
    Insere uma despesa e retorna seu ID. A data é gravada em Unix Timestamp.
    """
    data_despesa = int(time.time())
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO despesas (id_categoria_financeira, id_usuario, descricao, valor_despesa, data_despesa)
            VALUES (?, ?, ?, ?, ?);
            """,
            (id_categoria_financeira, id_usuario, descricao, valor_despesa, data_despesa)
        )
        return cursor.lastrowid

def listar_despesas() -> list[dict]:
    """
    Retorna a lista de despesas cadastradas no banco de dados.
    Utiliza INNER JOIN com categorias_financeiras e usuarios para expor nomes legíveis.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT d.id_despesa AS id, d.id_categoria_financeira, cf.nome AS categoria_nome,
                   d.id_usuario, u.nome AS usuario_nome, d.descricao, d.valor_despesa, d.data_despesa
            FROM despesas d
            INNER JOIN categorias_financeiras cf ON d.id_categoria_financeira = cf.id_categoria_financeira
            INNER JOIN usuarios u ON d.id_usuario = u.id_usuario;
            """
        )
        return [dict(row) for row in cursor.fetchall()]

def inserir_recebimento(id_usuario: int, categoria_texto: str, descricao: str, valor_recebido: float) -> int:
    """
    Insere um recebimento e retorna seu ID. A data é gravada em Unix Timestamp.
    """
    data_recebimento = int(time.time())
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recebimentos (id_usuario, categoria, descricao, valor_recebido, data_recebimento)
            VALUES (?, ?, ?, ?, ?);
            """,
            (id_usuario, categoria_texto, descricao, valor_recebido, data_recebimento)
        )
        return cursor.lastrowid

def listar_recebimentos() -> list[dict]:
    """
    Retorna a lista de recebimentos avulsos cadastrados.
    Utiliza INNER JOIN com usuarios para trazer o nome do operador.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT r.id_recebimento AS id, r.id_usuario, u.nome AS usuario_nome,
                   r.categoria, r.descricao, r.valor_recebido, r.data_recebimento
            FROM recebimentos r
            INNER JOIN usuarios u ON r.id_usuario = u.id_usuario;
            """
        )
        return [dict(row) for row in cursor.fetchall()]
