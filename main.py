import re
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRecent

api_id = ''
api_hash = ''
phone_number = '+'
channel_id = '' # group ID

# Iniciar sesión con Telethon
client = TelegramClient('session_name', api_id, api_hash)
client.connect()

# Verificar si el usuario está autenticado
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Ingrese el código de verificación: '))

# Leer la lista de canales desde el archivo 'channels.txt'
with open('channels.txt', 'r') as file:
    channels = [line.strip() for line in file]

# Definir el formato y las palabras clave
pattern = re.compile(r'\b\d{16}\|\d{2}\|\d{4}\|\d{3}\b')
keywords = ['𝑨𝑷𝑷𝑹𝑶𝑽𝑬𝑫', 'Approved']

# Lista para almacenar los resultados
resultados = []

# Bucle a través de los canales
for channel_username in channels:
    try:
        # Obtener el ID del canal
        channel_entity = client.get_entity(channel_username)

        # Obtener mensajes recientes del canal
        messages = client.get_messages(channel_entity, limit=100)

        # Bucle a través de los mensajes
        for message in messages:
            # Verificar si el mensaje contiene las palabras clave y coincide con el formato
            if any(keyword.lower() in message.text.lower() for keyword in keywords) and re.search(pattern, message.text):
                resultados.append(f"Mensaje encontrado en el canal {channel_username}:\n{message.text}\n")

    except Exception as e:
        print(f"Error al procesar el canal {channel_username}: {e}")

# Enviar los resultados al canal especificado
if resultados:
    resultados_text = "\n".join(resultados)
    client.send_message(channel_id, resultados_text)
    print(f"Resultados enviados al canal {channel_id}")

# Cerrar la conexión de Telethon
client.disconnect()
