# Importiert requests zum Herunterladen der HTML-Datei.
import requests

# Importiert das Datumssystem.
import datetime

# Importiert .json zur Datenverarbeitung.
import json

# Setzt die Abstände fest.
timeFrames = {
    "1j": (0, 1),
    "6m": (1, 6),
    "1m": (1, 1)
}


# Definiert die Methode zur Datenaqurierung.
# noinspection PyUnusedLocal
def OnvistaData(startDate: str, endDate: str, ID: str, type: str, filename: str):
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
        - Oft steht die onvista-ID im Link nach dem Kürzel "notation", es ist aber auch immer möglich auf die
        Schaltfläche "alle Kurse" zu gehen und dort die .cvs-Datei herunterzuladen. Dort findet man nun die onvista-ID
        wieder im Dateikürzel.
        
        Importieren einer .json-Datei in eine .Excel-Datei:
        https://www.howtogeek.com/775651/how-to-convert-a-json-file-to-microsoft-excel/

        Hilfe zur API-Erklärung:
        https://forum.portfolio-performance.info/t/historische-kurse-von-onvista-nicht-mehr-lesbar/14794/16

        Die .json-Datei beinhaltet die Zeitabstände in dem timestamp-Format, High, Low, Closing, First, Volumen und
        Number-Prices.
    """

    # Formatiert die Art des angefragten Objektes.
    if type.lower() == "aktie":
        type = "STOCK"
    elif type.lower() == "index":
        type = "FUND"
    else:
        print("Kein gültiger Typ.")
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
            print("Ungültiges Enddatum.")
            return 0


    # Formatiert das Anfangsdatum.
    if startDate is None:
        print("Das Anfangsdatum darf nicht frei bleiben.")
        return 0

    # Berechnet die Differenz von einem Jahr.
    elif startDate.lower() == "1j":
        endDate = str(datetime.datetime.now())
        ftemp = endDate.split("-")

        startDate = f"{str(int(ftemp[0])-1)}-{ftemp[1]}-{str(ftemp[2].split(' ')[0])}T00:00:00:000Z"

    # Berechnet die Differenz der 6 Monate.
    elif startDate.lower() == "6m":
        endDate = str(datetime.datetime.now())
        ftemp = endDate.split("-")

        if str(int(ftemp[1])-6) < 1:
            ftemp[2] = str(int(ftemp[2]) - 1)
            ftemp[1] = 6
        else:
            ftemp[1] = str(int(ftemp[1])-6)
        startDate = f"{ftemp[2]}-{ftemp[1]}-{ftemp[0]}T00:00:00:000Z"

    # Berechnet die Different von einem Monat.
    elif startDate.lower() == "1m":
        endDate = str(datetime.datetime.now())
        ftemp = endDate.split("-")

        if str(int(ftemp[1])-1) < 1:
            ftemp[2] = str(int(ftemp[2]) - 1)
            ftemp[1] = 11
        startDate = f"{ftemp[2]}-{ftemp[1]}-{ftemp[0]}T00:00:00:000Z"

    # Zerlegt das Datum in eine datetime-Angabe.
    else:
        ftemp = startDate.split(".")
        startDate = f"{ftemp[2]}-{ftemp[1]}-{ftemp[0]}T00:00:00:000Z"

    ftemp = startDate.split("-")

    # Schaut nach der Validität des Anfangsdatums.
    try:
        # noinspection PyUnboundLocalVariable
        testDate = datetime.datetime(int(ftemp[0]), int(ftemp[1]), int(ftemp[2].split('T')[0]))
    except ValueError:
        print("Ungültiges Startdatum.")
        return 0

    # Fragt die Daten der onvista-API an.
    body = requests.get(f"https://api.onvista.de/api/v1/instruments/{type}/{ID}/chart_history?endDate={endDate}&idNotation={ID}&resolution=1D&startDate={startDate}")

    jsonData = body.text
    # Fängt einen Fehler bei der Datenanforderung ab.
    if "errorMessage" in jsonData:
        print("Die ID ist nicht korrekt.")
        return 0

    # Speichert die Datei als .json-Datei.
    try:
        with open(filename+'.json', 'w', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)
            print("Datei wurde erfolgreich abgespeichert.")
    except OSError:
        print("Ungültiger Dateiname.")
        return 0


# Demonstration.
OnvistaData(startDate="1j", endDate=None, filename="Fresenius", ID=1958612, type="Aktie")
OnvistaData(startDate="1j", endDate=None, filename="Euro Stoxx 50", ID=13320012, type="Index")
