import json
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8558553993:AAGSo6TDHZnULCLF7dGlB_K1LflYoTOHCwU"
ODOO_BASE = "http://localhost:8069"  
API = f"{ODOO_BASE}/gestion/apirest/socio"

def parse_comando(texto: str):
    """
    Devuelve: (accion, dicDatos) o (None, None)
    Soporta: Crear/Modificar/Consultar/Borrar con clave="valor"
    """
    if not texto:
        return None, None

    partes = [p.strip() for p in texto.split(",") if p.strip()]
    if not partes:
        return None, None

    accion = partes[0].lower()

    pares = re.findall(r'(\w+)\s*=\s*"([^"]*)"', texto)
    datos = {k: v for k, v in pares}

    if "num_socio" in datos:
        try:
            datos["num_socio"] = int(datos["num_socio"])
        except ValueError:
            return accion, {"error": "num_socio debe ser número"}

    return accion, datos

def odoo_crear(datos):
    r = requests.post(API, json=datos, timeout=10)
    return r.status_code, r.text

def odoo_modificar(datos):
    r = requests.put(API, json=datos, timeout=10)
    return r.status_code, r.text

def odoo_consultar(num_socio):
    params = {"data": json.dumps({"num_socio": num_socio})}
    r = requests.get(API, params=params, timeout=10)
    return r.status_code, r.text

def odoo_borrar(num_socio):
    params = {"data": json.dumps({"num_socio": num_socio})}
    r = requests.delete(API, params=params, timeout=10)
    return r.status_code, r.text

async def handler_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (update.message.text or "").strip()
    accion, datos = parse_comando(texto)

    if accion is None:
        await update.message.reply_text("Orden no soportada")
        return

    if isinstance(datos, dict) and datos.get("error"):
        await update.message.reply_text(f"Error: {datos['error']}")
        return

    try:
        if accion == "crear":
            if not all(k in datos for k in ("num_socio", "nombre", "apellidos")):
                await update.message.reply_text("Faltan datos. Ej: Crear, nombre=\"A\",apellidos=\"B\", num_socio=\"1\"")
                return
            code, body = odoo_crear(datos)
            await update.message.reply_text(f"HTTP {code}\n{body}")

        elif accion == "modificar":
            if not all(k in datos for k in ("num_socio", "nombre", "apellidos")):
                await update.message.reply_text("Faltan datos. Ej: Modificar, nombre=\"A\",apellidos=\"B\", num_socio=\"1\"")
                return
            code, body = odoo_modificar(datos)
            await update.message.reply_text(f"HTTP {code}\n{body}")

        elif accion == "consultar":
            if "num_socio" not in datos:
                await update.message.reply_text("Faltan datos. Ej: Consultar, num_socio=\"1\"")
                return
            code, body = odoo_consultar(datos["num_socio"])
            await update.message.reply_text(f"HTTP {code}\n{body}")

        elif accion == "borrar":
            if "num_socio" not in datos:
                await update.message.reply_text("Faltan datos. Ej: Borrar, num_socio=\"1\"")
                return
            code, body = odoo_borrar(datos["num_socio"])
            await update.message.reply_text(f"HTTP {code}\n{body}")

        else:
            await update.message.reply_text("Orden no soportada")

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Error llamando a Odoo: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_texto))
    app.run_polling()

if __name__ == "__main__":
    main()
