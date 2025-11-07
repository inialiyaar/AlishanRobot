import socket
import time

def get_ping(host="8.8.8.8", port=53, timeout=3):
    try:
        start = time.time()
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        end = time.time()
        sock.close()
        ping_time = round((end - start) * 1000, 2)
        return f"{ping_time}ms"
    except socket.error:
        return "Ping failed"
