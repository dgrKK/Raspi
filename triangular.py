import smbus
import time
import numpy as np

# MCP4725 configuration
I2C_BUS = 1
DAC_ADDR = 0x60
VREF = 3.3
DAC_RES = 4096

# Set up I2C
bus = smbus.SMBus(I2C_BUS)

def write_dac(value):
    """Send 12-bit value to DAC"""
    value = value & 0x0FFF
    high_byte = (value >> 4) & 0xFF
    low_byte = (value << 4) & 0xFF
    bus.write_i2c_block_data(DAC_ADDR, 0x40, [high_byte, low_byte])

def triangular_wave(freq_hz=1, steps=100):
    """
    Generate a triangular waveform at given frequency.
    
    freq_hz: Frequency of the triangle wave (Hz)
    steps: Number of steps per half-wave
    """
    delay = 1 / (2 * freq_hz * steps)  # Time between steps (for both up & down)

    print(f"Generating triangular wave: {freq_hz} Hz, {steps*2} steps/cycle")

    while True:
        # Ramp up
        for i in range(steps):
            voltage = (i / steps) * VREF
            digital_val = int((voltage / VREF) * (DAC_RES - 1))
            write_dac(digital_val)
            time.sleep(delay)

        # Ramp down
        for i in range(steps, -1, -1):
            voltage = (i / steps) * VREF
            digital_val = int((voltage / VREF) * (DAC_RES - 1))
            write_dac(digital_val)
            time.sleep(delay)

# Run the wave generator
# Example: 1 Hz triangle wave, 100 steps per ramp
# Press Ctrl+C to stop
# triangular_wave(freq_hz=1, steps=100)
