
"""
projekt3.py: třetí projekt do Engeto Online Python Akademie

author: Barbora Kočí
email: barbora.koci@email.cz
discord: barca6493
"""
from requests import get
from bs4 import BeautifulSoup as bs
import csv
import sys

def ziskej_odpoved_serveru(url):
    return get(url).text

def naparsuj_odpoved_na_tagy(obsah):
    return bs(obsah, features="html.parser")

def spust_soubor(uzemni_celek, vystup):
    if not uzemni_celek or not vystup:
        print("Chybí povinné agrumenty",
              "Zapiš: python projekt3.py 'uzemni_celek' 'vystup'", sep="\n")
        sys.exit(1)

    print(f"Stahuji data z vybrané URL: {uzemni_celek}")
    odpoved = ziskej_odpoved_serveru(uzemni_celek)
    volby_polivka = naparsuj_odpoved_na_tagy(odpoved)
    vsechny_kody = volby_polivka.find_all("td", {"headers": ["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"]})
    kody_obci = [td.a.text for td in vsechny_kody if td.a]
    vsechny_obce = volby_polivka.find_all("td", {"class": "overflow_name", "headers": ["t1sa1 t1sb2", "t2sa1 t2sb2", "t3sa1 t3sb2"]})
    obce = [td.text for td in vsechny_obce if td]
    xvyber = uzemni_celek[-4:]
    vsechny_url = [f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec={kod}&xvyber={xvyber}" for kod in kody_obci]
    strany = []

    print("Získávám názvy stran...")
    odpoved_obce = ziskej_odpoved_serveru(vsechny_url[0])
    obec_polivka = naparsuj_odpoved_na_tagy(odpoved_obce)
    for td in obec_polivka.find_all("td", {"class": "overflow_name", "headers": ["t1sa1 t1sb2", "t2sa1 t2sb2"]}):
        strany.append(td.text.replace('"', ''))

    print(f"Ukládám výsledky do souboru {vystup}")
    with open(vystup, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["kód", "obec", "voliči", "obálky", "platné hlasy"] + strany)
        for i in range(len(obce)):
            url = vsechny_url[i]
            odpoved_obce = ziskej_odpoved_serveru(url)
            obec_polivka = naparsuj_odpoved_na_tagy(odpoved_obce)
            volici = obec_polivka.find("td", {"headers": "sa2"}).text.replace('\xa0', ' ')
            obalky = obec_polivka.find("td", {"headers": "sa3"}).text.replace('\xa0', ' ')
            hlasy = obec_polivka.find("td", {"headers": "sa6"}).text.replace('\xa0', ' ')
            hlasy_pro_stranu = [td.text.replace('\xa0', ' ') for td in obec_polivka.find_all("td", {"class": "cislo", "headers": ["t1sa2 t1sb3", "t2sa2 t2sb3"]})]
            row = [kody_obci[i], obce[i], volici, obalky, hlasy] + hlasy_pro_stranu
            writer.writerow(row)
    print("Ukončuji election scraper.")

if __name__ == "__main__":
    spust_soubor(sys.argv[1], sys.argv[2])
