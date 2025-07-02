import smbus
import time

bus = smbus.SMBus(1)
address = 0x60  # or 0x61

def write_dac(value):
    value &= 0x0FFF  # 12-bit
    byte1 = (value >> 4) & 0xFF
    byte2 = (value << 4) & 0xFF
    bus.write_i2c_block_data(address, 0x40, [byte1, byte2])

while True:
    for i in range(0, 4096, 256):
        write_dac(i)
        print(f"Output: {i}")
        time.sleep(0.5)