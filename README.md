# Election scraper

## Popis projektu
Projekt slouží ke stažení výsledků parlamentních voleb z roku 2017. Odkaz najdete *<a href="https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ">zde</a>*.

## Instalace knihoven
V souboru requitements.txt najdete seznam knihoven použitých v tomto projektu. 
Knihovny doporučuji nainstalovat, ideálně ve virtuálním prostředí, pomocí následujícího příkazu:
* pip install -r requirements.txt

## Spuštění programu
Spuštění programu projekt3.py vyžaduje 2 povinné agrumenty.
_python projekt3.py <odkaz_uzemniho_celku><vysledny_soubor>_
Výsledky voleb budou staženy a uloženy do csv souboru.

## Ukázka projektu
Výsledky hlasování pro okres Chomutov:
* 1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202
* 2. argument: vysledky_chomutov.csv

### Spuštění programu
_python projekt3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202" "vysledky_chomutov.csv"_

### Průběh stahování
Stahuji data z vybrané URL: _https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202_...
Ukládám výsledky do souboru *vysledky_chomutov.csv*...
Ukončuji election scraper.

### Částečný výstup
kód,obec,voliči,obálky,platné hlasy,Občanská demokratická strana,Řád národa.... 
562980,Bílence,186,113,113,4,1,0,5,5,10,0,0,1,0,0,5,2,4,54,0,1,4,0,2,0,0,15,0
562998,Blatno,434,287,287,36,0,0,11,17,36,4,2,2,0,0,27,0,6,105,0,1,5,0,2,0,0,32,1


