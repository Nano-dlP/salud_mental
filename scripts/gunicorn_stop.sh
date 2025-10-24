#!/bin/bash
# gunicorn_stop.sh
# Detiene Gunicorn en producción o desarrollo según parámetro --dev

PROJECT_DIR="/var/www/salud_mental"          # raíz del proyecto
LOG_DIR="$PROJECT_DIR/logs"                  # carpeta de logs
PID_FILE="$PROJECT_DIR/gunicorn.pid"        # PID producción
PID_FILE_DEV="$PROJECT_DIR/gunicorn_dev.pid" # PID desarrollo
ACCESS_LOG="$LOG_DIR/gunicorn_access.log"
ERROR_LOG="$LOG_DIR/gunicorn_error.log"
ACCESS_LOG_DEV="$LOG_DIR/gunicorn_dev_access.log"
ERROR_LOG_DEV="$LOG_DIR/gunicorn_dev_error.log"


# Comprobar parámetro --dev
if [ "$1" == "--dev" ]; then
    PID_FILE="$PROJECT_DIR/gunicorn_dev.pid"
    echo "Deteniendo Gunicorn en modo desarrollo..."
else
    echo "Deteniendo Gunicorn en modo producción..."
fi

# Función para verificar si el PID existe y si el proceso está vivo
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            return 0  # está corriendo
        else
            echo "PID encontrado pero proceso no activo. Eliminando archivo PID."
            rm -f "$PID_FILE"
            return 1
        fi
    else
        return 1  # no está corriendo
    fi
}

# Detener Gunicorn si está corriendo
if is_running; then
    kill $(cat "$PID_FILE")
    rm -f "$PID_FILE"
    echo "Gunicorn detenido correctamente."
else
    echo "No hay proceso Gunicorn corriendo con PID $(cat "$PID_FILE" 2>/dev/null)."
fi
