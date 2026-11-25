FROM python:3.12-slim AS builder


RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential pkg-config default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copia SÓ o requirements antes do código: a camada de dependências
# fica em cache e só é refeita quando o requirements.txt mudar.
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Estágio 2: RUNTIME
# Sem compilador: menor e com menos superfície de ataque.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Apenas a biblioteca de execução do MySQL 
RUN apt-get update && apt-get install -y --no-install-recommends \
        libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Usuário sem privilégios: o container não roda como root
RUN useradd --create-home --uid 1000 app
WORKDIR /app

# Instala as dependências a partir dos wheels pré-compilados
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*.whl \
    && rm -rf /wheels

# Código da aplicação
COPY --chown=app:app . .

# Variáveis só para o build (collectstatic precisa carregar o settings);
# NÃO ficam na imagem final de forma útil: em runtime use -e / --env-file.
RUN SECRET_KEY=build DB_NAME=x DB_USER=x DB_PASSWORD=x \
    python manage.py collectstatic --noinput \
    && chown -R app:app /app

USER app
EXPOSE 8000

# Gunicorn em vez do runserver
CMD ["gunicorn", "gerenciador_financeiro.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4"]