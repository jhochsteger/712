# Embedded Devices "Anzeige und Analyse von Sensordaten"

192.168.137.10

1. An den RaspberryPi die SD-Karte und das Ethernet Kabel vom Computer anstecken
2. Den RaspberryPi mit Strom versorgen
3. In den Properties des Wifi-Adapters die Option "Allow other network users to connect" aktivieren
4. Bei "Home networking connection" den Ethernet Adapter auswählen
5. Mit Putty über den namen Hostnamen raspberrypi.local verbinden
6. Mit ``sudo raspi-config`` i2c aktivieren
7. Wenn noch nicht vorhanden die Zeilen

```
i2c-bcm2708
i2c-dev
```

​	hinzufügen und dann den RaspberryPi neustarten

8. die packages ``i2c-tools python-smbus`` installieren
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

Quellen:

https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html

https://tutorials-raspberrypi.de/rotation-und-beschleunigung-mit-dem-raspberry-pi-messen/