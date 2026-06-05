import sqlite3
from backend.conexao import conectar

def inserir_categoria_produto(nome: str, descricao: str = None) -> int:
    """
    Insere uma nova categoria de produto e retorna o ID gerado.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categorias_produto (nome, descricao) VALUES (?, ?);",
            (nome, descricao)
        )
        return cursor.lastrowid

def listar_categorias_produto() -> list[dict]:
    """
    Retorna a lista de todas as categorias de produto.
    Cada categoria é representada por um dicionário com as chaves: id, nome, descricao.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria_produto AS id, nome, descricao FROM categorias_produto;")
        return [dict(row) for row in cursor.fetchall()]

def inserir_categoria_financeira(nome: str, tipo_movimentacao: str) -> int:
    """
    Insere uma nova categoria financeira e retorna o ID gerado.
    Valida se tipo_movimentacao é obrigatoriamente 'ENTRADA' ou 'SAIDA'.
    """
    tipo_movimentacao_upper = tipo_movimentacao.upper()
    if tipo_movimentacao_upper not in ('ENTRADA', 'SAIDA'):
        raise ValueError("O tipo_movimentacao deve ser obrigatoriamente 'ENTRADA' ou 'SAIDA'.")
        
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categorias_financeiras (nome, tipo_movimentacao) VALUES (?, ?);",
            (nome, tipo_movimentacao_upper)
        )
        return cursor.lastrowid

def listar_categorias_financeiras(tipo: str = None) -> list[dict]:
    """
    Retorna a lista de categorias financeiras, opcionalmente filtrada pelo tipo.
    """
    query = "SELECT id_categoria_financeira AS id, nome, tipo_movimentacao FROM categorias_financeiras"
    params = ()
    
    if tipo is not None:
        tipo_upper = tipo.upper()
        if tipo_upper not in ('ENTRADA', 'SAIDA'):
            raise ValueError("O filtro de tipo deve ser 'ENTRADA' ou 'SAIDA'.")
        query += " WHERE tipo_movimentacao = ?;"
        params = (tipo_upper,)
    else:
        query += ";"
        
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
