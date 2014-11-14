Micro Python v1.3.3-94-gc92672d on 2014-10-18; PYBv1.0 with STM32F405RG

===============
Lessons learned
===============

* Code in interrupts is very limited: no memory alloc permited
* We do not have threads but we have timers and interrupts. Hardware has 17 timers.
* I had problems with struct pack/unpack so I made the functions myself for 8 bytes datatype
* It is difficult to avoid a main loop in my programs => when I have a main loop I do not have the REPL.
* Fortunately, ^C works everywere to interrut the main loop even from the UART.
* The Pin handling in python is really easy, good work!

==========
Real time?
==========

Switching a PIN
===============

::

    import pyb
    x3 = pyb.Pin('X3',pyb.Pin.OUT_PP)
    while True:
      x3.high()
      x3.low()

results: 14.5 us period, 68.97Khz. 7us in high state, 7.5us in low state. 7us for changing the value of a pin.

Output to input change
======================

::

    import pyb
    x3 = pyb.Pin('X3',pyb.Pin.OUT_PP)
    x4 = pyb.Pin('X4',pyb.Pin.OUT_PP)
    while True:
      x3.high()
      x3.low()
      x3.high()
      x4.init(pyb.Pin.IN)
      x3.low()

results: 30.8 us in high => 23.8 us for changing output to input

Interrupt latency
=================

x3 generates PWM of 14Khz, x4 is input capture of this signal. x5 is high on interrupt.

::

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

results: from falling edge on x3 to high level on x5: 12us => 12-7=5us from hw to sw
