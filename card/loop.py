import pyb
import geiger
import tapunte
import fram_t
import sys
from pyb import UART

class loop():
    def __init__(self, geigerPower, am2302, fram, frt, ch2, uart, apwix):
        self.geigerPower = geigerPower
        self.am2302 = am2302
        self.fram = fram
        self.frt = frt
        self.ch2 = ch2
        self.uart = uart
        self.apwix = apwix

    def humidityMode(self):
        self.geigerPower.high()
        while(True):
            pyb.delay(20000)
            print('%08X'%(self.am2302.getTempHum()))

    def geigerTransmissionModeGuay(self):
        self.geigerPower.low()
        geiger.start()
        geiger.count1m = 0
        while True:
            if geiger.count1m != 0:
                geiger.count1m = 0
                print('*')

    def geigerTransmissionMode(self):
        pyb.repl_uart(None)
        #self.uart.deinit()
        #self.uart = UART(6,9600)
        #self.uart.init(9600,bits=8,stop=1,parity=None)
        self.geigerPower.low()
        geiger.start()
        geiger.count1m = 0
        while True:
            if geiger.count1m != 0:
                geiger.count1m = 0
                self.uart.send('*')
                self.uart.send('\n')

    def geigerMode(self):
        self.geigerPower.low()
        geiger.start()
        geiger.count1m = 0
        while True:
            if geiger.count1m != 0:
                geiger.count1m = 0
                #suena buzzer
                self.ch2.pulse_width(12000)
                pyb.delay(80) #in msecs
                self.ch2.pulse_width(0)
            else:
                pyb.delay(50)

    def loop(self):
        self.geigerPower.low()
        geiger.start()
        rtc = pyb.RTC()
        ap1m = tapunte.tapunte()
        t15 = 0 #contador de 15 minutos
        #esperamos segs = 0
        datetime = rtc.datetime()
        while datetime[6] != 0:
            datetime = rtc.datetime()
        lm = datetime[5]
        pyb.disable_irq()
        geiger.count1m = 0
        geiger.count15m = 0
        pyb.enable_irq()
        while True:
            datetime = rtc.datetime()
            if datetime[5] == lm:
                pyb.delay(50)
                self.apwix.apw()
            else:
                lm = datetime[5]
                t15 = t15 + 1
                is15 = t15 == 15
                pyb.disable_irq()
                count1m_copy = geiger.count1m
                count15m_copy = geiger.count15m
                geiger.count1m = 0
                if is15:
                    geiger.count15m = 0
                pyb.enable_irq()
                cpm = count1m_copy
                if cpm > ap1m.maxcpm:
                    ap1m.maxcpm = cpm
                if cpm < ap1m.mincpm:
                    ap1m.mincpm = cpm
                if is15:
                    ap1m.cpm = count15m_copy//15
                    ap1m.d = int('0x%02d%02d%02d%02d'%(datetime[0]%100, datetime[1], datetime[2], datetime[3]),16)
                    ap1m.t = int('0x%02d%02d%02d%02d'%(datetime[4], datetime[5], datetime[6], 0), 16)
                    ap1m.am2302 = self.am2302.getTempHum()
                    self.fram.framWrite(self.frt.indApunte * tapunte.TAPUNTE_SIZE, ap1m.buff)
                    self.frt.incrIndApunte()
                    t15 = 0
                    ap1m.maxcpm = 0
                    ap1m.mincpm = 65535
