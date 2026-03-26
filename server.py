import socket


class Server:
    def __init__(self):
        self.HOST = "0.0.0.0"
        self.PORT = 5001

    def __get_ip(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            self.HOST = s.getsockname()[0]
        finally:
            s.close()

    def run(self):
        self.__get_ip()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print(f"Server listening on {self.HOST}:{self.PORT}")

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        message = f"[SERVER]: mensagem recebida: {data.decode()}"
                        print(message)
                        conn.sendall(message.encode())
