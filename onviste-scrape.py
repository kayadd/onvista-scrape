# Importiert requests zum Herunterladen der HTML-Datei.
import time

import requests

# Importiert das Datumssystem.
import datetime

# Importiert Jason zur Datenverarbeitung.
import json

# Setzt die Abstände fest.
timeFrames = {
    "1j": (0, 1),
    "6m": (1, 6),
    "1m": (1, 1)
}


# noinspection PyUnusedLocal
def scrapeData(startDate: str, endDate: str, ID: str, type: str, filename: str):
    """ startDate: str
        Kann eines dieser Kürzel haben {
            '1j': Ein Jahr
            '6m': Sechs Monate
            '1m': Einen Monat
        }
        Muss ein gültiges Datum sein.

        endDate: str
        Muss ein gültiges Datum sein.

        ID: str
        Die ID ist die interne Nummer der Aktie oder des Indizes bei onvista.
        Diese wird herausgefunden, indem man die erste Zahl aus der dem Dateinamen der .csv-Datei nimmt.

        type: str
        Gibt den Typ des Finanzobjektes an.
        Kann eines dieser Kürzel haben {
            'Aktie': 'STOCK'
            'Index': 'FUND'
        }

        filename: str
        Gibt den Dateinamen der .json-Datei an. Darf also folgende Zeichen nicht enthalten.
        /\?|*":<>.

        Hilfe:

        Finden der onvista-ID für Aktien:
        -Auf der Seite das Orderbuch anklicken und dort die neueste .cvs-Datei herunterladen. Die ID steht nun als
        erste Zahl in dem Dateinamen

        Finden der onvista-ID für Indizes:
        -Im angeklickten Link zum Index ist dies die letzte Zahl. Davor steht das Prefix: ?notation=

        Importieren einer .json-Datei in eine .Excel-Datei:
        https://www.howtogeek.com/775651/how-to-convert-a-json-file-to-microsoft-excel/

        Hilfe zur API-Erklärung:
        https://forum.portfolio-performance.info/t/historische-kurse-von-onvista-nicht-mehr-lesbar/14794/16

        Die .json-Datei beinhaltet die Zeitabstände in dem timestamp-Format, High, Low, Closing, First, Volumen und
        Number-Prices.
    """

    # Formatiert die Art des angefragten Objektes:
    if type.lower() == "aktie":
        type = "STOCK"
    elif type.lower() == "index":
        type = "FUND"
    else:
        print("Kein gültiger Typ")
        return 0

    # Formatiert das Enddatum.
    if endDate is None:
        endDate = str(datetime.datetime.now())
        ftemp = endDate.split("-")
        endDate = f"{ftemp[0]}-{ftemp[1]}-{ftemp[2].split(' ')[0]}T00:00:00:000Z"

    else:
        ftemp = endDate.split(".")
        endDate = f"{ftemp[2]}-{ftemp[1]}-{ftemp[0]}T00:00:00:000Z"

        # Schaut nach der Validität des Enddatums.
        try:
            # noinspection PyUnboundLocalVariable
            testDate = datetime.datetime(int(ftemp[2]), int(ftemp[1]), int(ftemp[0]))
        except ValueError:
            print("Ungültiges Enddatums.")
            return 0


    # Formatiert das Anfangsdatum.
    if startDate is None:
        print("Das Anfangsdatum darf nicht frei bleiben.")
        return 0

    # Berechnet die Differenz von einem Jahr
    if startDate.lower() == "1j":
        endDate = str(datetime.datetime.now())
        ftemp = endDate.split("-")

        startDate = f"{str(int(ftemp[0])-1)}-{ftemp[1]}-{str(ftemp[2].split(' ')[0])}T00:00:00:000Z"

    # Berechnet die Differenz der 6 Monate.
    if startDate.lower() == "6m":
        endDate = str(datetime.datetime.now())
        ftemp = endDate.split("-")

        if str(int(ftemp[1])-6) < 1:
            ftemp[2] = str(int(ftemp[2]) - 1)
            ftemp[1] = 6
        else:
            ftemp[1] = str(int(ftemp[1])-6)
        startDate = f"{ftemp[2]}-{ftemp[1]}-{ftemp[0]}T00:00:00:000Z"

    # Berechnet die Different von einem Monat.
    if startDate.lower() == "1m":
        endDate = str(datetime.datetime.now())
        ftemp = endDate.split("-")

        if str(int(ftemp[1])-1) < 1:
            ftemp[2] = str(int(ftemp[2]) - 1)
            ftemp[1] = 11
        startDate = f"{ftemp[2]}-{ftemp[1]}-{ftemp[0]}T00:00:00:000Z"

    print(startDate)

    if startDate is not None:
        ftemp = startDate.split(".")
        startDate = f"{ftemp[2]}-{ftemp[1]}-{ftemp[0]}T00:00:00:000Z"

    print(startDate)
    # Schaut nach der Validität des Anfangsdatums.
    #try:
        # noinspection PyUnboundLocalVariable
        #testDate = datetime.datetime(int(ftemp[0]), int(ftemp[1]), int(ftemp[2].split(' ')[0]))
    #except IndexError:
        #testDate = datetime.datetime(int(ftemp[2]), int(ftemp[1]), int(ftemp[1].split(' ')[0]))

    #except ValueError:
    #    print("Ungültiges Startdatum.")
    #    return 0


    body = requests.get(f"https://api.onvista.de/api/v1/instruments/{type}/25096683/chart_history?endDate={endDate}&idNotation={ID}&resolution=1D&startDate={startDate}")

    jsonData = body.text
    if "errorMessage" in jsonData:
        print("Die ID ist nicht korrekt.")
        return 0

    print(jsonData.split("[")[1].count(","))



    try:
        with open(filename+'.json', 'w', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)
            print("Datei wurde erfolgreich abgespeichert.")
    except OSError:
        print("Ungültiger Dateiname.")
        return 0


