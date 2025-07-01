import os
import sys

# Auto-install missing libraries
try:
    import board
    import busio
    from adafruit_mcp4725 import MCP4725
except ImportError:
    print("Installing required libraries...")
    os.system("pip3 install --upgrade adafruit-circuitpython-mcp4725")
    os.system("pip3 install --upgrade adafruit-blinka")
    os.execv(sys.executable, ['python3'] + sys.argv)

import time

# Set up I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create MCP4725 instance
dac = MCP4725(i2c)

# Set reference voltage (typically 3.3V on Raspberry Pi)
vref = 3.3

# Target output voltage (change this value as needed)
target_voltage = 1.65  # Volts (half of 3.3V)

# Convert voltage to 12-bit value
dac_value = int((target_voltage / vref) * 4095)
dac.normalized_value = target_voltage / vref

print(f"Output voltage set to approximately {target_voltage:.2f} V")

# Keep output stable
while True:
    time.sleep(1)
