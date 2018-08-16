import sys
import serial

ser = serial.Serial()



#Serial port open and configuration
class SerialTxRx(object):
    def __init__(self, comPort, baudrate):
        """ Initializer for the serial port """
        print comPort, baudrate
        self.serPortInit(comPort, baudrate)


    def __del__(self):
        'Destructor to close the serial port if the program is terminated'
        self.serPortClose()

    def serRead(self, size):
        response = ser.read(size)
        return response

    def serPortClose(self):
        print 'Serial port closed'
        ser.close()

    def serPortInit(self, portNum, baudrate):
        ser.port = 'COM'+ str(portNum)
        ser.baudrate = baudrate
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        ser.timeout = 1         #block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        #ser.writeTimeout = 2
        try:
            ser.open()
            self.serFlush()
            print 'Serial port opened'

        except Exception, e:
            print  e
            exit()

    def serFlush(self):
        ser.flushInput()
        ser.flushOutput()

    def serWrite(self, data):
        if ser.isOpen():
            try:
                #serFlush()
                ser.write(data)
            except Exception, e:
                print "ERROR: Communicating..." + str(e)
        else:
            print 'Open the COM Port'



if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print 'Enter ComPort, Baudrate'
    else:
        comPort = sys.argv[1]
        baudrate = sys.argv[2]
        SerialTxRx(comPort, baudrate)
        
