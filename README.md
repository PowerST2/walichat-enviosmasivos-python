# 📢 Envío Masivo de Mensajes por WaliChat

Automatización avanzada para el envío masivo y personalizado de mensajes de WhatsApp usando la API oficial de WaliChat. Diseñado para agilizar la comunicación con alumnos en procesos de admisión universitarios, permitiendo notificar asignaciones de aula de manera eficiente y segura.

---

## 📘 Descripción General

Este proyecto permite al personal administrativo de universidades (especialmente áreas de Admisión) enviar mensajes de WhatsApp personalizados a gran cantidad de alumnos, informando sobre la asignación de aula para el examen "Primer Parcial de CEPRE".

- Utiliza la **API oficial de WaliChat** para el envío de mensajes.
- Lee los alumnos desde un archivo `contactos.csv` y genera mensajes individualizados con nombre y aula.
- Incluye un retardo configurable (`DELAY`) entre envíos para evitar bloqueos o saturación del servicio.
- Al finalizar, genera un archivo `resultados.csv` con el historial completo y los estados de cada envío.

---

## 🧩 Requisitos Previos

Para ejecutar correctamente el proyecto, asegúrate de contar con:

- **Python 3.10 o superior** instalado ([Descargar Python](https://www.python.org/downloads/))
- **Conexión estable a Internet**
- **Token de autenticación de WaliChat**
  - Solicítalo en [wali.chat](https://wali.chat/) tras crear una cuenta y configurar tu API.
  - El token se coloca en el script o preferentemente en un archivo `.env` (ver sección "Buenas prácticas").
- **Archivo `contactos.csv` estructurado correctamente** (ver sección "Estructura del CSV").
- **Editor de texto recomendado:** [VS Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/), Sublime Text, etc.
- **Sistema operativo compatible:** Windows, macOS o Linux.

---

## ⚙️ Creación del Entorno Virtual `.venv`

Se recomienda el uso de un entorno virtual para aislar dependencias.

### 💻 En Windows (CMD o PowerShell):

```sh
python -m venv .venv
.venv\Scripts\activate
```

### 🐧 En Linux / macOS:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

> El prompt del terminal debería mostrar algo como `(.venv)`, indicando que el entorno está activo.

---

## 📦 Instalación de Dependencias

Este proyecto utiliza la librería `requests` para realizar solicitudes HTTP.

### Instalación directa:

```sh
pip install requests
```

### Instalación con `requirements.txt`:

1. Crea el archivo `requirements.txt` con el siguiente contenido:

   ```
   requests
   ```

2. Instala las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

---

## 🗂️ Estructura del Proyecto

La estructura recomendada del directorio es la siguiente:

```
C:\envios-masvos\
│
├── masivos.py               # Script principal
├── contactos.csv            # Archivo de entrada con los datos de los alumnos
├── resultados.csv           # Archivo generado con el historial de envíos
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto
```

---

## 📄 Estructura del CSV de Entrada (`contactos.csv`)

El archivo **contactos.csv** debe tener la siguiente estructura, con los encabezados en minúsculas y SIN espacios:

| nombre        | telefono       | aula  |
|---------------|---------------|-------|
| Juan Pérez    | +51987654321  | A-101 |
| María López   | +51912345678  | B-203 |
| Pedro Torres  | +51955566789  | C-305 |

**Notas Importantes:**
- Los encabezados deben ser **exactamente**: `nombre`, `telefono`, `aula`
- El número de teléfono debe incluir el prefijo internacional (`+51` para Perú)
- El archivo debe guardarse en formato **UTF-8 sin BOM**

---

## 💬 Explicación del Flujo del Script

### 1. **Carga del archivo CSV**
   - Se abre `contactos.csv` y se lee cada fila usando `csv.DictReader`.

### 2. **Procesamiento de cada contacto**
   - Por cada fila válida (con nombre, teléfono y aula), se genera un mensaje personalizado usando la función `generar_mensaje_asignacion(nombre, aula)`.

### 3. **Envío del mensaje**
   - El mensaje se envía mediante una solicitud HTTP POST a la API de WaliChat (`requests.post`), usando el token de autenticación.
   - Los resultados del envío se muestran en consola e incluyen el estado (`Éxito`/`Error`) y detalles proporcionados por la API.

### 4. **Retardo entre envíos**
   - El envío de cada mensaje espera un tiempo configurable (`DELAY` en segundos) antes de proceder al siguiente para no saturar la API.

### 5. **Registro de resultados**
   - Al finalizar, se genera `resultados.csv` con el historial de envíos, incluyendo nombre, teléfono, aula, estado, detalle y fecha de envío.

---

## 📤 Ejemplo de Mensaje Generado

El mensaje enviado a cada alumno es personalizado, por ejemplo:

```
Hola *Juan Pérez* 😊

Te saludamos desde la *Dirección de Admisión (DIAD)*.
Queremos informarte con mucho entusiasmo que tu aula asignada para el *examen Primer Parcial de CEPRE* es: *A-101* 🏫✨

Te recomendamos llegar con anticipación, llevar tu documento de identidad y todo lo necesario para rendir tu examen con tranquilidad.

¡Te deseamos mucho éxito en esta etapa! 🍀
Confía en ti y en todo lo que has aprendido 💪

Con aprecio,
*Dirección de Admisión (DIAD)*
*Universidad Nacional de Ingeniería*
```

---

## 🚀 Ejecución del Script

Para iniciar el proceso, asegúrate de que el entorno virtual esté activo y ejecuta:

```sh
python masivos.py
```

### Salida esperada en consola:

```
🚀 Iniciando envío masivo desde contactos.csv ...

✅ [+51987654321] Mensaje encolado correctamente (enviado)
✅ [+51912345678] Mensaje encolado correctamente (enviado)
📄 Envío completado. Resultados guardados en 'resultados.csv'
```

---

## 🧾 Archivo de Resultados (`resultados.csv`)

Al finalizar, el script crea un archivo con los detalles de cada envío:

| nombre        | telefono       | aula  | estado | detalle           | fecha_envio           |
|---------------|---------------|-------|--------|-------------------|-----------------------|
| Juan Pérez    | +51987654321  | A-101 | Éxito  | enviado           | 2025-10-09 14:23:11   |
| María López   | +51912345678  | B-203 | Error  | Token inválido    | 2025-10-09 14:24:02   |

---

## 🛠️ Posibles Errores y Soluciones

| Error                        | Causa posible                              | Solución                         |
|------------------------------|--------------------------------------------|----------------------------------|
| Error 401: Token inválido    | El token de la API es incorrecto/caducó    | Revisar el valor de `API_TOKEN`  |
| Error 400: Bad Request       | Número de teléfono o mensaje mal formateado| Verificar formato del número (+51...) |
| Error de conexión            | Sin Internet o API caída                   | Reintentar o verificar conexión  |
| Fila incompleta              | Faltan columnas en el CSV                  | Corregir el archivo contactos.csv|

---

## 🧪 Consejos y Buenas Prácticas

- **No enviar demasiados mensajes seguidos:** Ajusta `DELAY` a 2 o 3 segundos para evitar bloqueos.
- **Revisar `resultados.csv`** después de cada ejecución para detectar errores o mensajes no enviados.
- **Guardar copias de seguridad del CSV original** antes de procesar.
- **Mantener el token de la API en un archivo `.env`** para mayor seguridad.

### Ejemplo de uso de variables de entorno

**Archivo `.env`:**
```env
API_TOKEN=tu_token_aqui
```

**Lectura desde Python:**
```python
from dotenv import load_dotenv
import os
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
```
Recuerda instalar la librería dotenv con `pip install python-dotenv` si usas este enfoque.

---

## 🧰 Versión y Mantenimiento

- **Versión inicial:** v1.0.0
- **Autor:** Dirección de Admisión (DIAD) - Universidad Nacional de Ingeniería
- **Lenguaje:** Python 3.10+
- **Licencia:** MIT

---

## 🌐 Créditos y Agradecimientos

Proyecto desarrollado para la gestión eficiente del proceso de admisión de la Universidad Nacional de Ingeniería, con el apoyo del área DIAD.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.  
Puedes usarlo, modificarlo y distribuirlo libremente citando la fuente original.

---

© 2025 - Dirección de Admisión (DIAD)  
Universidad Nacional de Ingeniería