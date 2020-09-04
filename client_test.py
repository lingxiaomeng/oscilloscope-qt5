import socket


def main():
    # 1.创建套接字socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.连接服务器

    dest_addr = ('192.168.137.150', 5550)
    tcp_socket.connect(dest_addr)

    # 3. 接收/发送数据
    tcp_socket.send(b'START')

    # 接收服务器发送的数据
    recv_data = tcp_socket.recv(1024)
    print(recv_data)

    # 4. 关闭套接字socket
    tcp_socket.close()


if __name__ == "__main__":
    main()
