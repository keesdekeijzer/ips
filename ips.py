#!/usr/bin/env python3.10

# Gemaakt door Kees de Keijzer
# 2024-06-13
# ips is bedoeld om apparaten in een netwerk op te vragen met hun naam en hun ip adres
# ips gebruikt hiervoor de  opdracht arp

import subprocess


# hulpfunctie om het resultaat overzichtelijk te laten zien
def aanvullen(tekst, maxlengte):
    aanvul = ' ' * (maxlengte - len(tekst))
    nieuwe_tekst = tekst + aanvul + '\t'
    return nieuwe_tekst


# namen ophalen
p = subprocess.Popen("arp", stdout=subprocess.PIPE, shell=True)
(uitvoer, err) = p.communicate()
arp = uitvoer.decode('utf-8').splitlines()
namen = {}
for line in arp:
    if ':' in line:  # alleen regels waar een MAC-adres in staat
        regel = line.split()
        namen[regel[2]] = regel[0]

# ip-adressen ophalen
p = subprocess.Popen("arp -n", stdout=subprocess.PIPE, shell=True)
(uitvoer, err) = p.communicate()
arp_n = uitvoer.decode('utf-8').splitlines()
adressen = {}
for line in arp_n:
    if ':' in line:
        regel = line.split()
        adressen[regel[2]] = regel[0]

regels = []

for mac, naam in namen.items():
    nieuwe_regel = aanvullen(adressen[mac], 17) + aanvullen(naam, 40) + mac
    regels.append(nieuwe_regel)

regels.sort()  # sortering op ip-adressen is niet optimaal doordat de lengte kan verschillen

# kopregel toevoegen aan het begin
kopregel = aanvullen('IP-ADRES', 17) + aanvullen('NAAM APPARAAT', 40) + 'MAC-ADRES'
regels.insert(0, kopregel)

for regel in regels:
    print(regel)
