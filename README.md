# Fahndungen des Bundeskriminalamtes (BKA)

## Was ist das hier? 

Dies ist ein Scraper, der den den Zugriff auf die (Personen-) Fahndungsliste des BKA ermöglicht. \
Die Ausgabe erfolgt im JSON Format mit folgendem Schema:

```json
[
  {
    "category": "",
    "img": "",
    "name": "",
    "info": {
      "Delikt": "",
      "...": ""
    }
  }
]
```

## Benutzung

Alle Einträge der Fahndungsliste als `list[dict]`:

```py
from BKA import BKA

json = BKA().get_wanted_persons()
```

`get_wanted_persons()` besitzt außerdem einen optionalen Parameter für Pretty-Printing:

```py
BKA().get_wanted_persons(True)
```