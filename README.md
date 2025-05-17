{
  "source": {
    "host": "origen-db",
    "port": 5432,
    "user": "postgres",
    "password": "origen_pass",
    "database": "base_origen"
  },
  "target": {
    "host": "destino-db",
    "port": 5432,
    "user": "postgres",
    "password": destino_pass
    "database": "base_destino"
  }
}


docker build -t flask-pg-dump .
docker run -p 8080:8080 flask-pg-dump


/migrate