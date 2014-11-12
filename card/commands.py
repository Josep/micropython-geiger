import pyb
import fram_t
import tapunte
import fram

class commands():
    def __init__(self, rtc, fram, frt):
        self.frt = frt
        self.rtc = rtc
        self.fram = fram

    def getIndApunte(self):
        print('DEADBEEF01',end='')
        print(self.frt.indApunte)

    def getDateTime(self):
        dt = self.rtc.datetime()
        print('%02d'%(dt[0]%100),end='')
        print('%02d'%(dt[1]),end='')
        print('%02d'%(dt[2]),end='')
        print('%02d'%(dt[3]),end=' ')
        print('%02d'%(dt[4]),end='')
        print('%02d'%(dt[5]),end='')
        print('%02d'%(dt[6]),end='')
        print('%02d'%(0))

    def printApunte(self, i):
        apu = tapunte.tapunte()
        self.fram.framRead(apu.buff, i * self.frt.TAPUNTE_SIZE)
        print('DEADBEEF02', end='')
        print('%08X'%(apu.d), end=' ')
        print('%08X'%(apu.t), end=' ')
        print('%08X'%(apu.am2302), end=' ')
        print('%04X'%(apu.maxcpm), end='')
        print('%04X'%(apu.mincpm), end=' ')
        print('%04X'%(apu.cpm))

    def resetIndApunte(self):
        self.frt.resetIndApunte()
