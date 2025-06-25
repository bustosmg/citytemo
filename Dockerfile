FROM python:3.11-slim

# Variables de entorno para Cloud Run
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Exponer puerto
EXPOSE $PORT

# Ejecutar directamente con Python
CMD python app.py
