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

Quellen:

https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html

https://tutorials-raspberrypi.de/rotation-und-beschleunigung-mit-dem-raspberry-pi-messen/