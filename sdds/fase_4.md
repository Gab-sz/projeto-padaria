# Especificação de Desenvolvimento - Mock de Dados (Requisito Big Data)

**Contexto:**
Você está atuando como Engenheiro de Dados Sênior. Todas as fundações do banco de dados e os CRUDs operacionais já estão concluídos e funcionais. Sua missão agora é criar um script autônomo e isolado que simula o funcionamento financeiro e de vendas da padaria ao longo dos últimos 2 anos. O objetivo é popular o banco de dados com um volume massivo de registros (mínimo de 100.000 itens vendidos) para viabilizar as análises do módulo de Big Data utilizando Pandas posteriormente.

**Regras Arquiteturais Estritas:**
1. Zero acoplamento com a interface gráfica.
2. O script deve ser focado em performance. Inserir 100.000 linhas usando laços com `INSERT` individual em SQLite será extremamente lento e ineficiente. Você deve **obrigatoriamente** usar o método `executemany()` do cursor SQLite para realizar inserções em lote (bulk insert).
3. Respeitar a integridade referencial (`PRAGMA foreign_keys = ON`): as vendas simuladas só podem utilizar `id_produto` e `id_usuario` que já existam previamente no banco de dados.
4. O script deve utilizar as bibliotecas padrão `random`, `time` e `datetime` do Python.

**Tarefas de Implementação:**

### 1. Arquivo: `backend/simulador.py`
* **Objetivo:** Injetar massa de dados fictícia, com viés realista (sazonalidade e horários de pico), nas tabelas `vendas` e `itens_venda`.
* **Requisitos da Lógica de Implementação:**
    * **Preparo e Semeadura (Seed):** Se o banco estiver vazio, o script deve primeiro criar ao menos um usuário "Caixa" e alguns produtos genéricos de padaria (Pão Francês, Leite, Café, Bolo) na tabela `produtos` (e suas respectivas categorias) para ter IDs válidos para a simulação.
    * **Volume Transacional:** Gerar aproximadamente 40.000 registros de transações na tabela `vendas`. Como cada venda deve ter de 1 a 4 itens aleatórios, isso garantirá mais de 100.000 registros na tabela `itens_venda`.
    * **Distribuição Temporal (Realismo para o Analytics):** Gerar datas retroativas aleatórias abrangendo os últimos 730 dias (2 anos) em formato Unix Timestamp. 
    * **Viés de Negócio (Crucial):** A função que gera os horários não pode ser puramente uniforme. Ela deve forçar uma concentração de cerca de 70% das vendas em horários de pico reais de uma padaria (ex: entre 06:00-09:00 e 16:00-19:00). Isso é vital para que o gráfico de "Horários com mais vendas" do futuro Dashboard mostre um padrão claro.
    * **Lógica de Transação:**
        1. Processar os dados em memória RAM primeiro, criando listas de tuplas.
        2. Abrir a conexão com o banco (via `from backend.conexao import conectar`).
        3. Usar `cursor.executemany()` para inserir na tabela `vendas`.
        4. Recuperar ou calcular os `id_venda` gerados e preparar a lista massiva de `itens_venda`.
        5. Usar `cursor.executemany()` para inserir os itens e finalizar a transação (commit).
    * **Log de Execução:** Utilizar o módulo `time` para calcular o tempo total que o script levou para rodar. Ao final, exibir um `print` simples no terminal informando a quantidade de registros inseridos e os segundos de processamento.

**Formato da Entrega:**
Gere estritamente o código-fonte funcional em um bloco único para o arquivo `simulador.py`. Modularize a lógica interna com funções auxiliares se necessário. Não adicione explicações detalhadas, tutoriais ou textos complementares. Forneça apenas o código Python estruturado e formatado (PEP 8).