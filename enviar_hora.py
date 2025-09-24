import psutil
import subprocess
import time
import requests
import socket
from datetime import datetime

# Configuración del bot de Telegram
BOT_TOKEN = "7902970233:AAHTvKovwB_YBlAnZ9a6GU6FpmOs2kkbTA0"  # Reemplaza con tu token de bot
CHAT_ID = "8145837"       # Reemplaza con tu ID de chat


# Nombre del contenedor Docker
CONTAINER_NAME = "homeassistant"

# Archivo de log
LOG_FILE = "/home/kali/Documents/scripts/logs/restart_host.log"  # Ruta del archivo de log

# Duración máxima de espera (en segundos)
TIEMPO_MAXIMO_ESPERA = 600
INTERVALO_INTENTOS = 2

def tiene_conexion(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def obtener_hora_arranque():
    try:
        # Obtener el tiempo de arranque del sistema en segundos desde epoch
        boot_time_timestamp = psutil.boot_time()
        
        # Convertir el timestamp a un objeto datetime legible
        boot_time = datetime.fromtimestamp(boot_time_timestamp)
        formatted_boot_time = boot_time.strftime("%d-%m-%Y %H:%M:%S")
        return formatted_boot_time
    except Exception as e:
        return f"Error al obtener la hora de arranque: {e}"

def log_message(message, param):
    """Escribe un mensaje en el archivo de log con la fecha y hora actual."""
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {message}\n")
#    print(f"[{timestamp}] {message}")  # También imprime el mensaje en la terminal
    if param == 1: 
        #print("Estamos dentro del if")
        message1 = "### ARRANQUE DE LA RASPBERRYPI ###"
        message2 = "### ARRANQUE NO PROGRAMADO ###"
        send_telegram_message(BOT_TOKEN, CHAT_ID, message1)
        send_telegram_message(BOT_TOKEN, CHAT_ID, message2)
        message = timestamp + " -->> " + message + "."
        send_telegram_message(BOT_TOKEN, CHAT_ID, message) # También envia el mensaje a Telegram

def send_telegram_message(bot_token, chat_id, message):
    """Envía un mensaje a Telegram."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=params)
    if response.status_code != 200:
        log_message(f"Error al enviar el mensaje: {response.status_code}",0)
        log_message(str(response.json()))

def main():
    tiempo_transcurrido = 0
    while tiempo_transcurrido < TIEMPO_MAXIMO_ESPERA:
        if tiene_conexion():
            hora_arranque = obtener_hora_arranque()
            mensaje = (
                f"Hora de arranque del sistema: {hora_arranque}"
            )
            log_message(mensaje,1)
            break
        else:
            time.sleep(INTERVALO_INTENTOS)
            tiempo_transcurrido += INTERVALO_INTENTOS

if __name__ == "__main__":
    import os
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    main()
