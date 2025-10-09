import requests

# === CONFIGURACIÓN ===
API_URL = "https://api.wali.chat/v1/messages"
API_TOKEN = "3efe6e1f80130df7841821f662310b3d92037651b5b400af9276a26d3f7c4891f323b7c564a89588"
DESTINATARIO = "+51995191368"
MENSAJE = "Hola Diego 👋, este es un mensaje de prueba enviado desde Python usando la API de WaliChat."

# === ENVÍO DEL MENSAJE ===
headers = {
    "Content-Type": "application/json",
    "Token": API_TOKEN
}

data = {
    "phone": DESTINATARIO,
    "message": MENSAJE
}

try:
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        print("✅ Mensaje enviado correctamente.")
        print("Respuesta:", response.json())
    else:
        print("❌ Error al enviar el mensaje.")
        print("Código de estado:", response.status_code)
        print("Detalle:", response.text)
except Exception as e:
    print("⚠️ Error en la conexión o ejecución:", str(e))
