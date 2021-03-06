import socket, threading

def handle_messages(connection: socket.socket):
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Erro ao cuidar da mensagem do servidor: {e}')
            connection.close()
            break

def client() -> None:

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 11000

    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Conectado ao chat')
        while True:
            msg = input()

            if msg == 'quit':
                break

            socket_instance.send(msg.encode())

        socket_instance.close()

    except Exception as e:
        print(f'Erro ao conectar no socket do servidor: {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
