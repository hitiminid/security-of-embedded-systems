from time import sleep
import serial


class Communication:

    def __init__(self, port='/dev/ttyUSB0', baud_rate=9600, timeout=4):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.delay = 0.1 # Delay for one tenth of a second
        self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        sleep(5)


    def write(self, message):
        self.serial.write(message)
        sleep(self.delay)


    def read(self):
        return self.serial.read()

    def wait(self):
        sleep(self.delay)



communication = Communication()
communication.write(b'1')
sleep(.1)

while True:
    if communication.serial.in_waiting:
        print('dupa')
        break
    sleep(.1)
