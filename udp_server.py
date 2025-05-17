import socket
import threading

# Configuración del servidor
IP = "0.0.0.0"
PORT = 5055
ADDR = (IP, PORT)
BUFFER_SIZE = 1024

# Diccionario para guardar jugadores registrados
clients = {}

# Socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

print(f"[UDP SERVER] Escuchando en {IP}:{PORT}")

def handle_messages():
    while True:
        try:
            msg, client_addr = server.recvfrom(BUFFER_SIZE)
            msg_decoded = msg.decode("utf-8")

            if client_addr not in clients:
                clients[client_addr] = msg_decoded  # Registramos con el primer mensaje (nombre)
                print(f"[NUEVO JUGADOR] {msg_decoded} desde {client_addr}")
            else:
                print(f"[MSG] {clients[client_addr]}: {msg_decoded}")

            # Reenvía a todos los clientes (tipo chat)
            for other_client in clients:
                server.sendto(f"{clients[client_addr]}: {msg_decoded}".encode(), other_client)

        except Exception as e:
            print(f"[ERROR] {e}")

# Hilo principal
threading.Thread(target=handle_messages).start()
