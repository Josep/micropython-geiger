import pyb

def test1():
    x3 = pyb.Pin('X3',pyb.Pin.OUT_PP)
    while True:
      x3.high()
      x3.low()

def test2():
    x3 = pyb.Pin('X3',pyb.Pin.OUT_PP)
    x4 = pyb.Pin('X4',pyb.Pin.OUT_PP)
    while True:
      x3.high()
      x3.low()
      x3.high()
      x4.init(pyb.Pin.IN)
      x3.low()

x5 = pyb.Pin('X5',pyb.Pin.OUT_PP)
def ic_cb(tim):
    x5.high()
    x5.low()

def test3():
    tim2 = pyb.Timer(2, freq=14000)
    ch3 = tim2.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3, pulse_width=3000)
    tim5 = pyb.Timer(5, prescaler=1,period=8) #10.5MHz
    ic = tim5.channel(4, pyb.Timer.IC, pin = pyb.Pin.board.X4,
            polarity=pyb.Timer.FALLING)
    ic.callback(ic_cb)
