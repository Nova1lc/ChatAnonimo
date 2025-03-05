import requests
import time
import tkinter as tk
from tkinter import filedialog
import webbrowser

# Configuración de API
API_URL = "https://66cab9c759f4350f064fbdc9.mockapi.io/Bsz/api/V1/chats"
LITTERBOX_API = "https://cors-anywhere.herokuapp.com/https://catbox.moe/user/api.php"

# Colores por usuario
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

# Función para mostrar el banner del menú
def banner():
    print("=" * 40)
    print("       [ CHAT ANÓNIMO ]       ")
    print("=" * 40)
    print("[1] Iniciar sesión")
    print("[2] Registrarse")
    print("[3] Salir")
    print("[4] Ayuda")
    print("=" * 40)

# Función para registrar un usuario
def registrarse():
    nombre = input("Ingrese un nuevo nombre de usuario: ").strip()
    if not nombre:
        print("[X] El nombre de usuario no puede estar vacío.")
        return None
    
    response = requests.post(API_URL, json={"name": nombre})
    if response.status_code == 201:
        print(f"[✓] Usuario {nombre} registrado exitosamente.")
        return nombre
    else:
        print("[X] No se pudo registrar el usuario.")
        return None

# Función para iniciar sesión
def iniciar_sesion():
    nombre = input("Ingrese su nombre de usuario: ").strip()
    if not nombre:
        print("[X] El nombre de usuario no puede estar vacío.")
        return None
    return nombre

# Función para obtener el historial de mensajes
def obtener_historial():
    response = requests.get(API_URL)
    if response.status_code == 200:
        mensajes = response.json()
        print("\n[ Historial de Mensajes ]")
        for msg in mensajes:
            nombre = msg.get("name", "Desconocido")
            mensaje = msg.get("mensje", "[Mensaje no disponible]")
            color = COLORS.get(nombre, COLORS["default"])
            print(f"{color}{nombre}\033[0m >> {mensaje}")
    else:
        print("[ERROR] No se pudo obtener el historial de mensajes.")

# Función para obtener enlaces compartidos
def obtener_galeria():
    response = requests.get(API_URL)
    if response.status_code == 200:
        mensajes = response.json()
        urls = [msg["mensje"] for msg in mensajes if "https://" in msg.get("mensje", "")]
        if urls:
            print("\n[ Galería de Enlaces ]")
            for url in urls:
                print(url)
        else:
            print("[INFO] No hay enlaces en el historial de mensajes.")
    else:
        print("[ERROR] No se pudo obtener la galería de enlaces.")

# Función para abrir enlaces en el navegador
def abrir_enlace(enlace):
    print(f"[INFO] Abriendo {enlace} en el navegador...")
    webbrowser.open(enlace)

# Función para subir imágenes a Catbox
def subir_imagen():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Seleccionar una imagen", filetypes=[("Imagen", "*.png;*.jpg;*.jpeg;*.webp;*.gif")])
    
    if not archivo:
        print("[X] No se seleccionó ningún archivo.")
        return None

    files = {'fileToUpload': open(archivo, 'rb')}
    data = {'reqtype': 'fileupload'}
    
    try:
        response = requests.post(LITTERBOX_API, files=files, data=data)
        files['fileToUpload'].close()
    except Exception as e:
        print(f"[X] Error al intentar subir el archivo: {e}")
        return None

    if response.status_code == 200:
        data = response.text.strip()
        if data.startswith("https://"):
            print(f"[✓] Imagen cargada exitosamente: {data}")
            return data
    print("[X] Error en la subida del archivo.")
    return None

# Función para enviar mensajes
def enviar_mensaje(nombre):
    while True:
        mensaje = input(f"{nombre} (>> 'ms/' o 'exit/' o 'file/' o 'help/' o 'galeri/' o 'web/'): ").strip()
        
        if mensaje.lower() == "exit/":
            print("[INFO] Saliendo del chat...")
            break
        elif mensaje.lower() == "help/":
            print("\n[ AYUDA ]")
            print("ms/ >> Para enviar mensajes")
            print("file/ >> Para Enviar Un Archivo Temporal")
            print("exit/ >> Para salir del chat")
            print("galeri/ >> Para ver enlaces compartidos")
            print("web/URL >> Para abrir un enlace")
            continue
        elif mensaje.lower() == "galeri/":
            obtener_galeria()
            continue
        elif mensaje.lower().startswith("web/"):
            enlace = mensaje[4:].strip()
            if enlace.startswith("http"):
                abrir_enlace(enlace)
            else:
                print("[X] URL no válida.")
            continue
        elif mensaje.lower() == "file/":
            url_archivo = subir_imagen()
            if url_archivo:
                mensaje = url_archivo
            else:
                continue
        elif not mensaje.startswith("ms/"):
            print("[X] Usa 'ms/' para enviar mensajes.")
            continue
        
        mensaje = mensaje[3:].strip()
        response = requests.post(API_URL, json={"name": nombre, "mensje": mensaje})
        if response.status_code == 201:
            print(f"[✓] Mensaje enviado: {mensaje}")
            obtener_historial()
        else:
            print("[X] Error al enviar el mensaje.")
        time.sleep(3)

# Menú principal
while True:
    banner()
    opcion = input("Selecciona una opción (1-4): ").strip()
    
    if opcion == "1":
        usuario = iniciar_sesion()
        if usuario:
            enviar_mensaje(usuario)
    elif opcion == "2":
        registrarse()
    elif opcion == "3":
        print("[INFO] Saliendo del chat. ¡Hasta luego!")
        break
    elif opcion == "4":
        print("\n[ AYUDA ]")
            print("ms/ >> Para enviar mensajes, ejemplo: ms/Hola Mundo")
            print("file/ >> Para Enviar Un Archivo Temporal")
            print("exit/ >> Para salirse del chat")
            print("galeri/ >> Para ver los enlaces enviados")
            print("web/URL >> Para abrir un enlace")
    else:
        print("[X] Opción no válida.")
