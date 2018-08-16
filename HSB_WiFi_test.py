import sys
import time
from SerialTxRx import *
from WiFiPacketHandler import *


def main2():
    cmdRec = []
    ser = SerialTxRx(25, 57600)     #Open the serial port
    wifiPktHndlr = WiFiPacketHandler()  # Instantiate the wifi packet handler module to communicate with wifi module

    while True:
        charRec = ser.serRead(1)    # read the character received
        #charRec = ['18', 'E7', '41', '54', '2B', '4E', '5E', '54']
        if charRec:
            if charRec == '\n':
                cmdRec = []         # clear the buffer to store the command
            else:
                cmdRec.append('{:02X}'.format(ord(charRec)))

            #cmdRec.append(str(charRec))      # form the command that we rec
            print cmdRec
            resp = wifiPktHndlr.CmdRec(cmdRec) #get the response for the command received
            if resp:
                print resp

        #wifiPktHndlr.CmdSend(resp) #send the reply back to the controller

def main():
    cmdRec = []
    wifiPkt = WiFiPacketHandler()
    charRec = ['18', 'E7', '41', '54', '2B', '4E', '5E', '54']

    for char in range(len(charRec)):
        cmdRec.append(charRec[char])

    resp = wifiPkt.CmdRec(cmdRec)
    print resp


if __name__ == "__main__":
    main()
