FROM python:3.11-slim

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY app.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 8080

# Ejecutar directamente con Python (sin Gunicorn)
CMD ["python", "app.py"]
