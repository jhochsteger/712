import io
import smbus
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from flask import Response, app
from random import randrange

# Create figure for plotting
from matplotlib.backends.backend_template import FigureCanvas

fig = plt.figure()
gyro = fig.add_subplot(2, 1, 1, projection='3d')
beschl = fig.add_subplot(2, 1, 2, projection='3d')
gx = []
gy = []
gz = []
bx = []
by = []
bz = []

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
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
def animate(i, gx, gy, gz, bx, by, bz):


    # Add x and y to lists
    gx.append(read_word_2c(0x43))
    gy.append(read_word_2c(0x45))
    gz.append(read_word_2c(0x47))
    bx.append(read_word_2c(0x3b))
    by.append(read_word_2c(0x3d))
    bz.append(read_word_2c(0x3f))

    # Limit x and y lists to 20 items
    gx = gx[-20:]
    gy = gy[-20:]
    gz = gz[-20:]
    bx = bx[-20:]
    by = by[-20:]
    bz = bz[-20:]

    # Draw x and y lists
    gyro.clear()
    gyro.plot(gx, gy, gz)

    beschl.clear()
    beschl.plot(bx, by, bz)


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(gx, gy, gz, bx, by, bz), interval=1000)
plt.show()

@app.route('/plot.png')
def plot_png():
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
