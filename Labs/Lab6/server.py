import socket

print("Creating server...")
s = socket.socket()
s.bind(('0.0.0.0', 10000))
s.listen(0)

while True:
        client, addr = s.accept()
        while True:
                content = client.recv(32).decode("utf-8")
                if len(content) == 0:
                        break
                else:
                        print(content)
        # print("Closing connection")
        client.close()