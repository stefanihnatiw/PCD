import os, socket, sys, time

filename = "buffer"
host = "127.0.0.1"
port = 65432


def gen_buffer(size):
    with open(filename, "wb") as f:
        f.truncate(size)


def tcp_client(message_size, stop_and_wait):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    start = time.time()
    s.send("{} {}".format(str(message_size), str(stop_and_wait)).encode())

    session_bytes = 0
    session_messages = 0
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(message_size)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            session_bytes += sys.getsizeof(bytes_read)
            session_messages += 1

            if stop_and_wait:
                acknowledge = s.recv(100).decode()
    s.close()

    end = time.time()
    print("Client session: {}s transfer time, {} bytes read, {} messages read"
          .format(end - start, session_bytes, session_messages))


def udp_client(message_size, stop_and_wait):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    start = time.time()
    s.sendto("{} {}".format(str(message_size), str(stop_and_wait)).encode(), (host, port))

    session_bytes = 0
    session_messages = 0
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(message_size)
            if not bytes_read:
                s.sendto("end".encode(), (host, port))
                break
            s.sendto(bytes_read, (host, port))
            session_bytes += sys.getsizeof(bytes_read)
            session_messages += 1

            if stop_and_wait:
                acknowledge, address = s.recvfrom(100)
                acknowledge = acknowledge.decode()
    s.close()

    end = time.time()
    print("Client session: {}s transfer time, {} bytes read, {} messages read"
          .format(end - start, session_bytes, session_messages))


def client_start(message_size, stop_and_wait, protocol):
    if protocol == "tcp":
        tcp_client(message_size, stop_and_wait)
    else:
        udp_client(message_size, stop_and_wait)


protocol = input("Protocol: ")
stop_and_wait = input("Stop and wait: ")
if stop_and_wait == "False":
    stop_and_wait = False
else:
    stop_and_wait = True

mb = input("Number MB: ")
gen_buffer(size=int(mb)*1024*1024)
client_start(message_size=4096, stop_and_wait=stop_and_wait, protocol=protocol)

os.remove(filename)
