import mraa
import time
import socket,sys

trig = mraa.Gpio(9)
echo = mraa.Gpio(8)

trig.dir(mraa.DIR_OUT)
echo.dir(mraa.DIR_IN)

sock = socket.socket()

def distance(measure='cm'):
    trig.write(0)
    time.sleep(0.002)

    trig.write(1)
    time.sleep(0.00001)
    trig.write(0)

    sig = None
    nosig = None
    et = None


    while echo.read() == 0:
            nosig = time.time()

    while echo.read() == 1:
            sig = time.time()

    if sig == None or nosig == None:
        return 0

    # et = Elapsed Time
    et = sig - nosig

    if measure == 'cm':
        distance =  et * 17150
    elif measure == 'in':
        distance = et / 0.000148
    else:
        print('Improper choice of measurement!!')
        distance = None
    return distance

# Replace IP with your server IP
sock.connect(('192.168.1.209',int(sys.argv[1])))

while True:
    data = sock.recv(1)

    t1 = time.time()
    x = distance('cm')
    print x
    if x < 30:
        sock.send('1')
        time.sleep(1)
    else:
        sock.send('0')

sock.close()
