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

def executar_simulacao(total_vendas: int = 10000):
    """
    Executa a simulação completa para popular o banco de dados com uma massa de dados
    retroativa realista para os últimos 6 meses (180 dias).
    Garante integridade referencial e usa Bulk Inserts (executemany) para alta performance.
    """
    tempo_inicial = time.time()
    
    # 1. Garante que as tabelas existam
    criar_tabelas()
    
    with conectar() as conn:
        cursor = conn.cursor()
        
        # Ativa chaves estrangeiras explicitamente na conexão da simulação
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 2. Limpeza de dados das tabelas operacionais e cadastrais (preservando usuarios)
        print("Limpando dados anteriores...")
        cursor.execute("DELETE FROM itens_venda;")
        cursor.execute("DELETE FROM vendas;")
        cursor.execute("DELETE FROM despesas;")
        cursor.execute("DELETE FROM recebimentos;")
        cursor.execute("DELETE FROM produto_insumos;")
        cursor.execute("DELETE FROM produtos;")
        cursor.execute("DELETE FROM insumos;")
        cursor.execute("DELETE FROM categorias_produto;")
        cursor.execute("DELETE FROM categorias_financeiras;")
        
        # 3. Usuário de Testes Único
        cursor.execute("SELECT id_usuario FROM usuarios;")
        usuarios_existentes = cursor.fetchall()
        
        if not usuarios_existentes:
            cursor.execute(
                """
                INSERT INTO usuarios (nome, login, senha, funcao)
                VALUES (?, ?, ?, ?);
                """,
                ("Usuario Teste", "admin", "123", "admin")
            )
            id_usuario_teste = cursor.lastrowid
            print(f"Usuário de testes único 'admin' criado (ID: {id_usuario_teste}).")
        else:
            # Usar o primeiro usuário existente para as vendas e despesas
            id_usuario_teste = usuarios_existentes[0][0]
            
        # Re-selecionar todos os IDs de usuários para a simulação
        cursor.execute("SELECT id_usuario FROM usuarios;")
        ids_usuarios = [row[0] for row in cursor.fetchall()]
        
        # 4. Infraestrutura de Categorias de Produtos
        categorias_prod = [
            ("Panificação", "Pães, bolos e doces fabricados na padaria"),
            ("Laticínios", "Leites, queijos, manteigas e iogurtes"),
            ("Bebidas", "Sucos, refrigerantes, águas e cafés"),
            ("Secos", "Mercearia de prateleira e doces industriais"),
            ("Perecíveis", "Salgados assados, lanches e frios"),
            ("Limpeza", "Produtos de higiene e limpeza do local"),
            ("Embalagens", "Sacolas, copos, papéis e caixas para viagem")
        ]
        
        cat_prod_map = {}
        for nome, desc in categorias_prod:
            cursor.execute(
                "INSERT INTO categorias_produto (nome, descricao) VALUES (?, ?);",
                (nome, desc)
            )
            cat_prod_map[nome] = cursor.lastrowid
            
        # 5. Infraestrutura de Categorias Financeiras
        categorias_fin = [
            ("Contas de Consumo", "SAIDA"),
            ("Fornecedores", "SAIDA"),
            ("Aluguel", "SAIDA"),
            ("Folha de Pagamento", "SAIDA"),
            ("Manutenção", "SAIDA"),
            ("Aporte de Capital", "ENTRADA"),
            ("Encomendas Especiais", "ENTRADA")
        ]
        
        cat_fin_map = {}
        for nome, tipo in categorias_fin:
            cursor.execute(
                "INSERT INTO categorias_financeiras (nome, tipo_movimentacao) VALUES (?, ?);",
                (nome, tipo)
            )
            cat_fin_map[nome] = cursor.lastrowid
            
        # 6. Cadastro de Insumos (Estoque)
        # Nota: Tabela de insumos não possui a coluna 'categoria' conforme requisitos atualizados
        insumos_data = [
            ("Farinha de Trigo", 150.0, "KG", 20.0),
            ("Açúcar Refinado", 100.0, "KG", 10.0),
            ("Ovos", 300.0, "UN", 24.0),
            ("Manteiga", 60.0, "KG", 8.0),
            ("Leite Integral", 120.0, "L", 15.0)
        ]
        
        data_atual = int(time.time())
        insumos_map = {}
        for nome, qtd_ini, unid, est_min in insumos_data:
            cursor.execute(
                """
                INSERT INTO insumos (nome, quantidade_atual, unidade_medida, estoque_minimo, data_atualizacao)
                VALUES (?, ?, ?, ?, ?);
                """,
                (nome, qtd_ini, unid, est_min, data_atual)
            )
            insumos_map[nome] = cursor.lastrowid
            
        # 7. Cadastro do Catálogo de Produtos (20 itens no total)
        # 10 Produtos com Ficha Técnica
        produtos_com_ficha = [
            ("Pão Francês 50g", 0.50, 0.15, "Panificação", [("Farinha de Trigo", 0.045)]),
            ("Bolo de Cenoura", 18.00, 6.00, "Panificação", [("Farinha de Trigo", 0.200), ("Açúcar Refinado", 0.150), ("Ovos", 3.0), ("Manteiga", 0.050)]),
            ("Croissant Presunto/Queijo", 7.50, 2.50, "Panificação", [("Farinha de Trigo", 0.090), ("Manteiga", 0.040)]),
            ("Pão de Queijo Tradicional", 3.00, 1.00, "Panificação", [("Ovos", 0.4), ("Manteiga", 0.012)]),
            ("Coxinha de Frango", 6.00, 2.00, "Perecíveis", [("Farinha de Trigo", 0.075), ("Manteiga", 0.010)]),
            ("Bolo de Chocolate", 22.00, 7.50, "Panificação", [("Farinha de Trigo", 0.220), ("Açúcar Refinado", 0.200), ("Ovos", 3.0), ("Manteiga", 0.060)]),
            ("Pão de Forma Artesanal", 8.00, 2.80, "Panificação", [("Farinha de Trigo", 0.350), ("Manteiga", 0.025)]),
            ("Rosca de Coco Doce", 13.50, 4.50, "Panificação", [("Farinha de Trigo", 0.240), ("Açúcar Refinado", 0.090), ("Ovos", 1.0), ("Manteiga", 0.020)]),
            ("Sonho de Creme", 5.50, 1.90, "Panificação", [("Farinha de Trigo", 0.070), ("Açúcar Refinado", 0.025), ("Ovos", 0.5), ("Manteiga", 0.010)]),
            ("Esfiha de Carne Assada", 6.50, 2.30, "Perecíveis", [("Farinha de Trigo", 0.075), ("Manteiga", 0.010)])
        ]
        
        # 10 Produtos sem Ficha Técnica (Revenda Direta / Serviços)
        produtos_sem_ficha = [
            ("Refrigerante Coca-Cola Lata", 5.00, 2.20, "Bebidas"),
            ("Água Mineral sem Gás 500ml", 3.00, 0.80, "Bebidas"),
            ("Suco de Uva Del Valle 1L", 7.50, 3.90, "Bebidas"),
            ("Café Espresso Carioca", 4.50, 1.10, "Bebidas"),
            ("Sacola Ecológica Retornável", 2.50, 0.60, "Embalagens"),
            ("Alfajor Artesanal", 6.00, 2.80, "Secos"),
            ("Barra de Chocolate Lacta 90g", 8.50, 4.20, "Secos"),
            ("Ice Tea Pêssego 450ml", 5.50, 2.40, "Bebidas"),
            ("Cerveja Heineken Lata 350ml", 7.50, 3.90, "Bebidas"),
            ("Saco de Gelo Cubo 5kg", 12.00, 4.50, "Secos")
        ]
        
        produtos_cache = [] # Guarda dicionários com ID e preço
        
        # Salva produtos com ficha
        for nome, preco_venda, custo_prod, cat_nome, receita in produtos_com_ficha:
            id_cat = cat_prod_map[cat_nome]
            cursor.execute(
                """
                INSERT INTO produtos (id_categoria_produto, nome, preco_venda, custo_producao)
                VALUES (?, ?, ?, ?);
                """,
                (id_cat, nome, preco_venda, custo_prod)
            )
            id_prod = cursor.lastrowid
            produtos_cache.append({"id": id_prod, "preco_venda": preco_venda})
            
            # Vincula insumos na receita
            for ins_nome, qtd_nec in receita:
                id_ins = insumos_map[ins_nome]
                cursor.execute(
                    """
                    INSERT INTO produto_insumos (id_produto, id_insumo, quantidade_necessaria)
                    VALUES (?, ?, ?);
                    """,
                    (id_prod, id_ins, qtd_nec)
                )
                
        # Salva produtos sem ficha
        for nome, preco_venda, custo_prod, cat_nome in produtos_sem_ficha:
            id_cat = cat_prod_map[cat_nome]
            cursor.execute(
                """
                INSERT INTO produtos (id_categoria_produto, nome, preco_venda, custo_producao)
                VALUES (?, ?, ?, ?);
                """,
                (id_cat, nome, preco_venda, custo_prod)
            )
            id_prod = cursor.lastrowid
            produtos_cache.append({"id": id_prod, "preco_venda": preco_venda})
            
        print(f"Cadastrados {len(produtos_cache)} produtos base no catálogo.")
        
        # 8. Geração de Despesas e Recebimentos (Últimos 6 Meses)
        hoje = datetime.now()
        data_limite_retroativa = hoje - timedelta(days=180)
        
        despesas_data = []
        recebimentos_data = []
        
        total_despesas_injetadas = 0
        total_recebimentos_injetados = 0
        
        # Gerar movimentações financeiras por mês
        for m in range(6):
            data_mes = hoje - timedelta(days=m * 30)
            
            # Despesas Fixas (Salários e Aluguel) - Exatamente uma vez por mês
            # Folha de Pagamento
            timestamp_salarios = int((data_mes.replace(day=5, hour=10, minute=0, second=0)).timestamp())
            despesas_data.append((
                cat_fin_map["Folha de Pagamento"],
                random.choice(ids_usuarios),
                "Salários dos Funcionários",
                5200.00,
                timestamp_salarios
            ))
            total_despesas_injetadas += 1
            
            # Aluguel
            timestamp_aluguel = int((data_mes.replace(day=10, hour=10, minute=0, second=0)).timestamp())
            despesas_data.append((
                cat_fin_map["Aluguel"],
                random.choice(ids_usuarios),
                "Aluguel do Ponto Comercial",
                3200.00,
                timestamp_aluguel
            ))
            total_despesas_injetadas += 1
            
            # Despesas Variáveis Mensais (Luz, Água, Fornecedores, Manutenção)
            # Luz/Água (Contas de Consumo)
            timestamp_consumo = int((data_mes.replace(day=18, hour=14, minute=0, second=0)).timestamp())
            despesas_data.append((
                cat_fin_map["Contas de Consumo"],
                random.choice(ids_usuarios),
                "Conta mensal de Energia e Água",
                random.uniform(500.00, 950.00),
                timestamp_consumo
            ))
            total_despesas_injetadas += 1
            
            # Fornecedores (2 compras por mês)
            for f in range(2):
                dia_forn = random.randint(1, 28)
                timestamp_forn = int((data_mes.replace(day=dia_forn, hour=11, minute=0, second=0)).timestamp())
                despesas_data.append((
                    cat_fin_map["Fornecedores"],
                    random.choice(ids_usuarios),
                    f"Compra de insumos - lote #{random.randint(100, 999)}",
                    random.uniform(1200.00, 2800.00),
                    timestamp_forn
                ))
                total_despesas_injetadas += 1
                
            # Manutenção (uma vez a cada dois meses)
            if m % 2 == 0:
                timestamp_manut = int((data_mes.replace(day=22, hour=15, minute=0, second=0)).timestamp())
                despesas_data.append((
                    cat_fin_map["Manutenção"],
                    random.choice(ids_usuarios),
                    "Manutenção de Forno Industrial",
                    random.uniform(200.00, 600.00),
                    timestamp_manut
                ))
                total_despesas_injetadas += 1
                
            # Recebimentos Mensais
            # Aporte de Capital (2 aportes totais nos 6 meses)
            if m in (1, 4):
                timestamp_aporte = int((data_mes.replace(day=2, hour=9, minute=0, second=0)).timestamp())
                recebimentos_data.append((
                    random.choice(ids_usuarios),
                    "Aporte de Capital",
                    "Aporte de sócio investidor",
                    5000.00,
                    timestamp_aporte
                ))
                total_recebimentos_injetados += 1
                
            # Encomendas Especiais (3 por mês)
            for r in range(3):
                dia_rec = random.randint(1, 28)
                timestamp_rec = int((data_mes.replace(day=dia_rec, hour=16, minute=0, second=0)).timestamp())
                recebimentos_data.append((
                    random.choice(ids_usuarios),
                    "Encomendas Especiais",
                    f"Festa de Aniversário - Encomenda #{random.randint(10, 99)}",
                    random.uniform(250.00, 800.00),
                    timestamp_rec
                ))
                total_recebimentos_injetados += 1
                
        # Inserir despesas no banco
        cursor.executemany(
            """
            INSERT INTO despesas (id_categoria_financeira, id_usuario, descricao, valor_despesa, data_despesa)
            VALUES (?, ?, ?, ?, ?);
            """,
            despesas_data
        )
        
        # Inserir recebimentos no banco
        cursor.executemany(
            """
            INSERT INTO recebimentos (id_usuario, categoria, descricao, valor_recebido, data_recebimento)
            VALUES (?, ?, ?, ?, ?);
            """,
            recebimentos_data
        )
        
        # 9. Geração Massiva de 10.000 Vendas (Restrição de Horário Comercial)
        print(f"Iniciando simulação de {total_vendas} vendas com horários comerciais em memória...")
        
        vendas_list = []
        itens_venda_list = []
        
        formas_pagamento = ["PIX", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"]
        
        # Obter o ID de início de auto-incremento
        cursor.execute("SELECT COALESCE(MAX(id_venda), 0) FROM vendas;")
        proximo_venda_id = cursor.fetchone()[0] + 1
        
        # Distribuição de vendas ao longo dos 180 dias
        for i in range(total_vendas):
            id_venda = proximo_venda_id + i
            id_usuario = random.choice(ids_usuarios)
            forma_pagamento = random.choice(formas_pagamento)
            
            # Distribui de forma aleatória nos últimos 180 dias
            dias_atras = random.randint(0, 179)
            
            # Restrição Estrita do Horário Comercial: entre 06:00 e 20:00 (06h a 19h59)
            hora = random.randint(6, 19)
            minuto = random.randint(0, 59)
            segundo = random.randint(0, 59)
            
            data_venda_dt = hoje - timedelta(days=dias_atras)
            data_venda_dt = data_venda_dt.replace(hour=hora, minute=minuto, second=segundo, microsecond=0)
            data_venda = int(data_venda_dt.timestamp())
            
            # Cada venda possui de 1 a 4 produtos
            num_produtos = random.randint(1, 4)
            produtos_venda = random.sample(produtos_cache, num_produtos)
            
            valor_total = 0.0
            
            for p in produtos_venda:
                id_prod = p["id"]
                preco_unit = p["preco_venda"]
                
                # Quantidades fracionadas ou inteiras (ex: 2 pães ou 0.5 kg de bolo)
                # Pães costumam ter quantidades inteiras (1 a 10) e bolos fracionadas.
                # Simplificamos para pesos fracionados com 1 ou 2 casas decimais.
                quantidade = float(random.choice([1, 2, 3, 4, 5, 0.5, 1.5, 2.5]))
                subtotal = round(quantidade * preco_unit, 2)
                valor_total += subtotal
                
                itens_venda_list.append((
                    id_venda,
                    id_prod,
                    quantidade,
                    preco_unit,
                    subtotal
                ))
                
            valor_total = round(valor_total, 2)
            vendas_list.append((
                id_venda,
                id_usuario,
                valor_total,
                forma_pagamento,
                data_venda
            ))
            
        print("Gravando 10.000 cupons de vendas (Bulk Insert)...")
        
        # Inserção das Vendas
        cursor.executemany(
            """
            INSERT INTO vendas (id_venda, id_usuario, valor_total, forma_pagamento, data_venda)
            VALUES (?, ?, ?, ?, ?);
            """,
            vendas_list
        )
        
        # Inserção de Itens de Vendas
        cursor.executemany(
            """
            INSERT INTO itens_venda (id_venda, id_produto, quantidade, valor_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?);
            """,
            itens_venda_list
        )
        
        conn.commit()
        
    tempo_final = time.time()
    tempo_gasto = tempo_final - tempo_inicial
    
    # 10. Relatório Resumo
    print("\n" + "=" * 50)
    print("STATUS DA INJEÇÃO: Concluído com sucesso!")
    print("=" * 50)
    print(f"Total de Usuários no Banco: {len(ids_usuarios)}")
    print(f"Total de Categorias de Produtos: {len(categorias_prod)}")
    print(f"Total de Categorias Financeiras: {len(categorias_fin)}")
    print(f"Total de Produtos Criados: {len(produtos_cache)}")
    print(f"Total de Insumos Criados: {len(insumos_data)}")
    print(f"Total de Despesas Injetadas: {total_despesas_injetadas}")
    print(f"Total de Recebimentos Injetados: {total_recebimentos_injetados}")
    print(f"Total de Cupons de Vendas Commitados: {len(vendas_list)}")
    print(f"Total de Linhas de Itens de Venda Commitados: {len(itens_venda_list)}")
    print(f"Tempo Total Gasto (Bulk Insert): {tempo_gasto:.2f} segundos")
    print("=" * 50 + "\n")

if __name__ == '__main__':
    executar_simulacao()
