# Elections-Scraper
https://github.com/barborakoci/Elections-Scraper.git

python -m venv projekt3
projekt3\Scripts\Activate.ps1

python --version         # ověřím verzi Pythonu 3.12.0
python -m pip --version  # ověřím verzi manažera knihoven, novější zápis 24.0
# výpis z příkazu 'python -m pip list'
python -m pip install requests    # ověřit na pypi.org
python -m pip install beautifulsoup4
pip install asyncio
pip install httpx

# vytvořit soubor requests pomocí pycharm načíst knihovny
pip freeze > requirements.txt

https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Výsledný soubor budete spouštět pomocí 2 argumentů (ne pomocí funkce input). První argument obsahuje odkaz, který územní celek chcete scrapovat (př. územní celek Prostějov ), druhý argument obsahuje jméno výstupního souboru (př. vysledky_prostejov.csv)
Pokud uživatel nezadá oba argumenty (ať už nesprávné pořadí, nebo argument, který neobsahuje správný odkaz), program jej upozorní a nepokračuje.

Následně dopište README.md soubor, který uživatele seznámíte se svým projektem. Jak nainstalovat potřebné knihovny ze souboru requirements.txt, jak spustit váš soubor, příp. doplnit ukázku, kde demonstrujete váš kód na konkrétním odkaze s konkrétním výpisem.
# zapsat readme
Nadpisy můžete formátovat pomocí symbolu "#" a odstavce textu můžete psát běžně. Pokud chcete vytvořit tučný text, můžete ho obalit dvojitými hvězdičkami nebo podtržítky. Pro kurzívu se používají jednoduché hvězdičky nebo podtržítka. Pro vytvoření odrážek můžete použít znaménko "-" nebo "*". 



