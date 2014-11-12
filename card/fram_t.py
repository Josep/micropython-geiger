import tapunte


class fram_t():
    TAPUNTE_SIZE = 18
    N_APUNTES = 14300
    MARCA_FLASH = 0x9adee12d
    buff = bytearray(b'\x00'*4)
    def ulong2byte(self, u):
        self.buff[3] = (u >> 24) & 0xff
        self.buff[2] = (u >> 16) & 0xff
        self.buff[1] = (u >> 8) & 0xff
        self.buff[0] = u & 0xff
    def byte2ulong(self):
        return (self.buff[3] << 24) + (self.buff[2] << 16) + (self.buff[1] << 8) + self.buff[0]
    def set_alarm(self, alarm):
        self.ulong2byte(alarm)
        self.fr.framWrite(self.posAlarm,self.buff) 
    def set_indApunte(self, indApunte):
        self.ulong2byte(indApunte)
        self.fr.framWrite(self.posIndApunte,self.buff) 
    def set_serialNumber(self, serialNumber):
        self.ulong2byte(serialNumber)
        self.fr.framWrite(self.posSerialNumber,self.buff) 
    def set_marcaFlash(self, marcaFlash):
        self.ulong2byte(marcaFlash)
        self.fr.framWrite(self.posMarcaFlash, self.buff)
    def get_alarm(self):
        self.fr.framRead(self.buff, self.posAlarm)
        return self.byte2ulong()
    def get_indApunte(self):
        self.fr.framRead(self.buff, self.posIndApunte)
        return self.byte2ulong()
    def get_serialNumber(self):
        self.fr.framRead(self.buff, self.posSerialNumber)
        return self.byte2ulong()
    def get_marcaFlash(self):
        self.fr.framRead(self.buff, self.posMarcaFlash)
        return self.byte2ulong()
    def resetIndApunte(self):
        self.indApunteLocal = 0
        self.set_indApunte(0)
        self.set_alarm(0)
    def prepare_ar(self):
        key = self.get_marcaFlash()
        if key != self.MARCA_FLASH:
            self.resetIndApunte()
            key = self.MARCA_FLASH
            self.set_marcaFlash(key)
        self.indApunteLocal = self.get_indApunte()
        self.apu = tapunte.tapunte()
        self.fr.framRead(self.apu.buff, self.indApunteLocal * self.TAPUNTE_SIZE)
    def setAlarmBit(self, b):
        alarmtmp = self.get_alarm()
        alarmtmp = alarmtmp | (1 << b)
        self.set_alarm(alarmtmp)
    def incrIndApunte(self):
        self.indApunteLocal = self.indApunteLocal + 1
        if self.indApunteLocal >= self.N_APUNTES:
            self.indApunteLocal = 0
            setAlarmBit(0);
        self.set_indApunte(self.indApunteLocal)
        self.fr.framRead(self.apu.buff, self.indApunteLocal * self.TAPUNTE_SIZE)
    def __init__(self, fr):
        self.fr = fr
        self.posAlarm = self.TAPUNTE_SIZE * self.N_APUNTES
        self.posIndApunte = self.posAlarm + 4
        self.posSerialNumber = self.posIndApunte + 4
        self.posMarcaFlash = self.posSerialNumber + 4
        self.prepare_ar()
    alarm = property(get_alarm, set_alarm)
    indApunte = property(get_indApunte, set_indApunte)
    serialNumber = property(get_serialNumber, set_serialNumber)
    marcaFlash = property(get_marcaFlash, set_marcaFlash)
