FROM python:3.13-alpine3.21

# Arbeitsverzeichnis setzen
WORKDIR /app

COPY . .

# Standardbefehl zum Starten der Anwendung
CMD ["python", "src/main.py"]

#port 3000
