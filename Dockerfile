FROM python:3.11-slim

# Instala dependencias necesarias
RUN apt-get update && \
    apt-get install -y wget gnupg curl lsb-release

# Agrega repositorio oficial de PostgreSQL y su clave GPG correctamente
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Instala el cliente PostgreSQL 16
RUN apt-get update && \
    apt-get install -y postgresql-client-16 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configura la app Flask
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]

