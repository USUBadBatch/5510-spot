import serial
import sys
import glob
import os

PORT = "/dev/ttyACM0"
BAUDRATE = 557600

serial_con = serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=0.001)


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
print(serial_ports())
while True:
    data = serial_con.read(1)
    data += serial_con.read(serial_con.inWaiting())
    sys.stdout.write(str(data, encoding="UTF-8"))
    sys.stdout.flush()


