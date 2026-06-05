import sqlite3
import time
from backend.conexao import conectar

def inserir_insumo(nome: str, categoria: str, quantidade_atual: float, unidade_medida: str, estoque_minimo: float) -> int:
    """
    Insere um novo insumo (matéria-prima) no estoque e retorna o ID gerado.
    O campo data_atualizacao é preenchido com o Unix Timestamp atual.
    """
    data_atualizacao = int(time.time())
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO insumos (nome, categoria, quantidade_atual, unidade_medida, estoque_minimo, data_atualizacao)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (nome, categoria, quantidade_atual, unidade_medida, estoque_minimo, data_atualizacao)
        )
        return cursor.lastrowid

def listar_insumos() -> list[dict]:
    """
    Retorna todos os insumos cadastrados no inventário.
    """
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_insumo, nome, categoria, quantidade_atual, unidade_medida, estoque_minimo, data_atualizacao
            FROM insumos;
            """
        )
        return [dict(row) for row in cursor.fetchall()]

def atualizar_quantidade_insumo(id_insumo: int, variacao: float) -> None:
    """
    Atualiza a quantidade atual de um insumo, adicionando ou subtraindo o valor de variacao.
    O campo data_atualizacao é atualizado para o Unix Timestamp atual.
    """
    data_atualizacao = int(time.time())
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE insumos
            SET quantidade_atual = quantidade_atual + ?, data_atualizacao = ?
            WHERE id_insumo = ?;
            """,
            (variacao, data_atualizacao, id_insumo)
        )
