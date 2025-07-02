import smbus
import time

# Initialize I2C bus
bus = smbus.SMBus(1)  # Use bus 1 on Raspberry Pi 3
address = 0x60        # Default I2C address for MCP4725

def write_dac(value):
    """
    Send 12-bit value to MCP4725 DAC over I2C
    value: int (0-4095)
    """
    if value < 0 or value > 4095:
        raise ValueError("Value must be between 0 and 4095")

    # MCP4725 expects two data bytes:
    # - upper 4 bits of value go in upper data byte (shifted left by 4)
    # - lower 8 bits go in second byte
    high_byte = (value >> 8) & 0x0F  # Only lower 4 bits
    low_byte = value & 0xFF

    # Control byte: 0x40 means "write DAC register" (fast mode)
    control = 0x40

    # Send all three bytes: control, high, low
    bus.write_i2c_block_data(address, control, [high_byte, low_byte])

# Main loop
try:
    while True:
        user_input = input("Enter DAC value (0-4095): ")
        if user_input.strip() == "":
            continue
        try:
            val = int(user_input)
            write_dac(val)
            print(f"Sent value {val} to DAC")
        except ValueError:
            print("Invalid input. Enter an integer between 0 and 4095.")
except KeyboardInterrupt:
    print("\nExiting...")
