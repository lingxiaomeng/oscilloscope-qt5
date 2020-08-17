# import spidev
#
# spi = spidev.SpiDev()
# bus = 1
# device = 0
# spi.open(bus, device)
# spi.max_speed_hz = 5000000
# spi.mode = 0x0
# spi.bits_per_word = 8
#
# a = spi.xfer([0x00, 0x10, 0x00])
# print(a)
# spi.close()
import socket

client_addr = ('127.0.0.1', 5555)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 5556))

sending = True
while True:
    data, address = s.recvfrom(1024)
    print(data)
    if sending:
        pass
    # s.sendto(bytes([0x00, 0x01, 0x02]), client_addr)
