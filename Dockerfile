# Базовый образ с Python
FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libpq-dev && \
    apt-get clean

# Установка рабочей директории
WORKDIR /app

# Копируем все файлы
COPY . .

# Установка зависимостей из requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Скрипт запуска
RUN chmod +x start.sh

CMD ["./start.sh"]
