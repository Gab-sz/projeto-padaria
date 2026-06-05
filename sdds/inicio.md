# Especificação de Desenvolvimento - Fase 1: Infraestrutura de Banco e Conexão

**Contexto:**
Você está atuando como um Desenvolvedor Backend Python Sênior. Sua tarefa é construir a fundação de um sistema desktop de gestão para uma padaria (Módulo Operacional). O primeiro passo é implementar a infraestrutura do banco de dados SQLite e o gerenciador de conexões seguro.

**Regras Arquiteturais Estritas:**
1. Zero acoplamento com a interface gráfica. O código deve conter apenas lógica de backend (Python puro e biblioteca `sqlite3`).
2. Utilize o padrão de *Context Manager* para a conexão com o banco.
3. O banco de dados deve utilizar obrigatoriamente `PRAGMA foreign_keys = ON;` para garantir a integridade referencial.
4. Evite variáveis globais soltas.

**Tarefas de Implementação:**

### 1. Arquivo: `backend/conexao.py`
* **Objetivo:** Criar um gerenciador de contexto seguro para transações no banco de dados.
* **Requisitos:**
    * Definir o caminho do banco como `DB_PATH = 'banco/padaria.db'`.
    * Criar a função `conectar()` decorada com `@contextmanager` da biblioteca `contextlib`.
    * A função deve abrir a conexão, ativar as chaves estrangeiras (`PRAGMA foreign_keys = ON`), usar `yield` para entregar a conexão ao bloco chamador, executar `commit()` em caso de sucesso, `rollback()` em caso de exceção (utilizando bloco `try/except`) e fechar a conexão no `finally`.
    * Criar uma função utilitária `testar_conexao() -> bool` que tenta fazer um `SELECT sqlite_version();` para validar se o banco está respondendo.

### 2. Arquivo: `banco/setup.py`
* **Objetivo:** Criar o script DDL (Data Definition Language) que inicializa o banco de dados e cria as tabelas caso não existam.
* **Requisitos:**
    * Importar o gerenciador `conectar` de `backend.conexao`.
    * Criar a função `criar_tabelas()`.
    * Dentro de um bloco `with conectar() as conn:`, executar o seguinte script SQL consolidado:

```sql
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

**Formato da Entrega:**
Gere estritamente o código-fonte funcional em blocos separados para cada um dos dois arquivos citados (`conexao.py` e `setup.py`). Não adicione explicações detalhadas ou textos complementares; forneça apenas o código Python estruturado e formatado (PEP 8).
