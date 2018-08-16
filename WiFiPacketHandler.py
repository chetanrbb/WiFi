"""
init the serial port


while True:
    read the data from the serial port
    assemble the command rec
    send it to the wifi packet handler
          : here disassemble the wifi command from the Packet headers
          : check for the CRC rec
          : if OK then read the command and prepare the response
          : assemble the packet for the response and send it

"""
import sys
import time
from WiFiHandler import *
import CRCCalc

# Constants
SYNC_BYTES  = 1
LEN_BYTES   = 2
MSGID_BYTES = 2
CRC_BYTES   = 2

SYNC_OFFSET = 0
LEN_OFFSET  = 1
MSGID_OFFSET = 3
CMD_OFFSET = 5

PACKET_LEN = SYNC_BYTES + LEN_BYTES + MSGID_BYTES + CRC_BYTES


class WiFiPacketHandler(WiFiHandler):
    """ Handles the packetizing of the commands for the wifi module.
    """
    def __init__(self):
        WiFiHandler.__init__(self)
        self.msgId = 0


    def CmdRec(self, cmd):
        """ We got a command which is in packetized format.
            This function will extract the command from the packet.
        """
        cmdLen = len(cmd)
        #print 'Cmd ' + cmd

        if(cmdLen > PACKET_LEN):        # check if we got the cmd which has atleast the packet bytes
            print cmd
            ATcmd = []
            u_length = []
            u_msgid = [] 

            syncByte = cmd[SYNC_OFFSET]
            syncByte = int(syncByte, 16)          # takes the number string and typecasts it to int
            syncByte = format(syncByte, 'x')    # format the number in hex format without the '0x'

            length   = cmd[LEN_OFFSET: MSGID_OFFSET]        # list may have numbers in it\
            for char in range(len(length)):
                u_length.append(str(length[char]))
            length   = ''.join(u_length)      # join/merge the numbers in the length and not show them as individual elements
            length   = int(length, 16)
            length   = format(int(length), 'x')

            msgId    = cmd[MSGID_OFFSET: CMD_OFFSET]
            for char in range(len(msgId)):
                u_msgid.append(str(msgId[char]))
            msgId = ''.join(u_msgid)
            msgId = int(msgId, 16)
            msgId = format(int(msgId), 'x')

            cmdRec   = cmd[CMD_OFFSET: -1]      # CRC bytes are the last 2 bytes of the message
            for char in range(len(cmdRec)):
                ATcmd.append(str(unichr(cmdRec[char])))      # convert the int to ASCII character and append it in the list
            cmdRec = ''.join(ATcmd)  # the list shows the command characters as separate. So use ''.join to combine the char to form the command

            crcRec   = cmd[-1:]                 # Read the last 2 bytes of CRC
            crcRec   = ''.join(crcRec)
            crcRec   = int(crcRec, 16)          # takes the number string and typecasts it to int
            crcRec   = format(crcRec, 'x')      # takes the int and converts it to hex values, returns it in str form

            crcCal   = CRCCalc.getCRC(cmd[LEN_OFFSET: -1]) # calc the CRC of the message rec
            crcCal   = int(crcCal, 16)
            crcCal   = format(crcCal, 'x')

            if(crcCal == crcRec):
                resp = WiFiHandler.Command(self,cmdRec)
                print 'CmdSend: ' + cmdRec
                print 'Response: ' + resp
                #print 'Command Rec: ' + cmdRec + 'Resp: ' + resp
            else:
                print 'Command Invalid'

    def CmdSend(self, cmd):
        """ send the response of the command received
        """
        msgLen = len(cmd)
        self.msgId = self.msgId + 1
        cmdSend = []
        cmdSend2 = []
        cmdSend.append((msgLen >> 8) & 0xFF)        # convert int to string
        cmdSend.append((msgLen) & 0xFF)
        cmdSend.append((self.msgId >> 8) & 0xFF)
        cmdSend.append((self.msgId) & 0xFF)

        for chars in range(len(cmd)):
            cmdSend.append(ord(cmd[chars]))     # return the ASCII value of the char

        crcVal = CRCCalc.getCRC(cmdSend)        # get the CRC value for the entire command that is to be sent
        cmdSend.append(crcVal)

        cmdSend2.append(int(0x16))
        for char in range(len(cmdSend)):
            cmdSend2.append(cmdSend[char])

        return cmdSend2

if __name__ == "__main__":
    cmdStr = []
    wifi = WiFiPacketHandler()
    cmdSend = 'ATV0'
    cmdStr = wifi.CmdSend(cmdSend)

    wifi.CmdRec(cmdStr)
