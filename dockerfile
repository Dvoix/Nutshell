FROM python:3.12-slim

WORKDIR /nutshell-project

RUN pip install uv

COPY backend/pyproject.toml backend/uv.lock ./backend/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --project backend --locked --no-dev

COPY backend ./backend

ENV PYTHONPATH=/nutshell-project

RUN chmod +x backend/prestartmigrations.sh

ENTRYPOINT ["./backend/prestartmigrations.sh"]

CMD ["uv", "run", "--project", "backend", "--no-dev", "uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
