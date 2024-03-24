# PDF facturatie programma
GUI programma ontwikkeld in Python3 om PDF pagina's in verschillende PDF bestanden van een overlay/stempel (= voorgrond) te voorzien. De overlay zelf is de eerste pagina uit het stempel PDF bestand, dat wordt ingesteld in de GUI. Een optionele bestandsnaam suffix kan tevens worden ingesteld om de bestandsnamen van de resulterende PDF's aan te passen.

## Installatie
Officiële release v1.0.0 is beschikbaar via de sectie "Releases" hier op GitHub.
Er zijn 2 versies voor Windows:
- Een `zip`-bestand dat een minimale executable/binary (`exe`-bestand) bevat die gelinkt is met een bijbehorende map met afhankelijkheden. De inhoud van dit `zip` bestand kan worden uitgepakt onder de `C:\Program Files\`-map of een andere locatie. Vervolgens kan men een snelkoppeling maken voor het `exe`-bestand en deze op het bureaublad plaatsen.
- Een alles-in-één `exe`-bestand dat 1 executable/binary is waarin alle afhankelijkheden al zijn opgenomen. Dit maakt de installatie eenvoudiger, maar zorgt er ook voor dat het programm wat trager opstart.
> [!IMPORTANT]
> Als je het programma in een beveiligd pad zoals de `C:\Program Files\`-map installeert, dan moet je het programma als een administrator gebruiker uitvoeren als je wil dat de standaardinstellingen kunnen worden weggeschreven.

## Gebruik
![alt text](https://github.com/CodeByAlejandro/PDF_facturatie_programma/blob/master/screenshots/PDF_facturatie_programma_screenshot.png)

Je gebruikt het programma als volgt:
1. Selecteer een stempel PDF met de overlay/stempel pagina via de daarvoor voorziene knop
2. Selecteer de resultaat-map waar de aangepaste PDF bestanden worden opgeslagen
3. Kies optioneel voor een bestandsnaam suffix of achtervoegsel om de naam van de resulterende PDF bestanden tevens te wijzigen ten opzichte van het origineel. Dit is handig als de resultaat-map ook dezelfde map is waar de originele PDF bestanden worden bijgehouden, die moeten worden bewerkt. Zodoende voorkomt u dat deze bestanden worden overschreven. Standaard wordt de suffix "_aangepast" voorgesteld, die voor de extensie `.pdf` zal worden toegevoegd.
4. Selecteer de originele PDF bestanden die moeten worden bijgewerkt aan de hand van de daarvoor voorziene knop. U kan hier meerdere bestanden selecteren door de CTRL-toets ingedrukt te houden. Verder is het ook mogelijk om een van-tot bereik aan bestanden te selecteren door de SHIFT-toets ingedrukt te houden en een begin -en eind bestand te selecteren. Alle bestanden ertussen worden dan ook automatisch geselecteerd in het selectievenster. **Deze informatie kan u ook opvragen door op de info-knop te klikken.**
5. Als u per ongeluk heeft gemist bij de selectie van de bestanden, dan kunt u de geselecteerde lijst terug leegmaken door op de daarvoor voorziene knop te klikken.
6. Indien u alles correct heeft ingegeven klikt u op de knop om de geselecteerde PDF bestanden te verwerken. Vervolgens wordt de verwerking opgestart en wordt er een verwerkingsstatus op het scherm getoond. De melding "Verwerking voltooid" geeft aan wanneer de verwerking compleet is.

### Standaardinstellingen
Na verwerking van een aantal PDF-bestanden worden de gekozen instellingen automatisch opgeslagen voor een volgend gebruik van het programma. Dit wordt bijgehouden in een `defaults.json`-bestand. Indien u bij installatie het `zip`-bestand hebt gebruikt, dan komt dit bestand terecht in de `defaults`-map in de `_internal`-map die in het `zip`-bestand was opgenomen (gebundeld bij de executable/binary (`exe`-bestand). Indien u bij installatie het alles-in-éém `exe`-bestand hebt gebruikt, dan wordt dit bestand intern opgeslagen, in deze binary. Bij installatie in een python virtual environment wordt dit bestand opgeslagen in de `defaults/`-map van het project.

### Foutmeldingen
Indien er tijdens de uitvoering van het programma fouten optreden, dan worden deze steeds op het scherm getoond.
Hieronder enkele voorbeelden:

![alt text](https://github.com/CodeByAlejandro/PDF_facturatie_programma/blob/master/screenshots/PDF_facturatie_programma_fout_bij_laden_standaardinstellingen.png)
![alt text](https://github.com/CodeByAlejandro/PDF_facturatie_programma/blob/master/screenshots/PDF_facturatie_programma_fout_bij_opslaan_standaardinstellingen.png)
![alt text](https://github.com/CodeByAlejandro/PDF_facturatie_programma/blob/master/screenshots/PDF_facturatie_programma_fout_bij_schrijven_resultaat_PDF_bestanden.png)
![alt text](https://github.com/CodeByAlejandro/PDF_facturatie_programma/blob/master/screenshots/PDF_facturatie_programma_programmatiefout_bij_vernieuwen_sleutel_standaardinstelling.png)
![alt text](https://github.com/CodeByAlejandro/PDF_facturatie_programma/blob/master/screenshots/PDF_facturatie_programma_programmatiefout_bij_vernieuwen_waarde_standaardinstelling.png)

## Aanpassen aan de broncode
Installeer de software manueel in een zogenaamde python virtual environment met volgende commando's:
```shell
git clone https://github.com/CodeByAlejandro/PDF_facturatie_programma.git
cd PDF_facturatie_programma
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
Vervolgens kan u het programma als volgt oproepen:
```shell
python app/main.py
```

## Testen programma
Voor genereren van voldoende groote test PDFs om een verwerkingsstatus te zien te krijgen kan u de python module `build_large_test_pdfs.py` , uit de `test/`-map uivoeren. Dit zal 10 PDF's met elk 1000 pagina's genereren in de `input/`-map, op basis van de reeds bestaande PDF in die map.

## Deïnstallatie van manuele installatie in python virtual environment
Deactiveer de virtual environment via de reeds geëxporteerde shell functie `deactivate` (werd aangemaakt tijdens sourcen van het activatie-script):
```shell
deactivate
```
Vervolgens schrapt u het lokale project:
```shell
cd ..
rm -rf PDF_facturatie_programma
```

## Beschrijving project structuur
Hieronder volgt een beschrijving van de verschillende mappen en bestanden:
- app/
  -  Bevat alle Python broncode van het programma
- build_tools/
  - Bevat afhankelijkheden en scripts om de Windows executable/binary (`exe`-bestand) te bouwen
- defaults/
  - Bevat map met standaard stempel PDF en is ook de locatie waarin de standaardinstellingen worden weggeschreven (`defaults.json`)
- images/
  - Bevat afbeeldingen die worden gebruikt door het programma
- input/
  - Bevat voorbeeld PDF en locatie voor input PDFs om te verwerken
- screenshots/
  - Bevat afbeeldingen van het de graphische user interface van het programma
- technical_analysis/
  - Bevat documenten met betrekking tot technische analyse. Het UML-diagram van versie v1.0.0 werd hierin opgenomen.
- test/
  - Bevat python modules voor genereren van testdata en hulptools voor het testen van het programma.
- requirements.txt
  - Bevat Python afhankelijkheden van het programma
