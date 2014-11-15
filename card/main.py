# main.py -- put your code here!
import pyb
import fram
import fram_t
import loop
import am2302
import commands
import apw

from pyb import UART

#programamos pines
wixel = pyb.Pin('Y11',pyb.Pin.OUT_PP)
wixel.low() #turn on
geigerPower = pyb.Pin('Y9', pyb.Pin.OUT_PP) #relay for power geiger
geigerPower.high()  #turn off
geigerIn = pyb.Pin('Y10', pyb.Pin.IN)

#pitido inicial en salida Y8
tim12 = pyb.Timer(12, freq=3500)
ch2=tim12.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.Y8, pulse_width=12000)
pyb.delay(100) #in msecs
ch2.pulse_width(0)

#uart6 a wixel, pins Y1 y Y2
uart = UART(6,9600)
uart.init(9600,bits=8,stop=1,parity=None)
pyb.repl_uart(uart)

#initalize fram
fr = fram.fram()
frt = fram_t.fram_t(fr)

#rtc
rtc = pyb.RTC()

#initialize am2302
a = am2302.am2302(ch2, frt)

#initialize apagado periodico wixel
apwix = apw.apw(wixel,uart)

#initialize loop
l = loop.loop(geigerPower, a, fr, frt, ch2, uart, apwix)

#initialize commands
cms = commands.commands(rtc, fr, frt)
