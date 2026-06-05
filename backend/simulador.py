import os
import sys
import sqlite3
import random
import time
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao sys.path para garantir o funcionamento das importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.conexao import conectar
from banco.setup import criar_tabelas

def semear_dados_iniciais(conn) -> tuple[list[int], list[dict]]:
    """
    Semeia dados iniciais no banco caso esteja vazio ou com poucos registros,
    retornando as listas de IDs de usuários e dicionários de produtos.
    """
    cursor = conn.cursor()
    
    # 1. Garante que haja pelo menos um usuário
    cursor.execute("SELECT id_usuario FROM usuarios;")
    usuarios = [row[0] for row in cursor.fetchall()]
    if not usuarios:
        cursor.execute(
            "INSERT INTO usuarios (nome, login, senha) VALUES (?, ?, ?);",
            ("Caixa Simulador", "caixa_simulador", "simula123")
        )
        usuarios = [cursor.lastrowid]
        print("Usuário de simulação 'Caixa Simulador' criado.")
        
    # 2. Garante que haja pelo menos uma categoria de produto
    cursor.execute("SELECT id_categoria_produto FROM categorias_produto;")
    cat_rows = cursor.fetchall()
    if not cat_rows:
        cursor.execute(
            "INSERT INTO categorias_produto (nome, descricao) VALUES (?, ?);",
            ("Padaria", "Pães e derivados")
        )
        cat_id = cursor.lastrowid
        print("Categoria de simulação 'Padaria' criada.")
    else:
        cat_id = cat_rows[0][0]
        
    # 3. Garante que haja produtos suficientes (mínimo 6) para permitir variação no carrinho
    cursor.execute("SELECT id_produto, preco_venda FROM produtos;")
    produtos = [dict(id_produto=row[0], preco_venda=row[1]) for row in cursor.fetchall()]
    
    if len(produtos) < 6:
        produtos_novos = [
            ("Pão Francês 50g", 0.50, 0.15),
            ("Café Espresso", 4.00, 1.00),
            ("Leite Integral 1L", 5.00, 3.50),
            ("Bolo de Cenoura", 18.00, 6.00),
            ("Pão de Queijo", 3.00, 1.00),
            ("Salgado Assado", 6.00, 2.50),
            ("Suco Natural 300ml", 7.00, 2.50)
        ]
        for nome, preco, custo in produtos_novos:
            cursor.execute("SELECT id_produto FROM produtos WHERE nome = ?;", (nome,))
            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO produtos (id_categoria_produto, nome, preco_venda, custo_producao)
                    VALUES (?, ?, ?, ?);
                    """,
                    (cat_id, nome, preco, custo)
                )
        print("Produtos de simulação adicionais criados.")
        
        cursor.execute("SELECT id_produto, preco_venda FROM produtos;")
        produtos = [dict(id_produto=row[0], preco_venda=row[1]) for row in cursor.fetchall()]
        
    return usuarios, produtos

def gerar_hora_minuto_segundo() -> tuple[int, int, int]:
    """
    Retorna uma tupla (hora, minuto, segundo) simulando horários de pico.
    Cerca de 70% das vendas ocorrem nos horários de pico: 06h-09h e 16h-19h.
    """
    if random.random() < 0.70:
        # Horários de pico (06h às 08h59 e 16h às 18h59)
        if random.random() < 0.5:
            hora = random.randint(6, 8)
        else:
            hora = random.randint(16, 18)
    else:
        # Fora de pico (00h-05h, 09h-15h, 19h-23h)
        hora = random.choice([
            random.randint(0, 5),
            random.randint(9, 15),
            random.randint(19, 23)
        ])
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)
    return hora, minuto, segundo

def executar_simulacao(total_vendas: int = 40000):
    """
    Simula um volume massivo de vendas dos últimos 2 anos e insere em lote (bulk insert).
    """
    print("Garantindo estrutura do banco de dados...")
    criar_tabelas()
    
    tempo_inicial = time.time()
    
    with conectar() as conn:
        cursor = conn.cursor()
        
        # Limpa dados anteriores de vendas para garantir uma simulação limpa e controlada
        print("Limpando dados de vendas anteriores...")
        cursor.execute("DELETE FROM itens_venda;")
        cursor.execute("DELETE FROM vendas;")
        
        # Garante dados básicos e obtém as entidades para vinculação
        usuarios, produtos = semear_dados_iniciais(conn)
        
        # Obtém o maior id_venda para evitar colisões (será 1 após a limpeza)
        cursor.execute("SELECT COALESCE(MAX(id_venda), 0) FROM vendas;")
        proximo_venda_id = cursor.fetchone()[0] + 1
        
        print(f"Iniciando simulação de {total_vendas} vendas em memória...")
        
        vendas_data = []
        itens_venda_data = []
        
        formas_pagamento = ["DINHEIRO", "PIX", "DÉBITO", "CRÉDITO"]
        hoje = datetime.now()
        
        for i in range(total_vendas):
            id_venda = proximo_venda_id + i
            id_usuario = random.choice(usuarios)
            forma_pagamento = random.choice(formas_pagamento)
            
            # Distribuição ao longo dos últimos 730 dias (2 anos)
            dias_retroativos = random.randint(0, 729)
            hora, minuto, segundo = gerar_hora_minuto_segundo()
            
            data_venda_dt = hoje - timedelta(days=dias_retroativos)
            data_venda_dt = data_venda_dt.replace(hour=hora, minute=minuto, second=segundo, microsecond=0)
            data_venda = int(data_venda_dt.timestamp())
            
            # Cada venda tem de 1 a 4 itens
            num_itens = random.randint(1, 4)
            produtos_carrinho = random.sample(produtos, min(num_itens, len(produtos)))
            
            valor_total = 0.0
            
            for prod in produtos_carrinho:
                id_produto = prod["id_produto"]
                preco_unitario = prod["preco_venda"]
                
                # Quantidades inteiras simples para simulação
                quantidade = float(random.randint(1, 5))
                subtotal = quantidade * preco_unitario
                valor_total += subtotal
                
                itens_venda_data.append((
                    id_venda,
                    id_produto,
                    quantidade,
                    preco_unitario,
                    subtotal
                ))
                
            vendas_data.append((
                id_venda,
                id_usuario,
                valor_total,
                forma_pagamento,
                data_venda
            ))
            
        print("Gravando dados no banco de dados (inserção em lote)...")
        
        # Bulk Insert das vendas
        cursor.executemany(
            """
            INSERT INTO vendas (id_venda, id_usuario, valor_total, forma_pagamento, data_venda)
            VALUES (?, ?, ?, ?, ?);
            """,
            vendas_data
        )
        
        # Bulk Insert dos itens de venda
        cursor.executemany(
            """
            INSERT INTO itens_venda (id_venda, id_produto, quantidade, valor_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?);
            """,
            itens_venda_data
        )
        
    tempo_final = time.time()
    duracao = tempo_final - tempo_inicial
    
    print(f"\n--- Simulação Concluída ---")
    print(f"Vendas inseridas: {len(vendas_data)}")
    print(f"Itens de venda inseridos: {len(itens_venda_data)}")
    print(f"Tempo total de execução: {duracao:.2f} segundos")

if __name__ == '__main__':
    executar_simulacao()
