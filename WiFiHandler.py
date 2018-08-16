

""" Read the data from the serial port check if the data is valid and respond to it
"""
import sys
import time


class WiFiHandler(object):
    """ This class will handle the message that the controller sends to it and
        will respond to them.
    """
    ATCmdDict = {
                 'AT'   : '0',
                 'ATV0' : '0',
                 'ATE0' : '0',
                 'AT+WRXACTIVE=1' : '0'}

    def __init__(self):
        pass

    def Command(self, cmdRec):
        if cmdRec in self.ATCmdDict:
            #cmdPacketizing(ATCmdDict[cmdReq])
            ret = self.ATCmdDict[cmdRec]
            return ret
            #return self.ATCmdDic[cmdRec]
        else:
            #print self.ATCmdDict['AT']
            print "No command found by that name"
            return 0            # No command found


if __name__ == "__main__":
    wifi = WiFiHandler()
    ret = wifi.Command('AT')
    print ret
