import socket

HOST = '143.110.215.221'
PORT = 10000

def main():
    connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST, PORT))
    data = connection.recv(PORT)
    print(data)
    data = connection.recv(PORT)
    print(data)


if __name__ == "__main__":
    main()
