import requests
import time
import tkinter as tk
from tkinter import filedialog

API_URL = "https://66cab9c759f4350f064fbdc9.mockapi.io/Bsz/api/V1/chats"
LITTERBOX_API = "https://litterbox.catbox.moe/resources/internals/api.php"

COLORS = {
    "AvaStrOficial": "\033[91m",  # Rojo
    "Z-Zuka": "\033[91m",  # Rojo
    "Firulais": "\033[91m",  # Rojo
    "Nova": "\033[92m",  # Verde
    "Caiser⁵⁵⁵Hack": "\033[94m",  # Azul
    "ciaser": "\033[94m",  # Azul
    "Mango_.": "\033[95m",  # Rosa
    "default": "\033[0m"  # Reset
}

def banner():
    print("=" * 40)
    print("       [ CHAT ANÓNIMO ]       ")
    print("=" * 40)
    print("[1] Iniciar sesión")
    print("[2] Ver historial de mensajes")
    print("[3] Salir")
    print("[4] Ayuda")
    print("=" * 40)

def obtener_historial():
    response = requests.get(API_URL)
    if response.status_code == 200:
        mensajes = response.json()
        print("\n[ Historial de Mensajes ]")
        for msg in mensajes:
            nombre = msg.get("name", "Desconocido")
            mensaje = msg.get("mensje", "[Mensaje no disponible]")
            # Aplicando colores según el nombre de usuario
            color = COLORS.get(nombre, COLORS["default"])
            print(f"{color}{nombre}\033[0m >> {mensaje}")
        
        if len(mensajes) >= 100:
            eliminar_todos_los_mensajes()
    else:
        print("[ERROR] No se pudo obtener el historial de mensajes.")

def eliminar_todos_los_mensajes():
    response = requests.get(API_URL)
    if response.status_code == 200:
        mensajes = response.json()
        for msg in mensajes:
            try:
                delete_response = requests.delete(f"{API_URL}/{msg['id']}")
                if delete_response.status_code == 200:
                    print(f"[✓] Mensaje de {msg['name']} eliminado.")
                else:
                    print(f"[X] No se pudo eliminar el mensaje de {msg['name']}. Código: {delete_response.status_code}")
                time.sleep(0.5)
            except Exception as e:
                print(f"[ERROR] Eliminando mensaje de {msg['name']}: {e}")
        print("[INFO] Se han eliminado todos los mensajes debido a la cantidad máxima permitida (100).")
    else:
        print("[ERROR] No se pudo eliminar los mensajes.")

def iniciar_sesion():
    nombre = input("Ingrese su nombre de usuario: ").strip()
    
    if not nombre:
        print("[X] El nombre de usuario no puede estar vacío.")
        return None

    return nombre

def subir_imagen():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    
    if not file_path:
        print("[X] No se seleccionó ningún archivo.")
        return None
    
    with open(file_path, "rb") as file:
        files = {"fileToUpload": file}
        data = {"reqtype": "fileupload", "time": "1h"}
        response = requests.post(LITTERBOX_API, files=files, data=data)
        
        if response.status_code == 200:
            return response.text.strip()
        else:
            print("[X] Error al subir el archivo.")
            return None

def mostrar_galeria_links():
    response = requests.get(API_URL)
    if response.status_code == 200:
        mensajes = response.json()
        print("\n[ Galería de Links ]")
        for msg in mensajes:
            nombre = msg.get("name", "Desconocido")
            mensaje = msg.get("mensje", "")
            # Verifica si el mensaje contiene un enlace
            if "http" in mensaje:
                print(f"{nombre} >> {mensaje}")
    else:
        print("[ERROR] No se pudo obtener los mensajes con enlaces.")

def enviar_mensaje(nombre):
    while True:
        mensaje = input(f"{nombre} (>> 'ms/' o 'exit/' o 'file/' o 'help/' o 'galeri/'): ").strip()

        if mensaje.lower() == "exit/":
            print("[INFO] Saliendo del chat...")
            break

        if mensaje.lower() == "help/":
            print("\n[ AYUDA ]")
            print("ms/ >> Para enviar mensajes, ejemplo: ms/Hola Mundo")
            print("file/ >> Para Enviar Un Archivo Temporal")
            print("exit/ >> Para salirse del chat")
            print("galeri/ >> Para ver los enlaces enviados")
            print("=" * 40)
            continue

        if mensaje.lower() == "galeri/":
            mostrar_galeria_links()
            continue

        if mensaje.startswith("file/"):
            imagen_url = subir_imagen()
            if imagen_url:
                mensaje = imagen_url
            else:
                continue
        elif not mensaje.startswith("ms/"):
            print("[X] Debes empezar tu mensaje con 'ms/'. Ejemplo: ms/Hola a todos.")
            continue
        else:
            mensaje = mensaje[3:].strip()
        
        nuevo_mensaje = {"name": nombre, "mensje": mensaje}
        response = requests.post(API_URL, json=nuevo_mensaje)
        if response.status_code == 201:
            print(f"[✓] Mensaje enviado: {mensaje}")
        else:
            print("[X] No se pudo enviar el mensaje.")

        print("\n[ Historial de Mensajes ]")
        obtener_historial()
        
        time.sleep(3)

while True:
    banner()
    opcion = input("Selecciona una opción (1-4): ").strip()

    if opcion == "1":
        usuario = iniciar_sesion()
        if usuario:
            enviar_mensaje(usuario)
    elif opcion == "2":
        obtener_historial()
    elif opcion == "3":
        print("[INFO] Saliendo del chat. ¡Hasta luego!")
        break
    elif opcion == "4":
        print("\n[ AYUDA ]")
        print("ms/ >> Para enviar mensajes, ejemplo: ms/Hola Mundo")
        print("file/ >> Para Enviar Un Archivo Temporal")
        print("exit/ >> Para salirse del chat")
        print("galeri/ >> Para ver los enlaces enviados")
        print("=" * 40)
    else:
        print("[X] Opción no válida. Intenta de nuevo.")
