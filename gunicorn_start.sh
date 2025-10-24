#!/bin/bash
# gunicorn_start.sh
# Levanta Gunicorn en producción o desarrollo según parámetro --dev

PROJECT_DIR="/var/www/salud_mental"
cd $PROJECT_DIR

# Activar virtualenv si corresponde
# source venv/bin/activate

BIND="127.0.0.1:8000"
WSGI_MODULE="salud_mental.wsgi:application"
ACCESS_LOG="$PROJECT_DIR/gunicorn_access.log"
ERROR_LOG="$PROJECT_DIR/gunicorn_error.log"

# Parámetros por defecto (producción)
WORKERS=3
RELOAD=""
PID_FILE="$PROJECT_DIR/gunicorn.pid"

# Comprobar parámetro --dev
if [ "$1" == "--dev" ]; then
    WORKERS=1
    RELOAD="--reload"
    PID_FILE="$PROJECT_DIR/gunicorn_dev.pid"
    echo "Modo desarrollo activado: autoreload habilitado, 1 worker"
else
    echo "Modo producción activado: $WORKERS workers"
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

# Verificar si ya está corriendo
if is_running; then
    echo "Gunicorn ya está corriendo con PID $(cat $PID_FILE). No se puede iniciar otra instancia."
    exit 1
fi

echo "Iniciando Gunicorn..."
gunicorn $WSGI_MODULE \
    --bind $BIND \
    --workers $WORKERS \
    $RELOAD \
    --daemon \
    --pid $PID_FILE \
    --access-logfile $ACCESS_LOG \
    --error-logfile $ERROR_LOG

echo "Gunicorn iniciado en $BIND con $WORKERS workers. PID guardado en $PID_FILE."
