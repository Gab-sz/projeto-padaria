# Especificação de Desenvolvimento - Etapa 3: Frente de Caixa (PDV) e Transações

**Contexto:**
Você está atuando como Desenvolvedor Backend Python Sênior. As entidades base e dependentes já estão prontas. Sua tarefa agora é implementar o motor transacional do Ponto de Venda (PDV). Esta é a operação mais crítica do sistema, envolvendo o padrão Master-Detail (Venda -> Itens da Venda) e o acionamento de gatilhos lógicos de negócio (baixa de estoque baseada na ficha técnica).

**Regras Arquiteturais Estritas:**
1. Zero acoplamento com a interface gráfica.
2. Todo o processo de registro de venda (inserção principal, inserção dos itens e baixa de estoque) deve ocorrer dentro de um único bloco `with conectar() as conn:` para garantir a atomicidade (ACID) da transação. Se algo falhar, o `rollback` deve ser automático.
3. Utilize a biblioteca `time` para obter o Unix Timestamp atual para a data da venda.

**Tarefas de Implementação:**

### 1. Arquivo: `backend/vendas.py`
* **Objetivo:** Registrar as saídas de mercadorias, calcular os totais e interagir com o inventário.
* **Funções exigidas:**
    * `registrar_venda(id_usuario: int, itens_carrinho: list[dict], forma_pagamento: str) -> int`:
        * **Entrada:** `itens_carrinho` é uma lista de dicionários contendo `id_produto`, `quantidade` e `valor_unitario`.
        * **Passo 1 (Master):** Calcular o `valor_total` somando `(quantidade * valor_unitario)` de todos os itens. Inserir um registro na tabela `vendas` e recuperar o `id_venda` gerado.
        * **Passo 2 (Detail):** Iterar sobre `itens_carrinho` e inserir cada produto na tabela `itens_venda`, vinculando ao `id_venda` e salvando o `subtotal` daquele item.
        * **Passo 3 (Gatilho de Estoque):** Ainda dentro da iteração dos itens do carrinho, fazer uma consulta (SELECT) na tabela `produto_insumos` para descobrir quais insumos compõem aquele `id_produto`. Para cada insumo encontrado, subtrair da tabela `insumos` o equivalente a `(quantidade_vendida * quantidade_necessaria)`. Atualizar também a `data_atualizacao` do insumo.
        * **Retorno:** A função deve retornar o `id_venda` criado após o commit bem-sucedido da transação.
    
    * `listar_vendas(data_inicio: int = None, data_fim: int = None) -> list[dict]`:
        * Retorna o histórico de vendas (`id_venda`, nome do usuário, valor total, forma de pagamento, data). 
        * Permite filtragem opcional por um range de Unix Timestamps.
        * Deve utilizar `JOIN` com a tabela `usuarios` para trazer o nome do operador do caixa.

    * `obter_detalhes_venda(id_venda: int) -> list[dict]`:
        * Retorna o "cupom fiscal" detalhado. 
        * Faz um `SELECT` na tabela `itens_venda` usando `JOIN` com `produtos` para trazer o nome do produto, quantidade, valor unitário e subtotal, filtrando pelo `id_venda`.

**Formato da Entrega:**
Gere estritamente o código-fonte em um bloco único para o arquivo `vendas.py`. Não adicione explicações detalhadas, tutoriais ou textos complementares. Forneça apenas o código Python funcional, estruturado e com tipagem (Type Hints).