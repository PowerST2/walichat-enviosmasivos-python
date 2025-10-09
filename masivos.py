import csv
import time
import requests
from datetime import datetime

# === CONFIGURACIÓN ===
API_URL = "https://api.wali.chat/v1/messages"
API_TOKEN = "3efe6e1f80130df7841821f662310b3d92037651b5b400af9276a26d3f7c4891f323b7c564a89588"
CSV_PATH = "contactos.csv"
RESULTADOS_PATH = "resultados.csv"
DELAY = 1.0  # segundos entre cada envío (puedes subirlo a 2 o 3 si quieres ser más prudente)

# === FUNCIONES ===
def generar_mensaje_asignacion(nombre, aula):
    """
    Genera un mensaje personalizado para informar la asignación de aula
    para el Primer Parcial de Cepre
    """
    mensaje = f"""Hola *{nombre}* 😊

Te saludamos desde la *Dirección de Admisión (DIAD)*.
Queremos informarte con mucho entusiasmo que tu aula asignada para el *examen Primer Parcial de CEPRE* es: *{aula}* 🏫✨

Te recomendamos llegar con anticipación, llevar tu documento de identidad y todo lo necesario para rendir tu examen con tranquilidad.

¡Te deseamos mucho éxito en esta etapa! 🍀
Confía en ti y en todo lo que has aprendido 💪

Con aprecio,
*Dirección de Admisión (DIAD)*
*Universidad Nacional de Ingeniería*"""

    return mensaje


def enviar_mensaje(phone, message):
    headers = {
        "Content-Type": "application/json",
        "Token": API_TOKEN
    }
    payload = {
        "phone": phone,
        "message": message
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        status = response.status_code
        data = response.json() if response.text else {}

        if status in [200, 201]:
            estado_envio = data.get("deliveryStatus", "enviado")
            print(f"✅ [{phone}] Mensaje encolado correctamente ({estado_envio})")
            return "Éxito", estado_envio
        else:
            print(f"❌ [{phone}] Error {status}: {response.text}")
            return "Error", response.text
    except Exception as e:
        print(f"⚠️ [{phone}] Error de conexión: {e}")
        return "Error", str(e)


def enviar_mensajes_desde_csv():
    resultados = []
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            nombre = fila.get("nombre", "").strip()
            phone = fila.get("telefono", "").strip()
            aula = fila.get("aula", "").strip()
            
            if not phone or not nombre or not aula:
                print("⚠️ Fila incompleta, se omite:", fila)
                continue

            # Generar mensaje personalizado
            message = generar_mensaje_asignacion(nombre, aula)
            
            estado, detalle = enviar_mensaje(phone, message)
            resultados.append({
                "nombre": nombre,
                "telefono": phone,
                "aula": aula,
                "estado": estado,
                "detalle": detalle,
                "fecha_envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            time.sleep(DELAY)

    # Guardar resultados
    with open(RESULTADOS_PATH, "w", newline='', encoding="utf-8") as f:
        campos = ["nombre", "telefono", "aula", "estado", "detalle", "fecha_envio"]
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(resultados)
    print(f"\n📄 Envío completado. Resultados guardados en '{RESULTADOS_PATH}'")


# === EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    print("🚀 Iniciando envío masivo desde contactos.csv ...\n")
    enviar_mensajes_desde_csv()
