FROM python:3.12.2
WORKDIR /app
ADD app.py poetry.lock pyproject.toml ./
ADD src/ ./src

RUN pip install poetry uvicorn && poetry install --no-root

CMD ["poetry", "run", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0"]