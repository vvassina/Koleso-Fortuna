FROM python:3.10-bullseye

RUN apt-get update && \
    apt-get install -y gcc python3-dev libffi-dev libpq-dev build-essential && \
    apt-get clean

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh
CMD ["./start.sh"]
