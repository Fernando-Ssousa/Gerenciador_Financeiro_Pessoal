# Gerenciador Financeiro Pessoal

[![CI](https://github.com/Fernando-Ssousa/Gerenciador_Financeiro_Pessoal/actions/workflows/ci.yml/badge.svg)](https://github.com/Fernando-Ssousa/Gerenciador_Financeiro_Pessoal/actions/workflows/ci.yml)

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

## Testes

O projeto possui testes unitários para os apps `financeiro` e `usuarios` (models, formulários e views). Para rodá-los localmente:

```bash
python manage.py test
```

## CI/CD

A cada push ou pull request, um workflow do GitHub Actions ([.github/workflows/ci.yml](.github/workflows/ci.yml)) instala as dependências, executa os testes automatizados e valida o build do projeto (`collectstatic`).

## Estrutura do projeto

```
Gerenciador_Financeiro_Pessoal/
├── ambiente/                  # Ambiente virtual (NÃO commitar)
├── gerenciador_financeiro/    # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── usuarios/                  # App de cadastro, login e logout
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── tests.py
├── financeiro/                # App de contas, categorias, transações, parcelas, metas e dashboard
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   ├── templatetags/
│   └── tests.py
├── templates/                  # Templates HTML (Django Templates)
├── static/                     # Arquivos estáticos (CSS/imagens)
├── manage.py                   # Utilitário de linha de comando do Django
├── requirements.txt            # Dependências Python
├── .env                        # Variáveis de ambiente (NÃO commitar)
├── .env.example                # Exemplo de variáveis de ambiente
├── .github/workflows/          # Pipeline de CI (GitHub Actions)
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

## Licença

Projeto pessoal de estudo, sem licença definida.
