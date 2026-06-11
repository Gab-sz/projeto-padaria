# Especificação de Desenvolvimento - Fase 3: Simulador de Dados Completo (Big Data)

**Contexto:**
Você está atuando como Engenheiro de Dados Sênior. As bases estruturais do banco de dados já foram estabelecidas. Sua missão agora é construir um script de simulação autônomo (`backend/simulador.py`) responsável por gerar uma massa de dados retroativa altamente realista para os últimos 6 meses. Esse dataset servirá como combustível para o motor analítico do Pandas processar cenários volumétricos de Big Data.

**Regras Arquiteturais Estritas:**
1. **Zero Acoplamento:** Nenhuma interface gráfica ou input interativo deve ser evocado. O script deve ser 100% autônomo.
2. **Alta Performance (Bulk Inserts):** É terminantemente proibido executar laços individuais de `INSERT` para as vendas. Você deve acumular os dados em memória e utilizar `cursor.executemany()` para despachar os registros em lotes agrupados.
3. **Garantia de Integridade:** Ative `PRAGMA foreign_keys = ON;` no início da rotina. Todas as Foreign Keys devem apontar para IDs gerados no próprio ciclo de sementes (seed).

---

## Diretrizes de População do Banco de Dados

### 1. Usuário de Testes Único
* O script deve verificar a tabela `usuarios`. Caso esteja vazia, deve criar **exatamente um** usuário administrador de testes.
* Credenciais padrão: Nome: `Usuario Teste`, Login: `admin`, Senha: `123`.

### 2. Infraestrutura de Categorias
* **Categorias de Produtos/Insumos:** Inserir obrigatoriamente as 7 categorias operacionais: `Panificação`, `Laticínios`, `Bebidas`, `Secos`, `Perecíveis`, `Limpeza` e `Embalagens`.
* **Categorias Financeiras:** * *Saídas (Despesas):* Criar categorias como `Contas de Consumo` (Água/Luz), `Fornecedores`, `Aluguel`, `Folha de Pagamento` e `Manutenção`.
    * *Entradas (Recebimentos Avulsos):* Criar categorias como `Aporte de Capital` e `Encomendas Especiais`.

### 3. Catálogo de Produtos (Mínimo de 20 Itens)
O script deve cadastrar no mínimo 20 produtos comerciais divididos estrategicamente em dois tipos:

* **Produtos com Ficha Técnica (Consomem Insumos):** No mínimo 10 produtos (ex: Pão Francês, Bolo de Cenoura, Croissant, Pão de Queijo, Coxinha, etc.). O script deve cadastrar os insumos necessários (Farinha, Açúcar, Ovos, Manteiga) e criar o vínculo correspondente na tabela `produto_insumos` com as quantidades fracionadas de consumo (ex: 0.050 kg de farinha por pão).
* **Produtos sem Ficha Técnica (Revenda Direta / Sem Insumo Relacionado):** No mínimo 10 produtos (ex: Refrigerante em Lata, Água Mineral, Suco de Caixa, Café Expresso, Sacola Retornável, Doces Industrializados, etc.). Esses itens possuem custo de produção fixo, mas não decrementam ingredientes do inventário.

### 4. Janela Temporal e Horário Comercial (Regras Estritas de Data/Hora)
* **Retroatividade:** Todas as movimentações geradas (vendas, itens_venda, despesas e recebimentos) devem possuir datas distribuídas uniformemente ou com pesos sazonais abrangendo os **últimos 6 meses** (180 dias retroativos a partir da data atual de execução).
* **Armazenamento:** As datas devem ser convertidas e salvas estritamente no formato **Unix Timestamp (INTEGER)**.
* **Restrição de Horário Comercial:** Para a tabela de `vendas`, os horários gerados devem pertencer obrigatoriamente ao intervalo do horário comercial da padaria: **entre 06:00 e 20:00**. Nenhuma venda pode possuir timestamp correspondente à madrugada ou horários de fechamento.

### 5. Volume Volumétrico de Transações
* **Despesas e Recebimentos:** Inserir lançamentos mensais recorrentes para despesas fixas (Aluguel, Salários) e lançamentos aleatórios fracionados para despesas variáveis (Luz, Fornecedores) e recebimentos nos últimos 6 meses.
* **Vendas:** Gerar um volume massivo de **no máximo 10.000 transações de vendas** na tabela `vendas`. 
* **Itens da Venda:** Cada uma das vendas deve conter de 1 a 4 produtos aleatórios do catálogo de 20 itens, gerando os registros associados na tabela `itens_venda` com o cálculo exato do preço unitário histórico e do subtotal.

---

## Log de Performance e Fechamento
Ao término da execução de injeção massiva de dados, o script deve calcular o tempo de processamento total decorrido através do módulo `time` e imprimir no terminal um sumário estruturado informando:
- Status de conclusão da injeção de dados.
- Total de usuários, categorias e produtos base criados.
- Total de despesas e recebimentos injetados.
- Total exato de cupons de `vendas` e linhas de `itens_venda` commitados via `executemany`.
- Tempo total gasto na operação de bulk insert em segundos.

**Formato de Entrega:**
Gere exclusivamente o código estruturado do arquivo `backend/simulador.py`. Forneça o código Python limpo, em bloco único, documentado e totalmente aderente à PEP 8.
