import sqlite3
from backend.conexao import conectar

def inserir_produto(id_categoria_produto: int, nome: str, preco_venda: float, custo_producao: float) -> int:
    """
    Insere um novo produto no catálogo e retorna o ID gerado.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO produtos (id_categoria_produto, nome, preco_venda, custo_producao)
            VALUES (?, ?, ?, ?);
            """,
            (id_categoria_produto, nome, preco_venda, custo_producao)
        )
        return cursor.lastrowid

def listar_produtos() -> list[dict]:
    """
    Retorna a lista de produtos cadastrados.
    Utiliza INNER JOIN com categorias_produto para retornar as chaves:
    id, nome, categoria_nome, preco_venda, custo_producao.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.id_produto AS id, p.nome, c.nome AS categoria_nome, p.preco_venda, p.custo_producao
            FROM produtos p
            INNER JOIN categorias_produto c ON p.id_categoria_produto = c.id_categoria_produto;
            """
        )
        return [dict(row) for row in cursor.fetchall()]

def vincular_ficha_tecnica(id_produto: int, id_insumo: int, quantidade_necessaria: float) -> None:
    """
    Vincula um insumo à ficha técnica de um produto, indicando a quantidade necessária.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO produto_insumos (id_produto, id_insumo, quantidade_necessaria)
            VALUES (?, ?, ?);
            """,
            (id_produto, id_insumo, quantidade_necessaria)
        )

def obter_ficha_tecnica(id_produto: int) -> list[dict]:
    """
    Lista os insumos necessários para um produto específico, trazendo o nome do insumo,
    unidade de medida e quantidade necessária através de um JOIN com a tabela insumos.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT pi.id_insumo, i.nome AS insumo_nome, i.unidade_medida, pi.quantidade_necessaria
            FROM produto_insumos pi
            INNER JOIN insumos i ON pi.id_insumo = i.id_insumo
            WHERE pi.id_produto = ?;
            """,
            (id_produto,)
        )
        return [dict(row) for row in cursor.fetchall()]
