import smbus2
import time

class I2Cdev:
    def __init__(self, i2c_bus):
        self._i2c_bus = i2c_bus

    def read_byte(self, address, sub_address):
        self._i2c_bus.write_byte(address, sub_address)
        time.sleep(0.1)  # Add a delay to ensure data is ready
        return self._i2c_bus.read_byte(address)

    def read_byte_16(self, dev_addr, reg_addr):
        self._i2c_bus.write_byte_data(dev_addr, (reg_addr >> 8) & 0xFF, reg_addr & 0xFF)
        time.sleep(0.1)  # Add a delay to ensure data is ready
        return self._i2c_bus.read_byte(dev_addr)

    def read_bytes(self, address, sub_address, count):
        self._i2c_bus.write_byte(address, sub_address)
        time.sleep(0.1)  # Add a delay to ensure data is ready
        return [self._i2c_bus.read_byte(address) for _ in range(count)]

    def read_bytes_16(self, dev_addr, reg_addr, count):
        self._i2c_bus.write_byte_data(dev_addr, (reg_addr >> 8) & 0xFF, reg_addr & 0xFF)
        time.sleep(0.1)  # Add a delay to ensure data is ready
        return [self._i2c_bus.read_byte(dev_addr) for _ in range(count)]

    def write_byte(self, dev_addr, reg_addr, data):
        self._i2c_bus.write_byte_data(dev_addr, reg_addr, data)

    def write_bytes(self, dev_addr, reg_addr, data):
        self._i2c_bus.write_i2c_block_data(dev_addr, reg_addr, data)

    def i2c_scan(self):
        print("Scanning...")
        n_devices = 0
        for address in range(1, 127):
            try:
                self._i2c_bus.read_byte(address)
                print(f"I2C device found at address 0x{address:02X} !")
                n_devices += 1
            except Exception as e:
                pass

        if n_devices == 0:
            print("No I2C devices found\n")
        else:
            print("I2C scan complete\n")


# Usage example:
# Replace 'i2c_bus_number' with the actual I2C bus number on your Raspberry Pi
i2c_bus_number = 1  # Replace with the correct bus number
i2c_dev = I2Cdev(smbus.SMBus(i2c_bus_number))

# Example usage:
i2c_dev.i2c_scan()
