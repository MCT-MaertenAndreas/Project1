from RPi import GPIO as io

class BasicIODevice():
    def __init__(self, gpio_pin, input_output=io.OUT, pull_up_down=io.PUD_DOWN, initial=io.LOW):
        self.gpio_pin = gpio_pin
        self.input_output = input_output

        if input_output == io.OUT:
            io.setup(gpio_pin, input_output, initial=initial)
        else:
            io.setup(gpio_pin, input_output, pull_up_down)

    @property
    def value(self):
        if self.input_output == io.OUT:
            raise Error('BasicIODevice was initiated as an output device, you can\'t read the value!')

        return io.input(self.gpio_pin)

    def disable(self):
        self.set(io.LOW)

    def enable(self):
        self.set(io.HIGH)

    def set(self, toggle):
        if toggle != io.HIGH and toggle != io.LOW:
            raise ValueError('Set method can only use HIGH or LOW as toggle value!')

        io.output(self.gpio_pin, toggle)
