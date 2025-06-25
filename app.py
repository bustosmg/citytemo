from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración
#API_KEY = os.environ.get('OPENWEATHER_API_KEY')
API_KEY = "e30c0a67be20e63a6907922657d0c2ff"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET'])
def home():
    """Endpoint de bienvenida con información de la API"""
    return jsonify({
        "message": "Weather API - Consulta temperatura por ciudad",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Información de la API",
            "GET /weather?city=<ciudad>": "Obtener temperatura de una ciudad",
            "GET /health": "Estado de salud de la API"
        },
        "example": "/weather?city=Buenos Aires"
    })

@app.route('/weather', methods=['GET'])
def get_weather():
    """Obtener temperatura de una ciudad específica"""
    try:
        # Obtener parámetro de ciudad
        city = request.args.get('city')
        
        if not city:
            return jsonify({
                "error": "Parámetro 'city' es requerido",
                "example": "/weather?city=Buenos Aires"
            }), 400
        
        if not API_KEY:
            return jsonify({
                "error": "API Key de OpenWeatherMap no configurada",
                "message": "Configura la variable de entorno OPENWEATHER_API_KEY"
            }), 500
        
        # Construir URL para la API de OpenWeatherMap
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',  # Para obtener temperatura en Celsius
            'lang': 'es'        # Respuestas en español
        }
        
        # Realizar petición a la API externa
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 404:
            return jsonify({
                "error": "Ciudad no encontrada",
                "city": city,
                "message": "Verifica el nombre de la ciudad"
            }), 404
        
        if response.status_code != 200:
            logger.error(f"Error en API externa: {response.status_code}")
            return jsonify({
                "error": "Error al consultar datos meteorológicos",
                "status_code": response.status_code
            }), 500
        
        data = response.json()
        
        # Extraer información relevante
        weather_info = {
            "ciudad": data['name'],
            "pais": data['sys']['country'],
            "temperatura": {
                "actual": round(data['main']['temp'], 1),
                "sensacion_termica": round(data['main']['feels_like'], 1),
                "minima": round(data['main']['temp_min'], 1),
                "maxima": round(data['main']['temp_max'], 1),
                "unidad": "°C"
            },
            "humedad": data['main']['humidity'],
            "descripcion": data['weather'][0]['description'].title(),
            "presion": data['main']['pressure'],
            "visibilidad": data.get('visibility', 'N/A'),
            "coordenadas": {
                "latitud": data['coord']['lat'],
                "longitud": data['coord']['lon']
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "fuente": "OpenWeatherMap"
        }
        
        logger.info(f"Consulta exitosa para: {city}")
        return jsonify(weather_info)
        
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout al consultar datos meteorológicos",
            "message": "Intenta nuevamente en unos momentos"
        }), 408
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {str(e)}")
        return jsonify({
            "error": "Error de conexión",
            "message": "No se pudo conectar al servicio meteorológico"
        }), 503
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return jsonify({
            "error": "Error interno del servidor",
            "message": "Se produjo un error inesperado"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para monitoreo"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "Weather API"
    })

@app.errorhandler(404)
def not_found(error):
    """Manejador para rutas no encontradas"""
    return jsonify({
        "error": "Endpoint no encontrado",
        "available_endpoints": ["/", "/weather", "/health"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejador para errores internos del servidor"""
    logger.error(f"Error interno: {str(error)}")
    return jsonify({
        "error": "Error interno del servidor",
        "message": "Se produjo un error inesperado"
    }), 500

if __name__ == '__main__':
    # Configurar puerto para Cloud Run
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Iniciando servidor en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
