from SerialTxRx import *
import CRCCalc

def genMsg(msg):
    msgList = []
    sync = 0x16
    msgLen = len(msg)
    msgLenHi = (msgLen >> 8) & 0xFF
    msgLenLo = (msgLen & 0xFF)

    msgId = 6169;       # trial purpose
    msgIdHi = (msgId >> 8) & 0xFF
    msgIdLo = (msgId & 0xFF)

    # convert the string into hex values
    for char in msg:
        msgList.append(ord(char))

    # convert the data into binary format of 8bits
    crcCal = [msgLenHi, msgLenLo, msgIdHi, msgIdLo,]
    crcCal = crcCal + msgList

    # The function getCRC accepts a list of binary data
    crcVal = CRCCalc.getCRC(crcCal)

    # the crcVal is returned in the form of hex string
    # convert the hex string number to decimal plain number
    crcVal = int(crcVal, 16)
    # convert the number to binary form in 8bits format
    crcValHi = (crcVal >> 8) & 0xFF
    crcValLo = crcVal & 0xFF

    #print crcCal
    # print crcVal

    cmdGen = []
    cmdGen.append(sync)
    cmdGen = cmdGen + crcCal
    cmdGen.append(crcValHi)
    cmdGen.append(crcValLo)

    # print cmdGen
    return cmdGen

def sendCmd(ser, txCmd):
    respStr = ''
    spclStr = ''
    ser.serWrite(txCmd)
    response = ser.serRead(512)
    print (response)    # print special characters in the response

def main():
    # init the serial port
    ser = SerialTxRx(4, 57600)

    # command to be sent
    sendCmd(ser, genMsg('AT+GENVER=?'))
    sendCmd(ser, genMsg('AT+NSTAT=?'))
    sendCmd(ser, genMsg('AT+WSTATUS'))
    

if __name__ == "__main__":
    main()
