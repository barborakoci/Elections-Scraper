"""
projekt3.py: třetí projekt do Engeto Online Python Akademie

author: Barbora Kočí
email: barbora.koci@email.cz
discord: barca6493
"""
from requests import get
from bs4 import BeautifulSoup as bs
import csv
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
    odpoved = ziskej_odpoved_serveru("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202")
    volby_polivka = naparsuj_odpoved_na_tagy(odpoved)
    vsechny_kody = najdi_kody(volby_polivka, "td")
    kody_obci = [td.a.text for td in vsechny_kody if td.a]
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
    volici = [item for sublist in volici for item in sublist]
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
    obalky = [item for sublist in obalky for item in sublist]
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
    hlasy = [item for sublist in hlasy for item in sublist]
    return hlasy

def najdi_vsechny_strany(tag):
    polivky = ziskej_polivky()
    polivka = polivky[0]
    vsechny_strany = []
    tabulky = ["t1sa1 t1sb2", "t2sa1 t2sb2"]
    for tabulka in tabulky:
        vsechny_strany.append(polivka.find_all(tag, {"class": "overflow_name",
                                                    "headers":tabulka}))
    return vsechny_strany

def najdi_strany():
    vsechny_strany = najdi_vsechny_strany("td")
    strany = []
    for strana in vsechny_strany:
        strany.append([td.text.replace('"', '') for td in strana])
    strany = [item for sublist in strany for item in sublist]
    return strany

def najdi_vsechny_hlasy_pro_stranu(tag):
    polivky = ziskej_polivky()
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
    hps = [item for sublist in hps for item in sublist]
    return hps

def spust_soubor(uzemni_celek, vystup):
    if not uzemni_celek or not vystup:
        print("Chybí povinné agrumenty",
              "Zapiš: python projekt3.py 'uzemni_celek' 'vystup'", sep="\n")
        sys.exit(1)
    else:
        print(f"Stahuji data z vybrané URL: {uzemni_celek}")
        odpoved = ziskej_odpoved_serveru(uzemni_celek)
        volby_polivka = naparsuj_odpoved_na_tagy(odpoved)
        vsechny_kody = najdi_kody(volby_polivka, "td")
        vsechny_obce = najdi_obce(volby_polivka, "td")
        kody_obci = [td.a.text for td in vsechny_kody if td.a]
        obce = [td.text for td in vsechny_obce if td]
        volici = najdi_volice()
        obalky = najdi_obalky()
        hlasy = najdi_hlasy()
        strany = najdi_strany()
        hps = najdi_hlasy_pro_stranu()

        print(f"Ukládám výsledky do souboru {vystup}")

        with open(vystup, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["kód", "obec", "voliči", "obálky", "platné hlasy"] + strany)
            for i in range(len(obce)):
                row = [""] * 29
                kod_val, obec_val, volici_val, obalky_val, hlasy_val = kody_obci[i], obce[i], volici[i], obalky[i], \
                hlasy[i]
                row[:5] = [kod_val, obec_val, volici_val, obalky_val, hlasy_val]
                row[5:] = hps[i * 24:i * 24 + 24]
                writer.writerow(row)
        print("Ukončuji election scraper.")

if __name__ == "__main__":
    spust_soubor(sys.argv[1], sys.argv[2])















   
