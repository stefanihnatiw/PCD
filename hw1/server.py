import socket, sys

host = "127.0.0.1"
port = 65432


def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    while True:
        s.listen(5)
        client_socket, address = s.accept()

        prereq = client_socket.recv(100).decode()
        message_size, stop_and_wait = prereq.split()
        message_size = int(message_size)
        if stop_and_wait == "False":
            stop_and_wait = False
        else:
            stop_and_wait = True

        session_bytes = 0
        session_messages = 0
        while True:
            bytes_read = client_socket.recv(message_size)
            if not bytes_read:
                break
            session_bytes += sys.getsizeof(bytes_read)
            session_messages += 1

            if stop_and_wait:
                client_socket.send("Message was received".encode())

        print("Server session: tcp protocol, {} bytes read, {} messages read"
              .format(session_bytes, session_messages))


def udp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    while True:
        prereq, address = s.recvfrom(100)
        prereq = prereq.decode()

        message_size, stop_and_wait = prereq.split()
        message_size = int(message_size)
        if stop_and_wait == "False":
            stop_and_wait = False
        else:
            stop_and_wait = True

        session_bytes = 0
        session_messages = 0
        while True:
            bytes_read, address = s.recvfrom(message_size)
            bytes_read = bytes_read.decode()
            if bytes_read == "end":
                break

            session_bytes += sys.getsizeof(bytes_read)
            session_messages += 1

            if stop_and_wait:
                s.sendto("Message was received".encode(), address)

        print("Server session: udp protocol, {} bytes read, {} messages read"
              .format(session_bytes, session_messages))


def server_start(protocol):
    if protocol == "tcp":
        tcp_server()
    else:
        udp_server()


protocol = input("Protocol: ")
server_start(protocol)
