from fastapi import FastAPI
import requests

app = FastAPI()

VERIFY_TOKEN = "miWebhooksalesiaSeguro"

@app.get("/")
def home():
    return {"message": "El bot de WhatsApp está corriendo"}


@app.get("/webhook")
def verify_webhook():
    return {"status": "ok"}

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
