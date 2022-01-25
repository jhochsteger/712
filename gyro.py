import io
import smbus
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import flask
from flask import Response, app, Flask, render_template
from random import randrange
# Code Origin (Data): https://tutorials-raspberrypi.de/rotation-und-beschleunigung-mit-dem-raspberry-pi-messen/
# Code Origin (Flask): https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
# Create figure for plotting

fig = plt.figure()
gyro = fig.add_subplot(1, 3, 1, projection='3d')
beschl = fig.add_subplot(1, 3, 3, projection='3d')
gx = []
gy = []
gz = []
bx = []
by = []
bz = []

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
    #TODO Exceptionhandling
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect

# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

# This function is called periodically from FuncAnimation
def animate(gx, gy, gz, bx, by, bz):


    # Add x and y to lists
    gx.append(read_word_2c(0x43))
    gy.append(read_word_2c(0x45))
    gz.append(read_word_2c(0x47))
    bx.append(read_word_2c(0x3b))
    by.append(read_word_2c(0x3d))
    bz.append(read_word_2c(0x3f))

    # Limit x and y lists to 20 items
    gx = gx[-10:]
    gy = gy[-10:]
    gz = gz[-10:]
    bx = bx[-10:]
    by = by[-10:]
    bz = bz[-10:]

    # Draw x and y lists
    gyro.clear()
    gyro.plot(gx, gy, gz)
    gyro.set_title('Gyroskop')
    gyro.set_xlabel('X-Rotation')
    gyro.set_ylabel('Y-Rotation')
    gyro.set_zlabel('Z-Rotation')
    gyro.set_xlim([-10000, 10000])
    gyro.set_ylim([-10000, 10000])
    gyro.set_zlim([-10000, 10000])

    beschl.clear()
    beschl.plot(bx, by, bz)
    beschl.set_title('Beschleunigung')
    beschl.set_xlabel('X-Beschleunigung')
    beschl.set_ylabel('Y-Beschleunigung')
    beschl.set_zlabel('Z-Beschleunigung')
    beschl.set_xlim([-10000, 10000])
    beschl.set_ylim([-10000, 10000])
    beschl.set_zlim([-10000, 10000])


app = Flask(__name__)

@app.route('/plot.png')
def plot_png():
    animate(gx, gy, gz, bx, by, bz)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/test')
def charTest():
    return render_template('./index.html')

if __name__ == '__main__':
   app.run(debug = False, host='0.0.0.0')
