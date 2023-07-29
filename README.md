This repository is used to scrape data from the onvista-api. The website onvista provides some historical and current financial data.
The data contains:

-DATE: The date, that the data was submitted.
-FIRST: The price, that the stock or fund started with on that day.
-HIGH: The highest price, that the stock or fund on that day.
-LOW: The lowest price, that the stock or fund on that day.
-ClOSE: The price, that the stock or fund ended with.
-VOLUME: The number of stock, that were sold or bought.
-PICE-Price: The price of a single piece.

The documentation for onvistaData:

startDate: str
      Could be {
            '1j': one year
            '6m': six months
            '1m': one month
        }
        or must be a valid date.

  endDate: str
        Must be a valid date or None. If the parameter is set to None it will assume the last possible date.

ID: str
        The id must be the internal onvista-ID. How to find these data is described in the help-section

type: str
        Sets the type of the financial object, that the data corresponds to.
        Could be {
            'Aktie': 'STOCK'
            'Index': 'FUND'
        }

  filename: str
        Sets the filename of the .json-file. Therefore it cannot contain any of the following symbols.
        /\?|*":<>.


  Help-Finding the onvista-Id for stocks
        -Click on the button labeled "Orderbuch" and download a .cvs-Datei. The first number in the filename is 
        the internal onvista-ID.
        
  Help-Finding the onvista-ID for funds
        - Sometimes the onvista-ID contains the ID after the identifier "notation" in the link, but it is more convenient and reliable
        to click on the button labeled "alle Kurse" and download the .cvs-Datei . The first number in the filename is 
        the internal onvista-ID.
        
Help-Import .json to into Excel        
        How to import a .json.file into Excel:
        https://www.howtogeek.com/775651/how-to-convert-a-json-file-to-microsoft-excel/
