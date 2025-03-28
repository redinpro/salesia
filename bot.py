import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Token de verificación para Meta
VERIFY_TOKEN = "miWebhooksalesiaSeguro"

@app.get("/")
def home():
    return {"message": "El bot de WhatsApp está corriendo"}

# Endpoint para la validación del Webhook de Meta
@app.get("/webhook")
def verify_webhook(hub_mode: str = None, hub_verify_token: str = None, hub_challenge: str = None):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)  # Meta espera un número, no un string
    return {"error": "Token inválido"}, 403

# Endpoint para manejar solicitudes POST del Webhook
@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()  # Obtén los datos enviados por Meta
    print("Datos recibidos:", data)  # Imprime los datos para depuración
    return {"status": "received"}  # Responde a Meta con un estado exitoso

# Endpoint para enviar mensajes a través de la API de WhatsApp
@app.post("/send_message/")
def send_message(phone: str, message: str):
    url = "https://graph.facebook.com/v18.0/tu-numero-de-whatsapp/messages"  # Reemplaza con tu número
    headers = {
        "Authorization": "Bearer TU_ACCESS_TOKEN",  # Reemplaza con tu token de Meta
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()