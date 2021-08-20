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

Da man auf der Website mehr Inhalte nur aktiv per Knopf laden kann, wird der Methode \
`get_wanted_persons()` ein Parameter mitgegeben, der der Anzahl der geladenen Seiten entspricht. 

```py
from BKA import BKA

json = BKA().get_wanted_persons(1)
```