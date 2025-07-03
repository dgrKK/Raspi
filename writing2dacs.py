import smbus
import time

# I2C addresses of the two DACs
DAC1_ADDR = 0x60  # A0 pin to GND
DAC2_ADDR = 0x61  # A0 pin to VCC

# Create I2C bus object
bus = smbus.SMBus(1)

def write_dac(address, value):
    """Writes a 12-bit value to the DAC."""
    if not 0 <= value <= 4095:
        raise ValueError("Value must be between 0 and 4095")

    # MCP4725 expects two bytes: upper data and lower data
    upper = (value >> 4) & 0xFF
    lower = (value << 4) & 0xFF
    try:
        bus.write_i2c_block_data(address, 0x40, [upper, lower])  # 0x40 = write DAC register
        print(f"Wrote value {value} to DAC at address 0x{address:X}")
    except Exception as e:
        print(f"Error writing to DAC at 0x{address:X}: {e}")

# Example: ramp both DACs from 0 to 4095
for val in range(0, 4096, 256):
    write_dac(DAC1_ADDR, val)
    write_dac(DAC2_ADDR, 4095 - val)
    time.sleep(1)