"""
projekt3.py: třetí projekt do Engeto Online Python Akademie

author: Barbora Kočí
email: barbora.koci@email.cz
discord: barca6493
"""

from requests import get
from bs4 import BeautifulSoup as bs
import csv
import time
import asyncio
import httpx
import sys

def ziskej_odpoved_serveru(url):
    odpoved = get(url)
    return odpoved.text

def naparsuj_odpoved_na_tagy(obsah):
    return bs(obsah, features="html.parser")

def najdi_kody(polivka, tag):
    tabulky = ["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"]
    kody = []
    for tabulka in tabulky:
        kody.extend(polivka.find_all(tag, {"headers": tabulka}))
    return kody

def najdi_obce(polivka, tag):
    tabulky = ["t1sa1 t1sb2", "t2sa1 t2sb2", "t3sa1 t3sb2"]
    obce = []
    for tabulka in tabulky:
        obce.extend(polivka.find_all(tag, {"class": "overflow_name",
                                                 "headers":tabulka}))
    return obce

def najdi_vsechny_url():
    vsechny_url = []
    kody_obci = ['562980', '562998', '563005', '563013', '563021', '563048', '563056', '563064', '563072', '563081', '562971',
     '563099', '563102', '563111', '563129', '563137',
     '563315', '563161', '563188', '546518', '563200', '563218', '563226', '563242', '546160', '563269', '563277',
     '563285', '546062', '563293', '546071', '563323', '563331', '563340', '563358', '563382', '563404', '563412',
     '563439', '563463', '563471', '563480', '563498', '563501']
    for kod in kody_obci:
        vsechny_url.append(f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec={kod}&xvyber=4202")
    return vsechny_url

async def ziskej_odpovedi_serveru():
    vsechny_url = najdi_vsechny_url()
    odpovedi = []
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in vsechny_url]
        responses = await asyncio.gather(*tasks)
        odpovedi.extend(responses)
    return odpovedi

def ziskej_polivky():
    odpovedi = asyncio.run(ziskej_odpovedi_serveru())
    polivky = []
    for odpoved in odpovedi:
        polivky.append(naparsuj_odpoved_na_tagy(odpoved))
    return polivky

def najdi_vsechny_volice(tag):
    polivky = ziskej_polivky()
    vsichni_volici = []
    for polivka in polivky:
        vsichni_volici.append(polivka.find_all(tag, {"headers": "sa2"}))
    return vsichni_volici

def najdi_volice():
    vsichni_volici = najdi_vsechny_volice("td")
    volici = []
    for volic in vsichni_volici:
        volici.append([td.text.replace('\xa0', ' ') for td in volic])
    return volici

def najdi_vsechny_obalky(tag):
    polivky = ziskej_polivky()
    vsechny_obalky = []
    for polivka in polivky:
        vsechny_obalky.append(polivka.find_all(tag, {"headers": "sa3"}))
    return vsechny_obalky

def najdi_obalky():
    vsechny_obalky = najdi_vsechny_obalky("td")
    obalky = []
    for obalka in vsechny_obalky:
        obalky.append([td.text.replace('\xa0', ' ') for td in obalka])
    return obalky

def najdi_vsechny_hlasy(tag):
    polivky = ziskej_polivky()
    vsechny_hlasy = []
    for polivka in polivky:
        vsechny_hlasy.append(polivka.find_all(tag, {"headers": "sa6"}))
    return vsechny_hlasy

def najdi_hlasy():
    vsechny_hlasy = najdi_vsechny_hlasy("td")
    hlasy = []
    for hlas in vsechny_hlasy:
        hlasy.append([td.text.replace('\xa0', ' ') for td in hlas])
    return hlasy

def najdi_vsechny_strany(tag):
    polivky = ziskej_polivky()
    polivka = polivky[0]
    vsechny_strany = []
    tabulky = ["t1sa1 t1sb2", "t2sa1 t2sb2"]
    # for polivka[0] in polivky:
    for tabulka in tabulky:
        vsechny_strany.append(polivka.find_all(tag, {"class": "overflow_name",
                                                    "headers":tabulka}))
    return vsechny_strany

