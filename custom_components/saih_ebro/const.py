DOMAIN = "saih_ebro"

API_BASE_URL = "https://www.saihebro.com/datos/apiopendata"

CONF_SIGNALS = "signals"

# Estación Tortosa: señales de ejemplo
SIGNAL_TORTOSA_TEMP = "A027C04TEMPA"
SIGNAL_TORTOSA_LEVEL = "A027C17NRIO1"
SIGNAL_TORTOSA_FLOW = "A027C65QRIO1"

SENSORS_TORTOSA = {
    SIGNAL_TORTOSA_TEMP: {
        "name": "Temperatura agua Ebro en Tortosa",
        "unit": "°C",
        "device_class": "temperature",
    },
    SIGNAL_TORTOSA_LEVEL: {
        "name": "Nivel Ebro en Tortosa",
        "unit": "m",
        "device_class": None,
    },
    SIGNAL_TORTOSA_FLOW: {
        "name": "Caudal Ebro en Tortosa",
        "unit": "m³/s",
        "device_class": None,
    },
}

DEFAULT_SIGNALS = [
    SIGNAL_TORTOSA_TEMP,
    SIGNAL_TORTOSA_LEVEL,
    SIGNAL_TORTOSA_FLOW,
]

