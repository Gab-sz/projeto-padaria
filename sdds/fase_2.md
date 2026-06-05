# Especificação de Desenvolvimento - Etapa 2: CRUD de Entidades Dependentes

**Contexto:**
Você está atuando como Desenvolvedor Backend Python Sênior. As fundações de banco de dados (`conexao.py` e `setup.py`) e as entidades independentes base (Categorias e Insumos) já foram implementadas. Sua tarefa agora é construir os módulos que gerenciam as entidades que dependem de chaves estrangeiras (Usuários, Produtos, Ficha Técnica e Financeiro).

**Regras Arquiteturais Estritas:**
1. Escreva apenas funções puras que interagem com o banco de dados.
2. Zero acoplamento com a interface gráfica.
3. Utilize o context manager importando: `from backend.conexao import conectar`.
4. Utilize Type Hints nas assinaturas das funções.
5. Em funções de listagem (`SELECT`), utilize `INNER JOIN` para retornar nomes descritivos em vez de apenas IDs de chaves estrangeiras.

**Tarefas de Implementação:**

### 1. Arquivo: `backend/usuarios.py`
* **Objetivo:** Gerenciar o acesso ao sistema.
* **Funções exigidas:**
    * `inserir_usuario(nome: str, login: str, senha: str) -> int`: Insere o usuário e retorna o ID. (Nesta versão, pode salvar a senha em texto plano para simplificação acadêmica).
    * `listar_usuarios() -> list[dict]`: Retorna a lista de usuários.
    * `autenticar_usuario(login: str, senha: str) -> dict | None`: Consulta o banco e retorna um dicionário com os dados do usuário se as credenciais baterem, ou `None` caso falhe.

### 2. Arquivo: `backend/produtos.py`
* **Objetivo:** Gerenciar o catálogo de venda e a ficha técnica (relação Produto <-> Insumo).
* **Funções exigidas:**
    * `inserir_produto(id_categoria_produto: int, nome: str, preco_venda: float, custo_producao: float) -> int`.
    * `listar_produtos() -> list[dict]`: Deve utilizar um `INNER JOIN` com `categorias_produto` para retornar o nome da categoria, mapeando as chaves: `id`, `nome`, `categoria_nome`, `preco_venda`, `custo_producao`.
    * `vincular_ficha_tecnica(id_produto: int, id_insumo: int, quantidade_necessaria: float) -> None`: Insere na tabela associativa `produto_insumos`.
    * `obter_ficha_tecnica(id_produto: int) -> list[dict]`: Lista os insumos necessários para um produto específico, usando `JOIN` com a tabela `insumos` para trazer o nome e a unidade de medida do insumo.

### 3. Arquivo: `backend/financeiro.py`
* **Objetivo:** Centralizar as movimentações de caixa (Despesas e Recebimentos avulsos).
* **Funções exigidas:**
    * `inserir_despesa(id_categoria_financeira: int, id_usuario: int, descricao: str, valor_despesa: float) -> int`: Utiliza a biblioteca `time` para salvar a `data_despesa` atual em Unix Timestamp.
    * `listar_despesas() -> list[dict]`: Faz `JOIN` com `categorias_financeiras` e `usuarios` para exibir quem registrou e qual a categoria em texto.
    * `inserir_recebimento(id_usuario: int, categoria_texto: str, descricao: str, valor_recebido: float) -> int`: Utiliza `time` para salvar a `data_recebimento` em Unix Timestamp. (Note que recebimentos usam categoria em texto livre, conforme o schema).
    * `listar_recebimentos() -> list[dict]`: Faz `JOIN` com `usuarios` para listar os recebimentos de forma legível.

**Formato da Entrega:**
Gere estritamente o código-fonte em blocos separados para cada um dos três arquivos citados (`usuarios.py`, `produtos.py`, `financeiro.py`). Abstenha-se de adicionar explicações ou textos complementares; forneça apenas o código Python funcional.