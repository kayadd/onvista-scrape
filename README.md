This repository is used to scrape data from the <a href="https://www.onvista.de">onvista</a>-api. The website onvista provides some historical and current financial data.<br>
The data contains: <br>

-DATE: The date, that the data was submitted. <br>
-FIRST: The price, that the stock or fund started with on that day. <br>
-HIGH: The highest price, that the stock or fund on that day. <br>
-LOW: The lowest price, that the stock or fund on that day. <br>
-ClOSE: The price, that the stock or fund ended with. <br>
-VOLUME: The number of stock, that were sold or bought. <br>
-PICE-Price: The price of a single piece. <br>

The documentation for onvistaData: <br>

startDate: str <br>
      Could be { <br>
            '1j': one year <br>
            '6m': six months <br>
            '1m': one month <br>
        }<br>
        or must be a valid date.<br>

  endDate: str <br>
        Must be a valid date or None. If the parameter is set to None it will assume the last possible date, which should be the data of the           last day <br>

ID: str <br>
        The id must be the internal onvista-ID. How to find these data is described in the help-section <br>

type: str <br>
        Sets the type of the financial object, that the data corresponds to. <br>
        Could be { <br>
            'Aktie': 'STOCK' <br>
            'Index': 'FUND' <br>
        } <br>

  filename: str <br>
        Sets the filename of the .json-file. Therefore it cannot contain any of the following symbols. <br>
        /\?|*":<>. <br>


  Help-Finding the onvista-Id for stocks <br>
        -Click on the button labeled "Orderbuch" and download a .cvs-Datei. The first number in the filename is  <br>
        the internal onvista-ID. <br>
        
  Help-Finding the onvista-ID for funds <br>
        - Sometimes the onvista-ID contains the ID after the identifier "notation" in the link, but it is more convenient and reliable <br>
        to click on the button labeled "alle Kurse" and download the .cvs-Datei . The first number in the filename is <br>
        the internal onvista-ID. <br>
        
Help-Import .json to into Excel      <br>  
        How to import a .json.file into Excel: <br>
        https://www.howtogeek.com/775651/how-to-convert-a-json-file-to-microsoft-excel/ <br>
