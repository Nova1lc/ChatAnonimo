from curses import COLORS
from nt import read
import requests
import time
import tkinter as tk
from tkinter import filedialog
import webbrowser
import pyaudio
import wave

from urllib3 import response

API_URL = "https://66cab9c759f4350f064fbdc9.mockapi.io/Bsz/api/V1/chats"
LITTERBOX_API = "https://cors-anywhere.herokuapp.com/https://catbox.moe/user/api.php"

#Colores
COLORES = {
    "AvaStrOficial": "\033[91m",  # Rojo
    "Z-Zuka": "\033[91m",  # Rojo
    "Firulais": "\033[91m",  # Rojo
    "Nova": "\033[92m",  # Verde
    "Caiser⁵⁵⁵Hack": "\033[94m",  # Azul
    "ciaser": "\033[94m",  # Azul
    "Mango_.": "\033[95m",  # Rosa
    "default": "\033[0m"  # Reset
}

#Funcion para mostrar el banner del menu
def banner():
    print("=" * 40)
    print("       [ CHAT ANÓNIMO ]       ")
    print("=" * 40)
    print("[1] Iniciar sesión")
    print("[2] Registrarse")
    print("[3] Salir")
    print("[4] Ayuda")
    print("=" * 40)

def registrarse():
    nombre = input("Ingrese un nuevo nombre de usuario: ").strip()
    if not nombre:
        print("[x] El nombre de usuario no puede estar vacio.")
        return None

    response = requests.post(API_URL, json={"name": nombre})
    if response.status_code == 201:
        print(f"[✓] Usuario {nombre} registrado existosamente.")
        return nombre
    else:
        print("[X] No se pudo registrar el usuario.")
        return None
    #Funcion para iniciar sesion
def iniciar_sesion():
    nombre = input("Ingrese su nombre de usuario: ").strip()
    if not nombre:
        print("[X] El nombre de usuario no puede estar vacio. ")
        return None
    
    #Funcion para obtener el historial de mensajes
def obtener_historia():
    response = requests.get(API_URL)
    if response.status_code == 200:
        mensaje = response.json()
        print("\n[ Historia de mensaje ]")
        for msg in mensaje:
            nombre = msg.get("name", "Desconocido")
            mensaje = msg.get("mensaje", "[Mensaje no disponible]")
            color = COLORS.get(nombre, COLORS["default"])
            print(f"{color}{nombre}\033[0m >> {mensaje}")
    
    else:
        print("[Error] No se pudo obtener el historia de mensajes.")
    
#Funcion para obtener enlaces compartidos
def obtener_galeria():
    response = requests.get(API_URL)
    if response.status_code == 200:
        mensaje = response.json()
        urls = [msg["mensaje"] for msg in mensaje if "https://" in msg.get("mensje", "")]
        if urls:
            print("\n [ Galeria de enlaces ]")
            for url in urls:
                print(url)
        else:
            print("[INFO] No hay enlaces en el historial de mensajes.")
    else:
        print("[ERROR] No se pudo obtener la galeria de enlaces.")

#Funcion para abrir enlaces en el navegador
def abrir_enlaces(enlace):
    print(f"[INFO] Abriendo {enlace} en el navegador. . .")
    webbrowser.open(enlace)

#Funcion para subir imagenes a Catbox
def subir_imagen():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Seleccionar una imagen", filetypes=[("imagen", "*.png;*.jpg;*.jpeg;*.webp;*.gif")])

    if not archivo:
        print("[X] No se selecciono ningun archivo.")
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
            return None
    print("[X] Error en la subida del archivo.")
    return None

#Funcion para grabar y subir audio
def grabar_audio():
    #Configuracion de grabacion
    formate = pyaudio.paInt16
    canales = 1
    tasa_muestreo = 44100
    duracion = 5 #Duracion de la grabacion en segundo
    tamaño_bufer = 1024

    p = pyaudio.PyAudio()

    print("[INFO] Grabando...")

    #Abrir el flujo de audio
    stream = p.open(format=formate, channels=canales, rate=tasa_muestreo, input=True, frames_per_buffer=tamaño_bufer)
    frames = []

    for i in range(0, int(tasa_muestreo / tamaño_bufer * duracion)):
        data = stream,read(tamaño_bufer)
        frames.append(data)
    
    print("[INFO] Grabacion terminado.")

    #Detener la grabacion
    stream.stop_stream()
    stream.close()
    p.terminate()

    #Guardar el archivo en formato WAV
    archivo_audio = "audio_grabado.wav"
    wf = wave.open(archivo_audio, 'wb')
    wf.setnchannels(canales)
    wf.setsampwidth(p.get_sample_size(formate))
    wf.setframerate(tasa_muestreo)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"[INFO] Audio guardado como {archivo_audio}.")
    return archivo_audio

#Funcion para subir el archiov de audio grabado
def subir_audio_grabado():
    archivo_audio = grabar_audio()

    if not archivo_audio:
        return None
        
    files = {'fileToUpload': open(archivo_audio, 'rb')}
    data = {'reqtype': 'fileupload'}

    try:
        response = requests.post(LITTERBOX_API, files=files, data=data)
        files['fiileToUpload'].close()
    except Exception as e:
        print(f"[X] Error al intentar subir el archivo: {e}")
        return None
    
    if response.status_code == 200:
        data = response.text.strip()
        if data.startswith("https://"):
            print(f"[✓] Audio cargado exitosamente: {data}")
            return data
    print("[X] Error en la subida del archivo.")
    return None

#Funcion para enviar mensajes
def enviar_mensaje(nombre):
    while True:
        mensaje = input(f"{nombre} (>> 'ms/' o 'exit/' o 'file/' o 'audio/' o 'help/' o 'galeri/' o 'web/'): ").strip()

        if mensaje.lower() == "exit/":
            print("[INFO] Saliendo del chat...")
            break
        elif mensaje.lower() == "help/":
            print("\n[ AYUDA ]")
            print("ms/ >> Para enviar mensajes")
            print("file/ >> Para Enviar Un Archivo Temporal")
            print("audio/ >> Para Grabar y Enviar un Mensaje de Audio")
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
                abrir_enlaces(enlace)
            else:
                print("[X] URL no valida.")
                continue
        elif mensaje.lower() == "file/":
            url_archivo = subir_imagen()
            if url_archivo:
                mensaje = url_archivo
            else: 
                continue
        elif mensaje.lower() == "audio/":
            url_audio = subir_audio_grabado()
            if url_audio:
                mensaje = f"Audio: {url_audio}"
            else: 
                continue
        elif not mensaje.startswith("ms/"):
            print("[X] Usa 'ms/' para enviar mensajes.")
            continue

        mensaje = mensaje[3:].strip()
        response = requests.post(API_URL, json={"name": nombre, "mensaje": mensaje})
        if response.status_code == 201:
            print(f"[✓] Mensaje enviados: {mensaje}")
            obtener_historia()
        else:
            print("[X] Error al enviar el mensaje.")
        time.sleep(3)

#Menu principal
while True:
    banner()
    opcion = input("Selecciona una opcion (1-4):").strip()

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
        print("audio/ >> Para Grabar y Enviar un Mensaje de Audio")
        print("exit/ >> Para salirse del chat")
        print("galeri/ >> Para ver los enlaces enviados")
        print("web/URL >> Para abrir un enlace")
    else:
        print("[X] Opcion no valida.")
        