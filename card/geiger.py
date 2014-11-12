import pyb
import micropython

count15m = 0
count1m = 0

# Interrupt service routine for input capture
def ic_cb(tim):
    global count1m
    global count15m
    #ic_measure = ic.capture()
    count15m = count15m + 1
    count1m = count1m + 1

def start():
    micropython.alloc_emergency_exception_buf(100)
    t2 = pyb.Timer(2,prescaler=1,period=8) #10.5MHz
    ic = t2.channel(4, pyb.Timer.IC, pin=pyb.Pin.board.Y10, polarity=pyb.Timer.FALLING)
    ic.callback(ic_cb)
