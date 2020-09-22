# import spidev
import socket
import struct

import select
import queue
import threading
import time

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

                d1 = [0, 0, 1]
                d2 = [0, 0, 17]
                d3 = [0, 0, 234]
                d4 = [0, 0, 214]
                abs = (d1[2] << 8) + d2[2]
                phase = (d3[2] << 8) + d4[2]
                res = struct.pack('HH', abs, phase)

                queue_send.put_nowait(res)
                time.sleep(0.01)


# from socket import *

# spi = spidev.SpiDev()
# bus = 1
# device = 0
# spi.open(bus,device)
# spi.max_speed_hz = 5000000
# spi.mode = 0x0
# spi.bits_per_word = 8


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5550))
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
            data = s.recv(1024)
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
