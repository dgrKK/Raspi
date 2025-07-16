import smbus
import time

# ADS1115 I2C address (default)
ADS1115_ADDR = 0x48

# Register addresses
POINTER_CONVERT = 0x00
POINTER_CONFIG = 0x01

# PGA setting for ±4.096V full-scale range
GAIN_4_096V = 0x0200  # LSB size = 125 µV

# Single-ended input on AIN0 (MUX = 100)
MUX_SINGLE_AIN0 = 0x4000

# Other config bits
MODE_SINGLE = 0x0100
DATA_RATE = 0x0080
COMP_DISABLE = 0x0003
OS_SINGLE = 0x8000

# Combine configuration
CONFIG = (OS_SINGLE | MUX_SINGLE_AIN0 | GAIN_4_096V |
          MODE_SINGLE | DATA_RATE | COMP_DISABLE)

# Initialize I2C
bus = smbus.SMBus(1)

def read_voltage_ain0():
    # Write config to start conversion
    config_bytes = [(CONFIG >> 8) & 0xFF, CONFIG & 0xFF]
    bus.write_i2c_block_data(ADS1115_ADDR, POINTER_CONFIG, config_bytes)

    # Wait for conversion (minimum 1ms, we use 10ms)
    time.sleep(0.01)

    # Read conversion result
    result = bus.read_i2c_block_data(ADS1115_ADDR, POINTER_CONVERT, 2)
    raw = (result[0] << 8) | result[1]
    
    # Handle two's complement
    if raw > 0x7FFF:
        raw -= 0x10000

    # Convert to voltage (LSB = 125uV for ±4.096V)
    voltage = raw * 4.096 / 32768.0
    return raw, voltage

# Main loop
try:
    while True:
        raw, voltage = read_voltage_ain0()
        print(f"AIN0 Raw: {raw}, Voltage: {voltage:.4f} V")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped.")
