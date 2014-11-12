import pyb
import fram_t

class am2302():
    def __init__(self, ch2, frt):
        self.frt = frt
        #canal pitido
        self.ch2 = ch2
        #Y12 as output
        self.oneWire = pyb.Pin('Y12', pyb.Pin.OUT_PP)
        self.oneWire.high()

    def getTempHum(self, buzz=True):
        id_bit = 0 # identificador del bit que estamos tratando
        vbit = 0  # valor de la palabra de 40 bits que se lee, incluye checksum
        self.oneWire.init(pyb.Pin.OUT_PP)
        self.oneWire.high()
        retardo=250
        if buzz:
            #suena buzzer
            self.ch2.pulse_width(12000)
            pyb.delay(80) #in msecs
            self.ch2.pulse_width(0)
            retardo=170
        #pull the pin high and wait 250 milliseconds (ya esta en high, esperamos 250ms de todos modos)
        pyb.delay(retardo)
        #Host pulls low 1.5 ms
        start = pyb.micros()
        self.oneWire.low()
        pyb.udelay(1500)
        #Host pulls up 30us
        self.oneWire.high()
        pyb.udelay(30)
        #Paso a INPUT
        self.oneWire.init(pyb.Pin.IN)
        #sensor pulls low 80us
        while self.oneWire.value() != 0:
            pass
        #sensor pulls up 80us
        while self.oneWire.value() != 1:
            pass
        #sensor pulls low 50us // start bit
        while self.oneWire.value() != 0:
            pass
        while(True):
            #bit starts
            while self.oneWire.value() != 1:
                pass
            start = pyb.micros()
            #bit ends
            while self.oneWire.value() != 0:
                pass
            if (pyb.micros()-start) > 50:
                vbit = (vbit << 1) | 0x1 
            else:
                vbit = (vbit << 1)
            id_bit = id_bit + 1
            if id_bit >= 40:
                check_rec = vbit & 0xff   # checksum recibido
                vbit = vbit >> 8  #aqui "vbit" contiene el valor medido (32 bits)
                check_cal = (vbit & 0xff) + ((vbit >> 8) & 0xff) + ((vbit >> 16) & 0xff) + ((vbit >> 24) & 0xff) # checksum calculado 
                if check_cal != check_rec:
                    self.frt.setAlarmBit(2)
                break
        return vbit
