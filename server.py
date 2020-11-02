# import spidev
import socket
import struct

import select
import queue
import threading
import time

import random

queue_send = queue.Queue()


class SpiRead(threading.Thread):
    def __init__(self):
        super().__init__()
        self.is_sending = False
        self.is_stop = False

    def run(self) -> None:
        while not self.is_stop:
            if self.is_sending:
                # print('put')
                spi_data = b''
                for i in range(2048):
                    d1 = [0, random.randint(0, 100), random.randint(0, 100)]
                    d2 = [0, random.randint(0, 1), random.randint(0, 120)]
                    spi_data = spi_data + bytes([d1[1], d1[2], d2[1], d2[2]])
                queue_send.put_nowait(spi_data)
                time.sleep(0.3)


# from socket import *

# spi = spidev.SpiDev()
# bus = 1
# device = 0
# spi.open(bus,device)
# spi.max_speed_hz = 5000000
# spi.mode = 0x0
# spi.bits_per_word = 8


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5551))
server.setblocking(False)
server.listen(5)

spi_read = SpiRead()
spi_read.start()

inputs = [server]
outputs = []
while True:
    r_list, w_list, e_list = select.select(inputs, outputs, inputs)
    for s in r_list:
        if s == server:
            print("新的客户端连接")
            new_sock, addr = s.accept()
            inputs.append(new_sock)
        else:
            data = None
            try:
                data = s.recv(1024)
            except ConnectionResetError as err:
                print(err)

            if data:
                print("接收到客户端信息")
                print(data)

                if data == b'START':
                    spi_read.is_sending = True
                elif data == b'STOP':
                    spi_read.is_sending = False

                if s not in outputs:
                    outputs.append(s)
            else:
                print("客户端断开连接")
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()

    for s in w_list:
        # print(s)
        try:
            next_msg = queue_send.get_nowait()  # 非阻塞获取
            # print(next_msg)
        except queue.Empty:
            err_msg = "Output Queue is Empty!"
            # print(err_msg)
            # g_logFd.writeFormatMsg(g_logFd.LEVEL_INFO, err_msg)
        else:
            s.send(next_msg)
