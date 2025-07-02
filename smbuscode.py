import os
import sys
import time

# Try importing required libraries
try:
    import board
    import busio
    from adafruit_mcp4725 import MCP4725
except ImportError:
    print("Installing required libraries (with --break-system-packages)...")
    os.system("pip3 install --break-system-packages --upgrade adafruit-circuitpython-mcp4725 adafruit-blinka")
    os.execv(sys.executable, ['python3'] + sys.argv)

# Initialize I2C bus using Raspberry Pi's default I2C pins
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the MCP4725 DAC
dac = MCP4725(i2c)

# Reference voltage for MCP4725 (typically 3.3V on Raspberry Pi)
vref = 3.3

# Desired output voltage (change this value as needed, between 0 and vref)
target_voltage = 1.65  # Volts

# Set DAC output
normalized_value = target_voltage / vref
dac.normalized_value = normalized_value

print(f"Voltage output set to approx. {target_voltage:.2f} V (normalized value: {normalized_value:.3f})")

# Keep the output voltage stable (optional loop)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
