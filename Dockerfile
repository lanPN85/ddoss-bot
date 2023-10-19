FROM python:3.11-slim

LABEL maintainer="<lanpn phan.ngoclan58@gmail.com>"

RUN apt-get update && apt-get install -y curl pkg-config gcc

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 python -

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN /root/.local/bin/poetry config virtualenvs.create false && /root/.local/bin/poetry install --no-interaction --no-ansi

COPY . /app

# EXPOSE 9000

CMD [ "python", "bot.py" ]
