# Construir la imagen del servicio

# Imagen base

FROM python:3.13-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Que los mensajes salgan de una vez y no se queden en buffer
ENV PYTHONDONTWRITEBYTECODE=1  \
    PYTHONUNBUFFERED=1

    
# Updates the Debian package index.
# Installs libgomp1, a runtime library commonly required by machine-learning libraries such as NumPy, scikit-learn, or XGBoost.
# Deletes the downloaded package lists to keep the Docker image smaller
RUN apt-get update \ && apt-get install -y --no-install-recommends libgomp1 \ && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de requerimientos y el código fuente al contenedor
COPY requirements.txt .
#Instalar las librerias para copiar todos los archivos
RUN pip install --no-cache-dir -r requirements.txt
#Copiar todos los archivos del proyecto al contenedor
COPY . .

#Documentacion del puerto
EXPOSE 8080

#Correr el comando para el despliegue del modelo / servicio
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
