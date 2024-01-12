import time

class AS7331:
    def __init__(self, i2c_bus):
        self._i2c_bus = i2c_bus

    def get_chip_id(self):
        c = self._i2c_bus.read_byte(AS7331_ADDRESS, AS7331_AGEN)
        return c

    def power_down(self):
        temp = self._i2c_bus.read_byte(AS7331_ADDRESS, AS7331_OSR)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_OSR, temp & ~(0x40))

    def power_up(self):
        temp = self._i2c_bus.read_byte(AS7331_ADDRESS, AS7331_OSR)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_OSR, temp | 0x40)

    def reset(self):
        temp = self._i2c_bus.read_byte(AS7331_ADDRESS, AS7331_OSR)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_OSR, temp | 0x08)

    def set_configuration_mode(self):
        temp = self._i2c_bus.read_byte(AS7331_ADDRESS, AS7331_OSR)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_OSR, temp | 0x02)

    def set_measurement_mode(self):
        temp = self._i2c_bus.read_byte(AS7331_ADDRESS, AS7331_OSR)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_OSR, temp | 0x83)

    def init(self, mmode, cclk, sb, break_time, gain, time):
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_CREG1, (gain << 4) | time)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_CREG3, (mmode << 6) | (sb << 4) | cclk)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_BREAK, break_time)

    def one_shot(self):
        temp = self._i2c_bus.read_byte(AS7331_ADDRESS, AS7331_OSR)
        self._i2c_bus.write_byte(AS7331_ADDRESS, AS7331_OSR, temp | 0x80)

    def get_status(self):
        raw_data = self._i2c_bus.read_i2c_block_data(AS7331_ADDRESS, AS7331_STATUS, 2)
        return (raw_data[0] << 8) | raw_data[1]

    def read_temp_data(self):
        raw_data = self._i2c_bus.read_i2c_block_data(AS7331_ADDRESS, AS7331_TEMP, 2)
        return (raw_data[1] << 8) | raw_data[0]

    def read_uva_data(self):
        raw_data = self._i2c_bus.read_i2c_block_data(AS7331_ADDRESS, AS7331_MRES1, 2)
        return (raw_data[1] << 8) | raw_data[0]

    def read_uvb_data(self):
        raw_data = self._i2c_bus.read_i2c_block_data(AS7331_ADDRESS, AS7331_MRES2, 2)
        return (raw_data[1] << 8) | raw_data[0]

    def read_uvc_data(self):
        raw_data = self._i2c_bus.read_i2c_block_data(AS7331_ADDRESS, AS7331_MRES3, 2)
        return (raw_data[1] << 8) | raw_data[0]

    def read_all_data(self):
        raw_data = self._i2c_bus.read_i2c_block_data(AS7331_ADDRESS, AS7331_TEMP, 8)
        return [
            (raw_data[1] << 8) | raw_data[0],
            (raw_data[3] << 8) | raw_data[2],
            (raw_data[5] << 8) | raw_data[4],
            (raw_data[7] << 8) | raw_data[6]
        ]

# Usage example:
# Replace 'AS7331_ADDRESS' with the actual address of your device
AS7331_ADDRESS = 0x00  # Replace with the correct address
i2c_bus = ...  # Replace with your Raspberry Pi I2C library initialization
as7331_sensor = AS7331(i2c_bus)

# Example usage:
chip_id = as7331_sensor.get_chip_id()
print(f"Chip ID: {chip_id}")

# Continue with other sensor functions as needed.
