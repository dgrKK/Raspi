import smbus
import time

# MCP4725 default I2C address
DAC_ADDR = 0x60
I2C_BUS = 1         # Use I2C bus 1 on Raspberry Pi
VREF = 3.3          # Reference voltage
DAC_RES = 4096      # 12-bit DAC

# Initialize I2C bus
bus = smbus.SMBus(I2C_BUS)

def write_dac(value):
    """Write a 12-bit value to MCP4725 DAC"""
    value = max(0, min(4095, value))  # Clamp value to 12 bits
    high_byte = (value >> 4) & 0xFF
    low_byte = (value << 4) & 0xFF
    bus.write_i2c_block_data(DAC_ADDR, 0x40, [high_byte, low_byte])

def generate_triangle_wave(delay=0.001, steps=100):
    """
    Generate a continuous triangle wave on MCP4725.
    
    delay: time between steps (seconds)
    steps: number of steps from 0 to max
    """
    while True:
        # Ramp up
        for i in range(steps + 1):
            dac_value = int((i / steps) * 4095)
            write_dac(dac_value)
            time.sleep(delay)

        # Ramp down
        for i in range(steps, -1, -1):
            dac_value = int((i / steps) * 4095)
            write_dac(dac_value)
            time.sleep(delay)

# Run triangular wave generation
try:
    print("Generating triangle wave on MCP4725...")
    generate_triangle_wave(delay=0.001, steps=100)
except KeyboardInterrupt:
    print("Stopped by user.")