# Базовый образ с полной поддержкой Python 3.10
FROM python:3.10-bullseye

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y gcc python3-dev libffi-dev libpq-dev build-essential && \
    apt-get clean

# Установка рабочей директории
WORKDIR /app

# Копируем все файлы
COPY . .

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Скрипт запуска
RUN chmod +x start.sh
CMD ["./start.sh"]
