import requests
import time

API_URL = "https://66fb32f08583ac93b40b1c77.mockapi.io/Bsz/Admin/panel/ChatGeneral"

def banner():
    """ Muestra el banner principal del chat """
    print("=" * 40)
    print("       🔹 CHAT ANÓNIMO 🔹       ")
    print("=" * 40)
    print("1️⃣ Iniciar sesión")
    print("2️⃣ Registrarse")
    print("3️⃣ Salir")
    print("=" * 40)

def registrar_usuario():
    """ Permite registrar un nuevo usuario en la API """
    nombre = input("Elige un nombre de usuario: ").strip()
    
    if not nombre:
        print("❌ El nombre de usuario no puede estar vacío.")
        return None

    # Verificar si el usuario ya existe
    response = requests.get(API_URL)
    if response.status_code == 200:
        usuarios = response.json()
        for user in usuarios:
            if user["name"].lower() == nombre.lower():
                print("⚠️ El usuario ya existe. Prueba otro nombre.")
                return None

    # Crear usuario en la API
    nuevo_usuario = {"name": nombre}
    response = requests.post(API_URL, json=nuevo_usuario)

    if response.status_code == 201:
        print(f"✅ Usuario '{nombre}' registrado con éxito.")
        return nombre
    else:
        print("❌ Error al registrar usuario.")
        return None

def iniciar_sesion():
    """ Permite al usuario iniciar sesión """
    nombre = input("Ingrese su nombre de usuario: ").strip()
    
    if not nombre:
        print("❌ El nombre de usuario no puede estar vacío.")
        return None

    response = requests.get(API_URL)
    if response.status_code == 200:
        usuarios = response.json()
        for user in usuarios:
            if user["name"].lower() == nombre.lower():
                print(f"✅ Bienvenido de nuevo, {nombre}!")
                return nombre

    print("❌ Usuario no encontrado.")
    return None

def enviar_mensaje(nombre):
    """ Permite enviar un mensaje al chat con el formato ms/ """
    while True:
        mensaje = input(f"{nombre} (escribe tu mensaje con 'ms/'): ").strip()
        
        if mensaje.lower() == "/salir":
            print("👋 Saliendo del chat...")
            break
        
        if not mensaje.startswith("ms/"):
            print("⚠️ Debes empezar tu mensaje con 'ms/'. Ejemplo: ms/Hola a todos!")
            continue

        # Enviar mensaje con etiqueta
        nuevo_mensaje = {"name": nombre, "mensje": mensaje}
        response = requests.post(API_URL, json=nuevo_mensaje)
        if response.status_code == 201:
            print("📩 Mensaje enviado.")
        else:
            print("❌ Error al enviar el mensaje.")

        # Pausa antes de poder enviar el siguiente mensaje
        print("⏳ Pausa... puedes enviar más mensajes después de unos segundos.")
        time.sleep(3)  # Pausa de 3 segundos

def recibir_mensajes():
    """ Obtiene y muestra mensajes en tiempo real """
    mensajes_vistos = set()
    
    while True:
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                mensajes = response.json()
                for msg in mensajes:
                    mensaje_id = msg.get("id")
                    nombre = msg.get("name", "Desconocido")
                    mensaje = msg.get("mensje", "[Mensaje no disponible]")

                    if mensaje_id and mensaje_id not in mensajes_vistos:
                        # Mostrar el mensaje correctamente
                        if mensaje != "[Mensaje no disponible]":
                            print(f"\n{nombre}: {mensaje}")
                        else:
                            print(f"\n{nombre}: [Mensaje no disponible]")

                        mensajes_vistos.add(mensaje_id)
            else:
                print("⚠️ Error al obtener mensajes.")
        except Exception as e:
            print("❌ Error de conexión:", e)

        time.sleep(3)  # Se actualiza cada 3 segundos

# -------- MENÚ PRINCIPAL -------- #
while True:
    banner()
    opcion = input("Selecciona una opción (1-3): ").strip()

    if opcion == "1":
        usuario = iniciar_sesion()
        if usuario:
            try:
                recibir_mensajes()
            except KeyboardInterrupt:
                print("\n👋 Has salido del chat.")
                break
            enviar_mensaje(usuario)

    elif opcion == "2":
        usuario = registrar_usuario()
        if usuario:
            try:
                recibir_mensajes()
            except KeyboardInterrupt:
                print("\n👋 Has salido del chat.")
                break
            enviar_mensaje(usuario)

    elif opcion == "3":
        print("👋 Saliendo del chat. ¡Hasta luego!")
        break

    else:
        print("❌ Opción no válida. Intenta de nuevo.")
