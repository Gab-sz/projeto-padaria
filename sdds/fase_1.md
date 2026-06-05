# Especificação de Desenvolvimento - Fase 2: Módulo Operacional (Backend Core)

**Contexto:**
Você está atuando como um Desenvolvedor Backend Python Sênior. A infraestrutura de banco de dados (`banco/setup.py`) e o gerenciador de conexões SQLite (`backend/conexao.py`) já foram previamente implementados no projeto da padaria. Seu objetivo agora é construir os controladores de banco de dados (CRUD) na pasta `backend/`.

**Regras Arquiteturais Estritas:**
1. Você deve escrever apenas funções puras que interagem exclusivamente com o banco de dados.
2. Zero acoplamento com a interface gráfica. Nenhuma menção a Tkinter, `print()` ou `input()` no terminal.
3. Todas as funções devem utilizar o context manager de conexão existente importando: `from backend.conexao import conectar`. O context manager já lida com o `.commit()`, `.rollback()` e `.close()`.
4. O banco de dados utiliza `PRAGMA foreign_keys = ON;`.
5. Utilize Type Hints em todas as assinaturas de funções.

**Tarefas de Implementação:**

### 1. Arquivo: `backend/categorias.py`
* **Objetivo:** Gerenciar as tabelas de domínio `categorias_produto` e `categorias_financeiras`.
* **Funções exigidas:**
    * `inserir_categoria_produto(nome: str, descricao: str) -> int`: Executa o `INSERT` e retorna o ID gerado (`cursor.lastrowid`).
    * `listar_categorias_produto() -> list[dict]`: Retorna uma lista de dicionários mapeando as chaves: `id`, `nome` e `descricao`.
    * `inserir_categoria_financeira(nome: str, tipo_movimentacao: str) -> int`: Valida se `tipo_movimentacao` é obrigatoriamente 'ENTRADA' ou 'SAIDA' antes de inserir.
    * `listar_categorias_financeiras(tipo: str = None) -> list[dict]`: Retorna a lista de categorias. Deve permitir um filtro opcional pelo argumento `tipo`.

### 2. Arquivo: `backend/insumos.py`
* **Objetivo:** Gerenciar a tabela `insumos` (estoque de matérias-primas).
* **Funções exigidas:**
    * `inserir_insumo(nome: str, categoria: str, quantidade_atual: float, unidade_medida: str, estoque_minimo: float) -> int`: Utiliza a biblioteca `time` (`int(time.time())`) para preencher o campo `data_atualizacao` com o Unix Timestamp no momento da inserção.
    * `listar_insumos() -> list[dict]`: Retorna o inventário completo estruturado em dicionários.
    * `atualizar_quantidade_insumo(id_insumo: int, variacao: float) -> None`: Executa um `UPDATE` no banco somando o valor de `variacao` (que pode ser negativo em caso de uso) à `quantidade_atual`. Atualiza simultaneamente o campo `data_atualizacao`.

### 3. Arquivo: `backend/produtos.py`
* **Objetivo:** Gerenciar o catálogo de venda final (`produtos`) e a respectiva ficha técnica associativa (`produto_insumos`).
* **Funções exigidas:**
    * `inserir_produto(id_categoria_produto: int, nome: str, preco_venda: float, custo_producao: float) -> int`.
    * `listar_produtos() -> list[dict]`: Deve obrigatoriamente utilizar um `INNER JOIN` com a tabela `categorias_produto` para retornar o nome em texto da categoria associada, e não apenas o seu ID.
    * `vincular_ficha_tecnica(id_produto: int, id_insumo: int, quantidade_necessaria: float) -> None`: Insere a relação de dependência entre o produto vendido e o insumo gasto na tabela `produto_insumos`.
    * `obter_ficha_tecnica(id_produto: int) -> list[dict]`: Lista os IDs dos insumos e as quantidades necessárias para fabricar o produto especificado.

**Formato da Entrega:**
Gere estritamente o código-fonte em blocos separados para cada um dos três arquivos citados (`categorias.py`, `insumos.py`, `produtos.py`). Abstenha-se de adicionar explicações detalhadas ou textos complementares; forneça apenas o código Python funcional e limpo.