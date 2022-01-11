# Embedded Devices "Anzeige und Analyse von Sensordaten"

192.168.137.10

1. Überprüfen, ob auf der SD-Karte das SSH file vorhanden ist
2. An den RaspberryPi die SD-Karte und das Ethernet Kabel vom Computer anstecken
3. Den RaspberryPi mit Strom versorgen
4. In den Properties des Ethernetadapters beim Internetprotokoll Version 4 die IP-Adresse auf 192.168.137.1 und den DNS server auf 8.8.8.8 ändern.
5. In den Properties des Wifi-Adapters die Option "Allow other network users to connect" aktivieren
6. Bei "Home networking connection" den Ethernet Adapter auswählen
7. Mit Putty über den namen Hostnamen raspberrypi.local verbinden
8. Mit ``sudo raspi-config`` i2c aktivieren
9. Wenn noch nicht vorhanden die Zeilen

```
i2c-bcm2708
i2c-dev
```

 zu ``/etc/module`` hinzufügen und dann den RaspberryPi neustarten

8. Die Packages ``i2c-tools python-smbus`` installieren
9. Mit dem Befehl ``sudo i2cdetect -y 1`` die Hex-Adresse des Gyroskops herausfinden

```
pi@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

10. Um den Sensor auf Adresse 68 anzusprechen muss der folgende Befehl eingegeben werden ``sudo i2cget -y 1 0x68 0x75``
11. Als nächstes habe ich ein Pythonfile erstellt und folgenden Code hinein geschrieben

```
\#!/usr/bin/python


import smbus

import math

 

\# Register

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

​    return -((65535 - val) + 1)

  else:

​    return val

 

def dist(a,b):

  return math.sqrt((a*a)+(b*b))

 

def get_y_rotation(x,y,z):

  radians = math.atan2(x, dist(y,z))

  return -math.degrees(radians)

 

def get_x_rotation(x,y,z):

  radians = math.atan2(y, dist(x,z))

  return math.degrees(radians)

 

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1

address = 0x68    # via i2cdetect

 

\# Aktivieren, um das Modul ansprechen zu koennen

bus.write_byte_data(address, power_mgmt_1, 0)

 

print "Gyroskop"

print "--------"

 

gyroskop_xout = read_word_2c(0x43)

gyroskop_yout = read_word_2c(0x45)

gyroskop_zout = read_word_2c(0x47)

 

print "gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131)

print "gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131)

print "gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131)

 

print

print "Beschleunigungssensor"

print "---------------------"

 

beschleunigung_xout = read_word_2c(0x3b)

beschleunigung_yout = read_word_2c(0x3d)

beschleunigung_zout = read_word_2c(0x3f)

 

beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0

beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0

beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0

 

print "beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skaliert

print "beschleunigung_yout: ", ("%6d" % beschleunigung_yout), " skaliert: ", beschleunigung_yout_skaliert

print "beschleunigung_zout: ", ("%6d" % beschleunigung_zout), " skaliert: ", beschleunigung_zout_skaliert

 

print "X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)

print "Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
```

Quellen:

https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html

https://tutorials-raspberrypi.de/rotation-und-beschleunigung-mit-dem-raspberry-pi-messen/