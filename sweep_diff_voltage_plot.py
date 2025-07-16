import numpy as np
import matplotlib.pyplot as plt
import smbus
import time

# Constants
v1_fixed = 0.0  # V1 is fixed at 0V
v2_start = 0.001
v2_end = 5.0
step = 0.001

# I2C addresses of the two DACs
DAC1_ADDR = 0x60  # A0 pin to GND
DAC2_ADDR = 0x61  # A0 pin to VCC

# Create I2C bus object
bus = smbus.SMBus(2)

# Generate sweep values
v2_values = np.arange(v2_start, v2_end + step, step)
v1_values = np.full_like(v2_values, v1_fixed)
v_diff = v2_values - v1_values  # should be same as v2_values

# Placeholder for output readings
output_readings = []

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

def write_voltage_to_pin(channel, voltage):
    """
    Write the given voltage to the specified DAC channel.
    Converts voltage to 12-bit DAC value (assuming 5V reference).
    """
    # Convert voltage to 12-bit DAC value (0-4095)
    # Assuming 5V reference voltage
    v_ref = 5.0
    dac_value = int((voltage / v_ref) * 4095)
    
    # Clamp to valid range
    dac_value = max(0, min(4095, dac_value))
    
    # Map channel names to DAC addresses
    if channel == 'v1_pin':
        write_dac(DAC1_ADDR, dac_value)
    elif channel == 'v2_pin':
        write_dac(DAC2_ADDR, dac_value)
    else:
        raise ValueError(f"Unknown channel: {channel}")

def read_output_voltage(smbus):

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
    bus = smbus.SMBus(1)

# Combine configuration
    CONFIG = (OS_SINGLE | MUX_SINGLE_AIN0 | GAIN_4_096V |
          MODE_SINGLE | DATA_RATE | COMP_DISABLE)
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
     
    return raw 


# Main sweep loop
for v2 in v2_values:
    # Write voltages to hardware
    write_voltage_to_pin(channel='v1_pin', voltage=v1_fixed)
    write_voltage_to_pin(channel='v2_pin', voltage=v2)
    
    # Read output from hardware
    bus = smbus.SMBus(1)
    measured_output = read_output_voltage(bus)
    output_readings.append(measured_output)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(v_diff, output_readings, label='Output Voltage', color='blue')
plt.xlabel('Input Voltage Difference (V2 - V1) [V]')
plt.ylabel('Output Voltage [V]')
plt.title('Measured Output Voltage vs Input Voltage Difference')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
