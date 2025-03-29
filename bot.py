import os
from fastapi import FastAPI, Request
import requests

# Inicializamos la aplicación FastAPI
app = FastAPI()

# Token de verificación para Meta
VERIFY_TOKEN = "Santy365849"  # Cambia este valor según el configurado en Meta Developer

@app.get("/")
def home():
    """
    Endpoint principal para confirmar que el servidor está corriendo.
    """
    return {"message": "El bot de WhatsApp está corriendo"}

@app.get("/webhook")
def verify_webhook(hub_mode: str = None, hub_verify_token: str = None, hub_challenge: str = None):
    """
    Endpoint para la validación del webhook de Meta.
    Meta envía una solicitud GET con parámetros para validar el webhook.
    """
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        # Retornamos el 'hub.challenge' tal como lo envía Meta
        return hub_challenge
    return {"error": "Token inválido"}, 403

@app.post("/webhook")
async def handle_webhook(request: Request):
    """
    Endpoint para manejar las solicitudes POST del webhook.
    Aquí se reciben los datos enviados por Meta cuando ocurren eventos.
    """
    try:
        data = await request.json()  # Extraemos los datos del cuerpo de la solicitud
        print("Datos recibidos:", data)  # Imprimimos los datos para depuración
        return {"status": "received"}  # Respondemos a Meta indicando que el evento fue procesado
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return {"error": "Error interno"}, 500

@app.post("/send_message/")
def send_message(phone: str, message: str):
    """
    Endpoint para enviar mensajes a través de la API de WhatsApp.
    Requiere el número de teléfono y el mensaje como parámetros.
    """
    url = "https://graph.facebook.com/v18.0/tu-numero-de-whatsapp/messages"  # Sustituye con tu número de WhatsApp
    headers = {
        "Authorization": "Bearer TU_ACCESS_TOKEN",  # Reemplaza con tu token de acceso de Meta
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    try:
        response = requests.post(url, json=data, headers=headers)  # Realizamos la solicitud POST
        print("Respuesta de WhatsApp:", response.json())  # Imprimimos la respuesta para depuración
        return response.json()  # Retornamos la respuesta de la API de WhatsApp
        except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
        return {"error": "Error interno al enviar el mensaje"}, 500
