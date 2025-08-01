FROM python:3.9-slim

# Installer outils utiles
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps iputils-ping curl bash \
    && rm -rf /var/lib/apt/lists/*

# Définir variables pour logs non bufferisés
ENV PYTHONUNBUFFERED=1

# Copier les fichiers
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dahua_to_mqtt.py .

CMD ["python3", "-u", "/app/dahua_to_mqtt.py"]
