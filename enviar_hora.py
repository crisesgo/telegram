import subprocess
import time
import os
import requests
from datetime import datetime

# Configuración del bot de Telegram
BOT_TOKEN = "7902970233:AAHTvKovwB_YBlAnZ9a6GU6FpmOs2kkbTA0"  # Reemplaza con tu token de bot
CHAT_ID = "8145837"       # Reemplaza con tu ID de chat

# Archivo de log
#LOG_FILE = "/home/cristo/Documentos/Telegram/logs/saludo.log"  # Ruta del archivo de log
path = os.path.dirname(__file__)
log_dir = os.path.join(path, "logs")

def log_message(message, param):
    """Escribe un mensaje en el archivo de log con la fecha y hora actual."""
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    #with open(os.path.join(path, "stats.json"), "w") as file:
    #file.write(json_data)
    log_file = os.path.join(log_dir, "saludo.log")
    with open(log_file, "a") as log:
        log.write(f"[{timestamp}] {message}\n")
    #with open(LOG_FILE, "a") as log:
    #    log.write(f"[{timestamp}] {message}\n")
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
