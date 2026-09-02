# Gerenciador Financeiro Pessoal

Aplicação web em Django para controle de finanças pessoais: contas bancárias, categorias de receita/despesa, transações, parcelas e metas financeiras.

## Funcionalidades

- **Autenticação**: cadastro, login e logout de usuários.
- **Contas**: cadastro de contas correntes e poupanças, com saldo inicial e banco.
- **Categorias**: organização de receitas e despesas por categoria.
- **Transações**: lançamento de receitas/despesas vinculadas a uma conta e categoria.
- **Parcelas**: controle de contas a pagar/receber parceladas, com data de vencimento e status de pagamento.
- **Metas financeiras**: definição de metas com valor alvo, valor atual e prazo.
- **Dashboard**: visão geral consolidada das finanças do usuário.

Todos os dados são isolados por usuário logado.

## Tecnologias

- Python 3 / Django 4.2
- MySQL (via `mysqlclient`)
- django-bootstrap5 para o layout dos formulários
- python-dotenv para configuração via variáveis de ambiente

## Pré-requisitos

- Python 3.12+
- MySQL Server em execução
- Um banco de dados criado (ex.: `gerenciador_financeiro`)

## Instalação

1. Clone o repositório e entre na pasta do projeto.

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv ambiente
   # Windows
   ambiente\Scripts\activate
   # Linux/Mac
   source ambiente/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Copie o arquivo de exemplo de variáveis de ambiente e ajuste os valores:

   ```bash
   cp .env.example .env
   ```

   Preencha `.env` com sua `SECRET_KEY`, credenciais do MySQL e demais configurações:

   ```env
   SECRET_KEY=troque-por-uma-chave-secreta-gerada
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   DB_ENGINE=django.db.backends.mysql
   DB_NAME=gerenciador_financeiro
   DB_USER=root
   DB_PASSWORD=troque-por-uma-senha
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. Aplique as migrações:

   ```bash
   python manage.py migrate
   ```

6. (Opcional) Crie um superusuário para acessar o admin:

   ```bash
   python manage.py createsuperuser
   ```

7. Rode o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

Acesse `http://localhost:8000/` no navegador.

## Estrutura do projeto

```
gerenciador_financeiro/   # Configurações do projeto (settings, urls, wsgi)
usuarios/                 # Cadastro, login e logout
financeiro/               # Contas, categorias, transações, parcelas, metas e dashboard
templates/                # Templates HTML compartilhados
static/                   # Arquivos estáticos (CSS/JS)
```

## Licença

Projeto pessoal de estudo, sem licença definida.
