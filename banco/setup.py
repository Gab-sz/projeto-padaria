import os
import sys

# Adiciona o diretório raiz ao sys.path para garantir que os módulos do backend possam ser importados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.conexao import conectar

def criar_tabelas():
    """
    Executa o script DDL para criar as tabelas necessárias no banco de dados.
    """
    # Garante que o diretório para o banco de dados exista
    os.makedirs('banco', exist_ok=True)
    
    ddl_script = """
    -- 1. Tabelas de Domínio
    CREATE TABLE IF NOT EXISTS "categorias_produto" (
        "id_categoria_produto" INTEGER NOT NULL UNIQUE,
        "nome" TEXT NOT NULL UNIQUE,
        "descricao" TEXT,
        PRIMARY KEY("id_categoria_produto" AUTOINCREMENT)
    );

    CREATE TABLE IF NOT EXISTS "categorias_financeiras" (
        "id_categoria_financeira" INTEGER NOT NULL UNIQUE,
        "nome" TEXT NOT NULL UNIQUE,
        "tipo_movimentacao" TEXT NOT NULL,
        PRIMARY KEY("id_categoria_financeira" AUTOINCREMENT)
    );

    -- 2. Entidades Base
    CREATE TABLE IF NOT EXISTS "usuarios" (
        "id_usuario" INTEGER NOT NULL UNIQUE,
        "nome" TEXT NOT NULL,
        "login" TEXT NOT NULL UNIQUE,
        "senha" TEXT NOT NULL,
        "funcao" TEXT,
        PRIMARY KEY("id_usuario" AUTOINCREMENT)
    );

    CREATE TABLE IF NOT EXISTS "insumos" (
        "id_insumo" INTEGER NOT NULL UNIQUE,
        "nome" TEXT NOT NULL,
        "categoria" TEXT NOT NULL,
        "quantidade_atual" REAL NOT NULL,
        "unidade_medida" TEXT NOT NULL,
        "estoque_minimo" REAL NOT NULL,
        "data_atualizacao" INTEGER NOT NULL,
        PRIMARY KEY("id_insumo" AUTOINCREMENT)
    );

    CREATE TABLE IF NOT EXISTS "produtos" (
        "id_produto" INTEGER NOT NULL UNIQUE,
        "id_categoria_produto" INTEGER NOT NULL,
        "nome" TEXT NOT NULL,
        "preco_venda" REAL NOT NULL,
        "custo_producao" REAL NOT NULL,
        PRIMARY KEY("id_produto" AUTOINCREMENT),
        FOREIGN KEY("id_categoria_produto") REFERENCES "categorias_produto"("id_categoria_produto")
    );

    -- 3. Entidade Associativa (Ficha Técnica)
    CREATE TABLE IF NOT EXISTS "produto_insumos" (
        "id_produto" INTEGER NOT NULL,
        "id_insumo" INTEGER NOT NULL,
        "quantidade_necessaria" REAL NOT NULL,
        PRIMARY KEY("id_produto", "id_insumo"),
        FOREIGN KEY("id_produto") REFERENCES "produtos"("id_produto"),
        FOREIGN KEY("id_insumo") REFERENCES "insumos"("id_insumo")
    );

    -- 4. Financeiro
    CREATE TABLE IF NOT EXISTS "despesas" (
        "id_despesa" INTEGER NOT NULL UNIQUE,
        "id_categoria_financeira" INTEGER NOT NULL,
        "id_usuario" INTEGER NOT NULL,
        "descricao" TEXT NOT NULL,
        "valor_despesa" REAL NOT NULL,
        "data_despesa" INTEGER NOT NULL,
        PRIMARY KEY("id_despesa" AUTOINCREMENT),
        FOREIGN KEY("id_categoria_financeira") REFERENCES "categorias_financeiras"("id_categoria_financeira"),
        FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id_usuario")
    );

    CREATE TABLE IF NOT EXISTS "recebimentos" (
        "id_recebimento" INTEGER NOT NULL UNIQUE,
        "id_usuario" INTEGER NOT NULL,
        "categoria" TEXT NOT NULL,
        "descricao" TEXT NOT NULL,
        "valor_recebido" REAL NOT NULL,
        "data_recebimento" INTEGER NOT NULL,
        PRIMARY KEY("id_recebimento" AUTOINCREMENT),
        FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id_usuario")
    );

    -- 5. Operacional (PDV)
    CREATE TABLE IF NOT EXISTS "vendas" (
        "id_venda" INTEGER NOT NULL UNIQUE,
        "id_usuario" INTEGER NOT NULL,
        "valor_total" REAL NOT NULL,
        "forma_pagamento" TEXT NOT NULL,
        "data_venda" INTEGER NOT NULL,
        PRIMARY KEY("id_venda" AUTOINCREMENT),
        FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id_usuario")
    );

    CREATE TABLE IF NOT EXISTS "itens_venda" (
        "id_item" INTEGER NOT NULL UNIQUE,
        "id_venda" INTEGER NOT NULL,
        "id_produto" INTEGER NOT NULL,
        "quantidade" REAL NOT NULL,
        "valor_unitario" REAL NOT NULL,
        "subtotal" REAL NOT NULL,
        PRIMARY KEY("id_item" AUTOINCREMENT),
        FOREIGN KEY("id_venda") REFERENCES "vendas"("id_venda"),
        FOREIGN KEY("id_produto") REFERENCES "produtos"("id_produto")
    );
    """
    
    with conectar() as conn:
        conn.executescript(ddl_script)

if __name__ == '__main__':
    criar_tabelas()
    print("Banco de dados inicializado e tabelas criadas com sucesso.")
