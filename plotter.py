from sys import byteorder
import serial
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


serialPort = serial.Serial(port = "COM3",baudrate=115200, timeout=None) #bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
serialString = ""                           # Used to hold data coming over UART

xdim = 160
ydim = 120

bytesPerFrame = xdim * ydim * 2

def drawImage(buff):
    arr = np.frombuffer(buff,dtype=np.uint16).astype(np.uint32)
    arr = 0xFF000000 + ((arr & 0xF800) >> 8) + ((arr & 0x07E0) << 5) + ((arr & 0x001F) << 19)

    return Image.frombuffer('RGBA', (xdim, ydim), arr, 'raw','RGBA', 0, 1)

plt.ion()

while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 1):
        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.read_until(b'End', size=bytesPerFrame)
        serialString = serialString[:-3]
        serialString = int.from_bytes(serialString, byteorder='little').to_bytes(bytesPerFrame, byteorder='big')
        #print(serialString)

        # Print the contents of the serial data
        #print(serialString)
        im = drawImage(serialString)
        plt.imshow(im)
        plt.show()
        plt.pause(0.0001)
        plt.clf()
        #im.show()
        serialPort.reset_input_buffer()

        