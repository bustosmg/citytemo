# En lugar de:
API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# Usa directamente tu API key:
API_KEY = "e30c0a67be20e63a6907922657d0c2ff"

# Y al final del archivo, cambia:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Puerto 5000 para local
    app.run(host='0.0.0.0', port=port, debug=True)  # debug=True para ver errores
