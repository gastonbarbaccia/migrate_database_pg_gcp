# Imagen base con Python y herramientas necesarias
FROM python:3.10-slim

# Instalar utilidades de PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para Cloud Run
EXPOSE 8080

# Ejecutar la app
CMD ["python", "app.py"]
