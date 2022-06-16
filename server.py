import socket, threading


connections = []

def handle_user_connection(connection: socket.socket, address: str) -> None:

    while True:
        try:
            msg = connection.recv(1024)

            if msg:
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                broadcast(msg_to_send, connection)
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Erro na manutencao da conexao do usuario: {e}')
            remove_connection(connection)
            break


def broadcast(message: str, connection: socket.socket) -> None:



    for client_conn in connections:
        if client_conn != connection:
            try:
                client_conn.send(message.encode())
            except Exception as e:
                print('erro na transmissao da mensagem: {e}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:

    if conn in connections:
        conn.close()
        connections.remove(conn)


def server() -> None:


    LISTENING_PORT = 11000
    
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Servidor rodando!')
        
        while True:

            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'Um erro ocorreu na instancia do socket {e}')
    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()


if __name__ == "__main__":
    server()
