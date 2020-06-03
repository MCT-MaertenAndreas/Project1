################ CODE DOOR OKLADNICOFF KILIAN 1MCT3 ###################

# import all modules
import spidev
from RPi import GPIO as io
from time import sleep
import os


class Mcp:

    def __init__(self, bus=0, device=0):
        self._spi = spidev.SpiDev()
        self.bus = bus
        self.device = device

    def setup(self):
        io.setmode(io.BOARD)
        self._spi.open(self._bus, self._device)
        self._spi.max_speed_hz = 1350000

    @staticmethod
    def convert_to_volt(value):
        return (value / 1023) * 3.3

    @staticmethod
    def convert_to_percent(value):
        return int((value / 1023) * 100)

    # methods for returning and checking the selected SPI bus

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, value):
        if isinstance(value, int) and value in range(0, 2):
            self._bus = value
        else:
            raise ValueError(
                "Error: given SPI bus is not valid")

    # methods for returning and checking the selected slave

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        if isinstance(value, int):
            self._device = value
        else:
            raise ValueError(
                "Error: given device channel is not valid")

    # methods for setting and returning the received bytes

    @property
    def bytes_in(self):
        return self._bytes_in

    @bytes_in.setter
    def bytes_in(self, list_bytes):
        if isinstance(list_bytes, list):
            self._bytes_in = list_bytes
        else:
            self._bytes_in = [0, 0, 0]
            print("Error: received bytes couldn't be loaded")

    # read the inputs on a defined channel and return the value in a range 0-1023
    def read_channel(self, ch):
        ch = ch << 4 | 0b10000000
        bytes_out = [0b00000001, ch, 0b00000000]
        self.bytes_in = self._spi.xfer2(bytes_out)
        return (self._bytes_in[1] << 8) | self._bytes_in[2]

    def closespi(self):
        self._spi.close()


def main():
    # setting up the spi slave connection
    spi = Mcp(0, 0)
    spi.setup()

    # initializing the generalized PWM pin
    pwm = 21
    io.setwarnings(False)
    io.setup(pwm, io.OUT)
    pwm = io.PWM(pwm, 50)
    pwm.start(0)

    try:
        while True:
            # reading the input value from the input bytes (range from 0-1023)
            value = spi.read_channel(0)

            # makes the console a bit more humanitary to look at
            os.system('clear')
            print('''\r
Voltage: {:.2f} V
Duty cycle: {:.2f} % '''.format(spi.convert_to_volt(value), spi.convert_to_percent(value), end=''))

            # pwm gets restarted everytime, changing the duty cycle
            pwm.ChangeDutyCycle(spi.convert_to_percent(value))

            # adding a small delay between reads
            sleep(0.1)
    except KeyboardInterrupt:  # if the error is a keyboardinterrupt it will not be printed in the console
        pass
    except Exception as e:  # all other raised errors will be displayed
        print(e)
    finally:
        # clean up everything
        os.system('clear')
        print('\rclosing connection with slave...')
        pwm.stop()
        spi.closespi()
        io.cleanup()


# if this file is executed directly it wil run the main() function
if __name__ == "__main__":
    main()
