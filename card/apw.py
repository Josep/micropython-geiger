import pyb

# Estado:
# 0 => inicio
# 1 => 59 minutos apagado
# 2 => segundos 0-10, 20-30, 40-50 con deadbeef sin mandar
# 3 => segundos 0-10, 20-30, 40-50 con deadbeef mandado
# 4 => segundos 10-20, 30-40, 50-60
# 5 => Sin apagado periodico
class apw():
    def __init__(self, wixel, uart):
        self.wixel = wixel
        self.uart = uart
        self.t1 = 0
        self.estado = 0
        self.listo = b'\xda\xda\xbe\xbe'
        self.statusApagadoPeriodicoWixel = False
        self.tmr = 0
        self.timer5 = pyb.Timer(5, prescaler=0xffff, period=0x3fffffff)
        self.fr = 84000000.0/float(0xffff+1)
        self.timer5.counter(0)
    def apw(self):
        t2 = self.timer5.counter()
        if t2 > 0x30000000:
            self.tmr = self.tmr + self.timer5.counter()
            self.timer5.counter(0)
            t2 = self.tmr
        else:
            t2 = t2 + self.tmr
        if self.estado == 0:
            if self.statusApagadoPeriodicoWixel:
                self.t1 = t2
                self.estado = 2
            else:
                self.estado = 5
            return
        if self.estado == 1:
            dif = t2 - self.t1
            self.wixel.high()
            if dif > (59*60*self.fr):
                self.t1 = t2
                self.stado = 2
            if not self.statusApagadoPeriodicoWixel:
                self.estado = 5
            return
        if self.estado == 2:
            self.wixel.low()
            self.uart.write(self.listo)
            self.estado = 3
            return
        if self.estado == 3:
            dif = t2 - self.t1
            if ((dif > (10*self.fr)) and (dif <= (20*self.fr))) or ((dif > (30*self.fr)) and (dif <= (40*self.fr))) or ((dif > (50*self.fr)) and (dif <= (60*self.fr))):
                self.estado = 4
            if not self.statusApagadoPeriodicoWixel:
                self.estado = 5
            return
        if self.estado == 4:
            dif = t2 - self.t1
            if ((dif > (20*self.fr)) and (dif <= (30*self.fr))) or ((dif > (40*self.fr)) and (dif <= (50*self.fr))):
                self.estado = 2
            else:
                if dif > (60*self.fr):
                    self.estado = 1
            return
        if self.estado == 5:
            self.wixel.low()
            if self.statusApagadoPeriodicoWixel:
                self.t1 = t2
                self.estado = 2
            return
