# Sistema de Gestão de Padaria (ERP & PDV)

Este é um sistema desktop completo para controle e gestão de padarias, desenvolvido utilizando **Python**, **Tkinter** (para a interface gráfica nativa) e **SQLite** (para armazenamento persistente de dados).

O projeto é estruturado de forma modularizada, separando a lógica de negócios e persistência (Backend) da interface visual (Frontend).

---

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3.x
*   **Interface Gráfica (GUI):** Tkinter & TTK (Themed Tkinter)
*   **Banco de Dados:** SQLite3
*   **Lógica Funcional:** Sem dependências externas de terceiros (usa bibliotecas nativas do Python).

---

## 📁 Estrutura do Projeto

```text
projeto-padaria/
│
├── main.py                 # Ponto de entrada do sistema
├── .gitignore              # Arquivo para impedir o envio de caches e base de dados local
├── README.md               # Este arquivo de documentação
│
├── banco/
│   ├── setup.py            # Script DDL para criar e inicializar as tabelas
│   └── padaria.db          # Arquivo SQLite gerado localmente (ignorado pelo git)
│
├── backend/
│   ├── conexao.py          # Gerenciamento de contexto da conexão SQLite
│   ├── usuarios.py         # Cadastro, listagem e autenticação de usuários
│   ├── produtos.py         # Cadastro de produtos e ficha técnica
│   ├── insumos.py          # Controle de estoque de matérias-primas
│   ├── vendas.py           # Registro de vendas e baixa automática de insumos
│   ├── financeiro.py       # Fluxo de caixa, despesas e receitas avulsas
│   └── simulador.py        # Script para popular banco com dados massivos de teste
│
└── frontend/
    ├── app.py              # Controlador principal da janela Tkinter (Navegação de telas)
    └── views/              # Telas individuais da aplicação (Frames do Tkinter)
        ├── login.py        # Autenticação de usuários
        ├── menu.py         # Menu lateral e sidebar de navegação
        ├── pdv.py          # Frente de caixa (Carrinho, cálculo de totais e venda)
        ├── estoque.py      # Painel de controle de estoque de insumos
        ├── produtos.py     # Cadastro unificado de produtos e fichas técnicas
        ├── financeiro.py   # Registro de despesas e receitas avulsas
        └── cadastros.py    # Telas de suporte (Categorias de produto/financeiras e novos usuários)
```

---

## 🚀 Como Rodar o Projeto em Qualquer Máquina

Siga as instruções passo a passo para configurar e rodar o projeto do zero:

### 1. Clonar o Repositório
Abra um terminal (Prompt de Comando ou PowerShell) e execute o comando:
```bash
git clone https://github.com/JoaoLua/projeto-padaria.git
cd projeto-padaria
```

### 2. Inicializar o Banco de Dados
Como o banco de dados local (`padaria.db`) está adicionado ao `.gitignore` para evitar envio de dados de cache de forma binária, você precisará inicializar a estrutura de tabelas em sua máquina rodando o script de configuração:
```bash
python banco/setup.py
```
*Este comando criará o arquivo `padaria.db` dentro da pasta `banco` com todas as tabelas e relacionamentos necessários.*

### 3. (Opcional) Popular o Banco com Dados Simulados
Se você deseja popular o banco de dados com dados reais de teste para fins de demonstração (incluindo insumos, categorias e histórico de vendas):
```bash
python backend/simulador.py
```
*Isso gerará transações de venda fictícias e inserirá usuários padrões para que o sistema não inicie totalmente vazio.*

### 4. Executar o Sistema
Para abrir a interface gráfica do programa, execute:
```bash
python main.py
```

---

## 🔑 Credenciais Padrão de Acesso

Caso tenha rodado o script de simulação/população de dados (`simulador.py`), você pode acessar o sistema utilizando qualquer uma das credenciais abaixo:

*   **Administrador:**
    *   **Login:** `tst`
    *   **Senha:** `123`
*   **Caixa:**
    *   **Login:** `joao`
    *   **Senha:** `1234`
*   **Gerente:**
    *   **Login:** `maria`
    *   **Senha:** `abc`
*   **Caixa Simulação:**
    *   **Login:** `caixa_simulador`
    *   **Senha:** `simula123`