def najdi_strany():
    vsechny_strany = najdi_vsechny_strany("td")
    strany = []
    for strana in vsechny_strany:
        strany.append([td.text.replace('"', '') for td in strana])
    return strany

def najdi_vsechny_hlasy_pro_stranu(tag):
    polivky = ziskej_polivky()
    # polivka = polivky[0]
    vsechny_hps = []
    tabulky = ["t1sa2 t1sb3", "t2sa2 t2sb3"]
    for polivka in polivky:
        for tabulka in tabulky:
            vsechny_hps.append(polivka.find_all(tag, {"class": "cislo",
                                               "headers":tabulka}))
    return vsechny_hps

def najdi_hlasy_pro_stranu():
    vsechny_hps = najdi_vsechny_hlasy_pro_stranu("td")
    hps = []
    for hlasps in vsechny_hps:
        hps.append([td.text.replace('\xa0', ' ') for td in hlasps])
    return hps

if __name__ == "__main__":
    odpoved = ziskej_odpoved_serveru("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202")
    volby_polivka = naparsuj_odpoved_na_tagy(odpoved)
    vsechny_kody = najdi_kody(volby_polivka,"td")
    vsechny_obce = najdi_obce(volby_polivka, "td")
    kody_obci = [td.a.text for td in vsechny_kody if td.a]
    obce = [td.text for td in vsechny_obce if td]
    vsechny_url = najdi_vsechny_url()
    odpovedi = asyncio.run(ziskej_odpovedi_serveru())
    polivky = ziskej_polivky()
    volici = najdi_volice()
    obalky = najdi_obalky()
    hlasy = najdi_hlasy()
    strany_list = najdi_strany()
    hps = najdi_hlasy_pro_stranu()

    volici = [item for sublist in volici for item in sublist]
    obalky = [item for sublist in obalky for item in sublist]
    hlasy = [item for sublist in hlasy for item in sublist]
    strany_list = [item for sublist in strany_list for item in sublist]
    strany = ", ".join([str(item) for item in strany_list])
    # strany = stranyx.strip('"') # PROC NEFUNGUJE???
    hps = [item for sublist in hps for item in sublist]

    hlavicka = ["kód", "obec", "voliči", "obálky", "platné hlasy"]
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(hlavicka)

        for kod_val, obec_val, volici_val, obalky_val, hlasy_val in zip(kody_obci, obce, volici, obalky, hlasy):
            # for i in range(24):
                # for j in range(44):
            writer.writerow([kod_val, obec_val, volici_val, obalky_val, hlasy_val])

"""
SPOUSTENI S ARGUMENTY

jmeno = "Petr"
prijmeni = "Svetr"

if not jmeno or not prijmeni:
    print("Chybí jméno nebo příjmení")
    # jednička představuje obecně jakoukoliv chybu
    sys.exit(1)
else:
    print("Program pokračuje..")
    
    print(sys.argv[0]) # vypíše jméno spouštěného souboru
    
    print(sys.argv) # lze taky jako python prvni_argument.py "Petr"
    
    def formatuj_jmeno(jmeno):              # uspesne spusteni pomoci python povinny_argument.py "Marek"
    print(f"Uživatel {jmeno} spouští program")
if len(sys.argv) != 2:
    print(
        "Pro spuštění chybí argument 'jmeno',",
        "Zapiš: python povinny_argument.py 'jmeno'", sep="\n"
    )
else:
    formatuj_jmeno(sys.argv[1])
    
    
    
soucet = [int(cislo ) for cislo in sys.argv[1:]]             # priklad na vice argumentu
pocet = len(sys.argv[1:])
print(f"Průměrná hodnota je {sum(soucet) / pocet}")
"""











   
