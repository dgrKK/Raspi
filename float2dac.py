import smbus
import time

# I2C setup
bus = smbus.SMBus(1)  # Use bus 1 on Raspberry Pi
DAC1_ADDR = 0x60      # Address of first MCP4725
DAC2_ADDR = 0x61      # Address of second MCP4725

# DAC configuration
VREF = 5.0            # Reference voltage of the DAC
STEP = 0.001          # Voltage resolution (1mV)
MAX_CODE = 4095       # Max 12-bit value

# Generate hash map for voltage → 12-bit digital code
dac_map = {}
for i in range(int(VREF / STEP) + 1):
    v = round(i * STEP, 3)
    code = int((v / VREF) * MAX_CODE)
    dac_map[v] = code

# Function to write 12-bit value to MCP4725
def write_dac(i2c_addr, value):
    value = max(0, min(4095, value))  # Clamp to 12-bit range
    msb = (value >> 4) & 0xFF
    lsb = (value << 4) & 0xFF
    bus.write_i2c_block_data(i2c_addr, 0x40, [msb, lsb])

# Example usage
def set_dacs(voltage1, voltage2):
    v1 = round(voltage1, 3)
    v2 = round(voltage2, 3)
    code1 = dac_map.get(v1)
    code2 = dac_map.get(v2)

    if code1 is not None:
        write_dac(DAC1_ADDR, code1)
    else:
        print(f"Voltage1 {v1}V out of range")

    if code2 is not None:
        write_dac(DAC2_ADDR, code2)
    else:
        print(f"Voltage2 {v2}V out of range")

# ---- Run Example ----
try:
    while True:
        vin1 = float(input("Enter voltage for DAC1 (0–5V): "))
        vin2 = float(input("Enter voltage for DAC2 (0–5V): "))
        set_dacs(vin1, vin2)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nStopped.")
