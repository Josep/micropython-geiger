import serial
import sys
import threading
import time
from datetime import datetime
import copy

#portName = '/dev/cu.usbmodemfd122'
portName = '/dev/cu.usbmodemfa131'

exit = False
cmdrec = []

class read_th(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.buf=bytearray(b'\x00'*256)
        self.ind=0
        self.cmd=0
        self.leyendo=False

    def bufferize(self, car):
        cad='DEADBEEF'
        c = car.decode()
        if not self.leyendo:
            if self.ind < len(cad):
                for i,k in enumerate(cad):
                    if self.ind == i:
                        if c == k:
                            self.buf[i] = ord(c) & 0xff
                            self.ind = self.ind + 1
                        else:
                            self.ind = 0
                        break
            else:
                if self.ind == len(cad):
                    self.cmd = 10*int(c)
                    self.ind = self.ind + 1
                else:
                    if self.ind == len(cad)+1:
                        self.cmd = self.cmd+int(c)
                        self.ind = self.ind + 1
                        self.leyendo = True
                        self.ind = 0
                        for j in range(256):
                            self.buf[j] = 0
        else:
            if ord(c)==13:
                cmdrec.append(copy.copy(self.cmd))
                cmdrec.append(copy.copy(self.buf))
                self.ind = 0
                self.cmd = 0
                self.leyendo = False
                for j in range(256):
                    self.buf[j] = 0
            self.buf[self.ind] = ord(c) & 0xff
            self.ind = self.ind + 1

    def run(self):
        while not exit:
            c = self.port.read(1)
            print(c.decode(), end='')
            self.bufferize(c)


def send(cad,r=True):
    cad2 = cad
    if r:
        cad2 = cad2+'\r'
    for i in cad2:
        j = i.encode()
        port.write(j)
        time.sleep(0.015)

def setupDateTime():
    t = datetime.now()
    ts = t.strftime('%S')
    while True: #wait for change of second
        tn = datetime.now()
        tns = tn.strftime('%S')
        if tns != ts:
            break
    send(tn.strftime('rtc.datetime((%Y, %m, %d, %w, %H, %M, %S, 0))'))

def getIndApunte():
    indApunte = 0
    send('cms.getIndApunte()')
    count = 0
    while len(cmdrec) != 2:
        time.sleep(0.05)
        count = count + 1
        if count > 10:
            break
    if count < 10:
        indApunte=int(cmdrec[1][0:cmdrec[1].find(b'\x00')])
        cmdrec.clear()
    return indApunte

def getApunte(j):
    send('cms.printApunte(%d)'%(j))
    count = 0
    toReturn = ''
    while len(cmdrec) != 2:
        time.sleep(0.05)
        count = count + 1
        if count > 10:
            break
    if count < 10:
        toReturn=(cmdrec[1][0:cmdrec[1].find(b'\x00')]).decode()
        cmdrec.clear()
    return toReturn

def main(argv):
    if argv[0] == '-h':
        print("Usage: host.py [option]")
        print()
        print("Just one option at a time is processed")
        print("option is:")
        print(" -h     This help")
        print(" -d     Download measurements")
        print(" -t     Set date/time from host")
        print(" -l     Enter the loop")
        print(" -ew    Turn on wixel")
        print(" -aw    Turn off wixel")
        print(" -er    Turn on relay")
        print(" -ar    Turn off relay")
        print(" -eb    Turn on buzzer")
        print(" -ab    Turn off buzzer")
        print(" -eg    Turn on geiger mode")
        print(" -et    Turn on geiger transmission mode")
        print(" -hr    Soft reset")
        print(" -ph    Set humidity mode")
    if argv[0] == '-t':
        setupDateTime()
    if argv[0] == '-ew':    # enciende wixel
        send('wixel.low()')
    if argv[0] == '-aw':    # apaga wixel
        send('wixel.high()')
    if argv[0] == '-er':    # enciende relay geiger
        send('geiger.low()')
    if argv[0] == '-ar':    # apaga relay geiger
        send('geiger.high()')
    if argv[0] == '-eb':    # enciende buzzer
        send('ch2.pulse_width(12000)')
    if argv[0] == '-ab':    # apaga buzzer
        send('ch2.pulse_width(0)')
    if argv[0] == '-eg':    # enciende geiger mode
        send('l.geigerMode()')
    if argv[0] == '-et':    # enciende geiger transmission mode
        send('l.geigerTransmissionMode()')
        while(True):
            time.sleep(0.2)
    if argv[0] == '-hr':    # haz reset
        send('\x03', False) #^C
        send('\x04', False) #^D
    if argv[0] == '-ph': # pon humidity
        send('l.humidityMode()')
    if argv[0] == '-l': # enter the loop 
        send('l.loop()')
    if argv[0] == '-d': # download measures
        #get indApunte
        indApunte = getIndApunte()
        print('downloading %d registers...'%(indApunte))
        f = open('../result.txt','a')
        for j in range(indApunte):
            cad = getApunte(j)
            print(cad, file=f)
        f.close()
        #index to 0
        send('cms.resetIndApunte()')

def showStandard():
    send('')
    time.sleep(0.2)
    send('cms.getDateTime()')
    time.sleep(1)
    #getIndApunte
    indApunte = getIndApunte()
    print('indApunte =',indApunte)
    #getAlarm
    #print apunte ultimo
    if indApunte > 0:
        print(getApunte(indApunte-1))
    time.sleep(0.25)


if __name__ == "__main__":
    port = serial.Serial(portName, 9600, timeout=0.2)
    port.flushInput()
    rt = read_th(port)
    rt.start()
    time.sleep(0.2)
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        send('\x03') #^C
        showStandard()
    time.sleep(0.2)
    exit = True
    print()
    rt.join()
