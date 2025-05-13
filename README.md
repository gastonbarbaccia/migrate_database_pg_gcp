curl -X POST http://localhost:8080/clone \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "host": "source-host",
      "port": "5432",
      "dbname": "origen",
      "user": "postgres",
      "password": "source-password"
    },
    "target": {
      "host": "target-host",
      "port": "5432",
      "dbname": "destino",
      "user": "postgres",
      "password": "target-password"
    }
  }'
