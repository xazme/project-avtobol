# Многостадийная сборка для уменьшения уязвимостей
FROM python:3.12-slim-bookworm

WORKDIR /app

# Установка только необходимых системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Создаем виртуальное окружение
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.12-slim-bookworm

WORKDIR /app

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv

# Копируем код приложения
COPY . .

# Используем виртуальное окружение
ENV PATH="/opt/venv/bin:$PATH"

# Безопасные настройки
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Создаем непривилегированного пользователя
RUN useradd -m myuser && chown -R myuser:myuser /app
USER myuser

CMD ["python", "-u", "main.py"]