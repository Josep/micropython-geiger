====================================
Geiger counter with micropython card
====================================

Hardware Design
===============

Geiger tube SBM-20: http://www.gstube.com/data/2398/

Pyboard: http://micropython.org

High voltage generator from http://www.mare.ee/indrek/geiger/

Digitization of tube discharges from http://www.techlib.com/science/geiger.html (with one gate of 4093 and 3.3V supply)

Power supply from http://1wt.eu/articles/alix-ups and http://www.mouser.com/ds/2/268/22008a-53656.pdf

Wireless serial port with wixel: http://www.pololu.com/docs/0J46/all

Log device: fram http://www.cypress.com/?docID=50514

Temp & humidity sensor am2302: https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf

Buzzer: ZX-27T6A1 at http://dx.com

Micropython card pins used:
::

    Y12    IN/OUT AM2302
    Y10    IN     TIM2_CH4  GEIGER
    Y2     IN Rx	POLOLOU
    Y11    OUT	  Power POLOLOU
    GND    GND
    VDD    VDD    3.3V
    Y3     OUT    SCK FRAM
    Y4     OUT    CS  FRAM
    Y5     OUT    SI  FRAM
    Y6     IN     SO  FRAM
    Y8     OUT    BUZZER
    Y9     OUT    RELAY
    Y1     OUT Tx POLOLOU
    X3     FREE   For testing
    X4     FREE   For testing
    X5     FREE   For testing

.. image:: DAN_6872.png
    :alt: photo of mounted proto board here

Software Design
===============

Buzzer is activated with programming PWM signal at 3.5Khz.
AM2302 is one wire, Pin has to be changed from output to input.
fram has an SPI interface. It is harcoded in python as individual pins.
The core is the interrupt handler awaken by the discharges of the tube:

::

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

