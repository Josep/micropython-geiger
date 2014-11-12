import pyb

CPOL = 1
CPHA = 1
OPCODE_WREN  = 6
OPCODE_WRDI  = 4
OPCODE_RDSR  = 5
OPCODE_WRSR  = 1
OPCODE_READ  = 3
OPCODE_FSTRD = 11
OPCODE_WRITE = 2
OPCODE_SLEEP = 0xb9
OPCODE_RDID  = 0x9f

class fram():

    def __init__(self):
        #initialize fram pins Y3:Y6
        self.fram_sck = pyb.Pin('Y3', pyb.Pin.OUT_PP)
        self.fram_cs  = pyb.Pin('Y4', pyb.Pin.OUT_PP)
        self.fram_si  = pyb.Pin('Y5', pyb.Pin.OUT_PP)
        self.fram_so  = pyb.Pin('Y6', pyb.Pin.IN)
        #sck a 1
        self.fram_sck.high()
        #cs a 1
        self.fram_cs.high()
        #mosi a 0
        self.fram_si.low()
        #debuginfo
        r = self.RDSR()  #r should be 0x0040
        print('init fram: ', hex(r))

    def changeClock(self):
        val = self.fram_sck.value()
        if val == 0:
            self.fram_sck.high()
        else:
            self.fram_sck.low()

    def shiftOutN(self, value, n):
        toReturn = 0
        self.fram_cs.low()
        for i in range(n):
            if (value & (1 << (n - 1))) == 0:
                self.fram_si.low()
            else:
                self.fram_si.high()
            value = value << 1
            self.changeClock()
            if CPHA:
              self.changeClock()
              toReturn = (toReturn << 1) | self.fram_so.value()
            else:
              toReturn = (toReturn << 1) | self.fram_so.value()
              self.changeClock()
        self.fram_cs.high()
        return toReturn

    def WREN(self):
        self.shiftOutN(OPCODE_WREN,8)

    def WRDI(self):
        self.shiftOutN(OPCODE_WRDI,8)
    
    def RDSR(self):
        return self.shiftOutN(OPCODE_RDSR<<8,16) & 0xff
    
    def WRSR(self, s):
        self.shiftOutN((OPCODE_WRSR<<8)+s,16)
    
    def READ(self, addr):
        return self.shiftOutN(((OPCODE_READ)<<32)+((addr)<<8),40) & 0xff
    
    def FSTRD(self, addr):
        return self.shiftOutN((OPCODE_FSTRD<<40)+((addr)<<16),48) & 0xff
    
    def WRITE(self, addr,val):
        self.shiftOutN(((OPCODE_WRITE)<<32)+((addr)<<8)+val,40)
    
    def SLEEP(self):
        self.shiftOutN(OPCODE_SLEEP,8)
    
    def framWrite(self, destAddr, orig):
        size = len(orig)
        pdest = destAddr
        for i in range(size):
            self.WREN()
            self.WRITE(pdest,orig[i]&0xff)
            pdest = pdest+1
    
    def framRead(self, dest, origAddr):
        size = len(dest)
        porig = origAddr
        for i in range(size):
            dest[i] = self.READ(porig)
            porig = porig + 1
    
    def framSet(self, destAddr, val, size):
        pdest = destAddr
        for i in range(size):
            self.WREN()
            self.WRITE(pdest, val)
            pdest = pdest + 1