# Regelt die Eingabe.
if False:
    a = 1
    # Modell der Einzeleingabe.
    while a == 0:
        pstartDate = input("Bitte geben sie das Startdatum oder das Zeitraumkürzel('1j', '6m', `1m`) ein: ")
        pendDate = input("Bitte geben sie das Enddatum ein: ")
        pfileName = input("Bitte gib den Dateinamen der .json-Datei ein: ")
        pID = input("Bitte gib die onvista-ID des Finanzobjektes ein: ")
        ptype = input("Bitte gib den Typ des Finanzobjektes('Aktie' oder 'Index') ein:")

        scrapeData(startDate=pstartDate, endDate=pendDate, filename=pfileName, ID=pID, type=ptype)

    # Modell der Abgabe durch eine Dateieingabe der Daten und den Zeitraum.
    # Die Einteilung erfolgt innerhalb der Datei in dieser Reihenfolge:
    # onvista-ID, Dateiname, Finanzobjekttyp
    # Beispiel; 0234598, Amazon, Aktie
    pstartDate = input("Bitte geben sie das Startdatum oder das Zeitraumkürzel('1j', '6m', `1m`) ein: ")
    pendDate = input("Bitte geben sie das Enddatum ein: ")
    mFile = input("Bitte geben sie die .txt-Datei mit den Dateibezeichnungen, dem Typ und dem Onvista-Index an: ")

    fdata = open(mFile, "r")
    data = fdata.readlines()

    for i in range(len(data)):
        temp = data[i].replace("\n", "").split(",")
        if scrapeData(startDate=pstartDate, endDate=pendDate, filename=temp[1], ID=temp[0], type=temp[2]) is 0:
            exit()

# Demonstration
# scrapeData(startDate="1j", endDate=None, filename="Fresenius", ID=1958612, type="Aktie")
# scrapeData(startDate="1j", endDate=None, filename="Euro Stoxx 50", ID=13320012, type="Index")

    