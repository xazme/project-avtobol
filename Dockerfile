FROM python:3.12-alpine

# Устанавливаем только необходимые системные зависимости
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev && \
    pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Копируем только requirements.txt сначала для кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

# Копируем остальные файлы
COPY . .

# Безопасные настройки Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Запуск от непривилегированного пользователя
RUN adduser -D myuser && chown -R myuser:myuser /app
USER myuser

# Используем более безопасный способ запуска
CMD ["python", "-u", "main.py"]