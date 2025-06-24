# Weather API 🌤️

API REST simple para consultar la temperatura de cualquier ciudad del mundo, desarrollada con Flask y lista para desplegar en Google Cloud Run.

## Características

- ✅ Consulta temperatura por ciudad
- ✅ Respuestas en español
- ✅ Información meteorológica completa
- ✅ Manejo de errores robusto
- ✅ Logging para monitoreo
- ✅ Endpoint de salud para monitoreo
- ✅ Dockerizada y lista para Cloud Run

## Prerequisitos

- Python 3.11+
- Cuenta en [OpenWeatherMap](https://openweathermap.org/api) (API gratuita)
- Docker (para contenedorización)
- Google Cloud SDK (para despliegue)

## Configuración Local

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd weather-api
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key
Obtén tu API key gratuita de [OpenWeatherMap](https://openweathermap.org/api) y configúrala:

```bash
export OPENWEATHER_API_KEY="tu_api_key_aqui"
```

### 5. Ejecutar la aplicación
```bash
python app.py
```

La API estará disponible en `http://localhost:8080`

## Endpoints

### GET /
Información general de la API
```json
{
  "message": "Weather API - Consulta temperatura por ciudad",
  "version": "1.0.0",
  "endpoints": {...}
}
```

### GET /weather?city=<ciudad>
Obtener información meteorológica de una ciudad

**Ejemplo:**
```bash
curl "http://localhost:8080/weather?city=Buenos Aires"
```

**Respuesta:**
```json
{
  "ciudad": "Buenos Aires",
  "pais": "AR",
  "temperatura": {
    "actual": 18.5,
    "sensacion_termica": 17.8,
    "minima": 15.2,
    "maxima": 22.1,
    "unidad": "°C"
  },
  "humedad": 65,
  "descripcion": "Cielo Despejado",
  "presion": 1013,
  "coordenadas": {
    "latitud": -34.6118,
    "longitud": -58.3960
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "fuente": "OpenWeatherMap"
}
```

### GET /health
Estado de salud de la API para monitoreo
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "Weather API"
}
```

## Contenedorización con Docker

### Construir la imagen
```bash
docker build -t weather-api .
```

### Ejecutar el contenedor
```bash
docker run -p 8080:8080 -e OPENWEATHER_API_KEY="tu_api_key" weather-api
```

## Despliegue en Google Cloud Run

### 1. Configurar Google Cloud SDK
```bash
gcloud auth login
gcloud config set project TU_PROJECT_ID
```

### 2. Habilitar APIs necesarias
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### 3. Construir y subir imagen a Container Registry
```bash
# Configurar Docker para usar gcloud
gcloud auth configure-docker

# Construir y subir imagen
gcloud builds submit --tag gcr.io/TU_PROJECT_ID/weather-api
```

### 4. Desplegar en Cloud Run
```bash
gcloud run deploy weather-api \
  --image gcr.io/TU_PROJECT_ID/weather-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENWEATHER_API_KEY="tu_api_key" \
  --port 8080
```

### 5. Alternativa: Despliegue directo desde código fuente
```bash
gcloud run deploy weather-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENWEATHER_API_KEY="tu_api_key"
```

## Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `OPENWEATHER_API_KEY` | API Key de OpenWeatherMap | ✅ |
| `PORT` | Puerto de la aplicación (default: 8080) | ❌ |

## Estructura del Proyecto

```
weather-api/
├── app.py              # Aplicación principal de Flask
├── requirements.txt    # Dependencias de Python
├── Dockerfile         # Configuración de Docker
├── .dockerignore      # Archivos a ignorar en build
└── README.md          # Este archivo
```

## Manejo de Errores

La API maneja varios tipos de errores:

- `400`: Parámetro ciudad faltante
- `404`: Ciudad no encontrada
- `408`: Timeout en la consulta
- `500`: Error interno del servidor
- `503`: Servicio no disponible

## Monitoreo

- Endpoint `/health` para health checks
- Logging estructurado para debugging
- Métricas automáticas en Cloud Run

## Mejoras Futuras Sugeridas

1. **Cache**: Implementar Redis para cachear respuestas
2. **Rate Limiting**: Limitar requests por IP
3. **Autenticación**: JWT tokens para acceso controlado
4. **Métricas**: Integración con Prometheus/Grafana
5. **Tests**: Suite completa de tests unitarios
6. **CI/CD**: Pipeline automático de despliegue
7. **Múltiples proveedores**: Fallback a otras APIs meteorológicas

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación
2. Busca en issues existentes
3. Crea un nuevo issue con detalles del problema

---

Desarrollado con ❤️ para Google Cloud Run