import subprocess
import time
import os
import requests
from zoneinfo import ZoneInfo  # Python 3.9+
from datetime import datetime

# Configuración del bot de Telegram
BOT_TOKEN = "token"  # Reemplaza con tu token de bot
CHAT_ID = "8145837"       # Reemplaza con tu ID de chat

# Archivo de log
#LOG_FILE = "/home/cristo/Documentos/Telegram/logs/saludo.log"  # Ruta del archivo de log
path = os.path.dirname(__file__)
log_dir = os.path.join(path, "logs")

def log_message(message, param):
    """Escribe un mensaje en el archivo de log con la fecha y hora actual."""
    tz_madrid = ZoneInfo("Europe/Madrid")
    timestamp = datetime.now(tz_madrid).strftime("%d-%m-%Y %H:%M:%S")
    log_file = os.path.join(log_dir, "saludo.log")
    with open(log_file, "a") as log:
        log.write(f"[{timestamp}] {message}\n")
    if param == 1:         
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
    mensaje = ("### MENSAJE DE PRUEBA ###")
    log_message(mensaje,1)

if __name__ == "__main__":
    os.makedirs(log_dir, exist_ok=True)  # Asegura que la carpeta exista
    main()
