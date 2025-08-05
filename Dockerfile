FROM python:3.10-slim

# Установка зависимостей для сборки aiohttp
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libpq-dev python3-dev build-essential libssl-dev && \
    apt-get clean

# Установка рабочей директории
WORKDIR /app

# Копируем проект
COPY . .

# Обновление pip и установка зависимостей
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Даём права на выполнение скрипта запуска
RUN chmod +x start.sh

# Запускаем бота
CMD ["./start.sh"]
