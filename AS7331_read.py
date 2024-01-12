import smbus2
import time

# I2C address of the AS7331 sensor
AS7331_I2C_ADDR = 0x49

# I2C bus (1 for Raspberry Pi 3, 0 for Raspberry Pi 2)
bus = smbus2.SMBus(1)

def read_sensor_data():
    # Read data from the sensor's registers using appropriate I2C commands
    # Implement the I2C communication protocol as per the sensor's datasheet

    # Example: Read data from register 0x00
    data = bus.read_byte_data(AS7331_I2C_ADDR, 0x00)

    return data

if __name__ == "__main__":
    try:
        while True:
            # Read sensor data
            sensor_data = read_sensor_data()

            # Print or process the sensor data as needed
            print("Sensor Data:", sensor_data)

            # Wait for some time before the next reading
            time.sleep(1)

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to exit the loop gracefully
        pass
    finally:
        # Close the I2C bus when done
        bus.close()
