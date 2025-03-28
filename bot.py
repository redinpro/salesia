import os
from fastapi import FastAPI
import requests

app = FastAPI()


async def verify_webhook(request: Request):
    challenge = request.query_params.get("hub.challenge")
    token = request.query_params.get("hub.verify_token")

    if token == VERIFY_TOKEN:
        return int(challenge)  # Meta espera un número, no un string
    return {"error": "Token inválido"}, 403
import os 
from fastapi import FastAPI, Request

app = FastAPI()
VERIFY_TOKEN = "miWebhooksalesiaSeguro"

async def verify_webhook(request: Request):
    challenge = request.query_params.get("hub.challenge")
    token = request.query_params.get("hub.verify_token")

    if token == VERIFY_TOKEN:
        return int(challenge)  # Meta espera un número, no un string
    return {"error": "Token inválido"}, 403

@app.get("/")
def home():
    return {"message": "El bot de WhatsApp está corriendo"}


@app.get("/webhook")
def verify_webhook(hub_mode: str = None, hub_verify_token: str = None, hub_challenge: str = None):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)  # Meta espera un número, no un string
    return {"error": "Token inválido"}, 403

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
