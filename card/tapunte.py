TAPUNTE_SIZE = 18

class tapunte():

    buff = bytearray(b'\x00'*TAPUNTE_SIZE)
    buf4 = bytearray(b'\x00'*4)
    buf2 = bytearray(b'\x00'*2)

    def ulong2byte(self, u):
        self.buf4[3] = (u >> 24) & 0xff
        self.buf4[2] = (u >> 16) & 0xff
        self.buf4[1] = (u >> 8) & 0xff
        self.buf4[0] = u & 0xff
    def word2byte(self, u):
        self.buf2[1] = (u >> 8) & 0xff
        self.buf2[0] = u & 0xff
    def byte2ulong(self):
        return (self.buf4[3] << 24) + (self.buf4[2] << 16) + (self.buf4[1] << 8) + self.buf4[0]
    def byte2word(self):
        return (self.buf2[1] << 8) + self.buf2[0]
    def set_d(self, d):
        self.ulong2byte(d)
        self.buff[0] = self.buf4[0]
        self.buff[1] = self.buf4[1]
        self.buff[2] = self.buf4[2]
        self.buff[3] = self.buf4[3]
    def set_t(self, t):
        self.ulong2byte(t)
        self.buff[4] = self.buf4[0]
        self.buff[5] = self.buf4[1]
        self.buff[6] = self.buf4[2]
        self.buff[7] = self.buf4[3]
    def set_am2302(self, am2302):
        self.ulong2byte(am2302)
        self.buff[8] = self.buf4[0]
        self.buff[9] = self.buf4[1]
        self.buff[10] = self.buf4[2]
        self.buff[11] = self.buf4[3]
    def set_maxcpm(self, maxcpm):
        self.word2byte(maxcpm)
        self.buff[12] = self.buf2[0]
        self.buff[13] = self.buf2[1]
    def set_mincpm(self, mincpm):
        self.word2byte(mincpm)
        self.buff[14] = self.buf2[0]
        self.buff[15] = self.buf2[1]
    def set_cpm(self, cpm):
        self.word2byte(cpm)
        self.buff[16] = self.buf2[0]
        self.buff[17] = self.buf2[1]
    def get_d(self):
        self.buf4[0] = self.buff[0]
        self.buf4[1] = self.buff[1]
        self.buf4[2] = self.buff[2]
        self.buf4[3] = self.buff[3]
        return self.byte2ulong()
    def get_t(self):
        self.buf4[0] = self.buff[4]
        self.buf4[1] = self.buff[5]
        self.buf4[2] = self.buff[6]
        self.buf4[3] = self.buff[7]
        return self.byte2ulong()
    def get_am2302(self):
        self.buf4[0] = self.buff[8]
        self.buf4[1] = self.buff[9]
        self.buf4[2] = self.buff[10]
        self.buf4[3] = self.buff[11]
        return self.byte2ulong()
    def get_maxcpm(self):
        self.buf2[0] = self.buff[12]
        self.buf2[1] = self.buff[13]
        return self.byte2word()
    def get_mincpm(self):
        self.buf2[0] = self.buff[14]
        self.buf2[1] = self.buff[15]
        return self.byte2word()
    def get_cpm(self):
        self.buf2[0] = self.buff[16]
        self.buf2[1] = self.buff[17]
        return self.byte2word()

    def __init__(self):
        self.d = 0xffffff
        self.t = 0xffffff
        self.am2302 = 0xffffffff
        self.maxcpm = 0
        self.mincpm = 0xffff
        self.cpm = 0xffff

    d = property(get_d , set_d)
    t = property(get_t, set_t)
    am2302 = property(get_am2302, set_am2302)
    maxcpm = property(get_maxcpm , set_maxcpm)
    mincpm = property(get_mincpm, set_mincpm)
    cpm = property(get_cpm, set_cpm)

if __name__ == "__main__":
        ap = tapunte()
        print(ap.buff)
        ap.am2302 = 0xdeadbeef
        print(hex(ap.am2302))
        print(ap.buff)

