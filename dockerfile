
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

# Установка залежностей
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get install -y libpq-dev \
    && apt-get clean \
    && apt-get install -y postgresql-client

    
# Створення робочої директорії
WORKDIR /app


# Копіювання файлів
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
COPY ./init_db.sh /init_db.sh
RUN chmod +x /init_db.sh

CMD ["sh", "/init_db.sh"]

