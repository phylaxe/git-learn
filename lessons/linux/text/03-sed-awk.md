---
title: "Text transformieren mit sed und awk"
level: text
order: 3
points: 20

setup:
  - cmd: "printf 'name,alter,stadt\nAnna,28,Zürich\nBen,35,Berlin\nClara,22,Wien\nDavid,31,Bern\n' > mitarbeiter.csv"
  - cmd: "printf 'Version: 1.0.0\nAuthor: Old Name\nLicense: MIT\nAuthor: Old Name\n' > metadata.txt"

task: |
  Du hast zwei Dateien: mitarbeiter.csv (eine CSV-Tabelle) und metadata.txt.

  Aufgaben:
  1. Ersetze ALLE Vorkommen von "Old Name" durch "Neuer Autor" direkt in
     metadata.txt (in-place) mit sed -i.
  2. Extrahiere aus mitarbeiter.csv nur die Spalten Name und Stadt (1. und 3.
     Spalte) und speichere das Ergebnis in "namen-staedte.txt".
     Verwende: awk -F, '{print $1","$3}' mitarbeiter.csv > namen-staedte.txt

hints:
  - "sed 's/alt/neu/g' datei.txt ersetzt alle Vorkommen von 'alt' durch 'neu'."
  - "Ohne 'g' am Ende ersetzt sed nur das erste Vorkommen pro Zeile."
  - "Mit 'sed -i' wird die Datei direkt geändert (in-place): sed -i 's/Old Name/Neuer Autor/g' metadata.txt"
  - "awk liest Dateien spaltenweise. Mit -F, setzt du das Trennzeichen auf Komma."
  - "awk -F, '{print $1\",\"$3}' mitarbeiter.csv gibt Spalte 1 und 3 aus."

solution: |
  sed -i 's/Old Name/Neuer Autor/g' metadata.txt
  awk -F, '{print $1","$3}' mitarbeiter.csv > namen-staedte.txt

validation:
  - type: file_content
    path: metadata.txt
    contains: "Neuer Autor"
  - type: file_content
    path: namen-staedte.txt
    contains: "Anna"
  - type: file_content
    path: namen-staedte.txt
    contains: "Zürich"
---

## Text transformieren mit sed und awk

`sed` und `awk` sind leistungsstarke Werkzeuge zur Textverarbeitung und -transformation.

### sed – Stream Editor

`sed` verarbeitet Texte zeilenweise und eignet sich besonders für Suchen-und-Ersetzen-Operationen.

#### Grundlegende Substitution

```bash
sed 's/alt/neu/' datei.txt      # ersetzt erstes Vorkommen pro Zeile
sed 's/alt/neu/g' datei.txt     # ersetzt ALLE Vorkommen (g = global)
```

Das `s`-Kommando steht für "substitute" (ersetzen). Die Schrägstriche trennen die Teile:
`s/Suchmuster/Ersatz/Flags`

#### In-Place-Bearbeitung mit -i

Ohne `-i` gibt `sed` das Ergebnis nur auf der Konsole aus. Mit `-i` wird die Datei direkt geändert:

```bash
sed -i 's/Old Name/Neuer Autor/g' metadata.txt
```

#### Weitere sed-Beispiele

```bash
sed 's/ERROR/FEHLER/g' server.log          # Wort ersetzen
sed '/^#/d' config.ini                     # Kommentarzeilen löschen
sed -n '5,10p' logfile.txt                 # Zeilen 5–10 ausgeben
```

### awk – Musterbasierte Textverarbeitung

`awk` eignet sich hervorragend für die spaltenweise Verarbeitung strukturierter Daten wie CSV-Dateien.

#### Felder und Trennzeichen

Standardmäßig trennt `awk` Felder an Leerzeichen. Mit `-F` setzt du ein eigenes Trennzeichen:

```bash
awk '{print $1}' datei.txt         # erste Spalte (Leerzeichen als Trenner)
awk -F, '{print $1}' daten.csv     # erste Spalte, Komma als Trenner
awk -F: '{print $1,$3}' /etc/passwd
```

#### Spalten auswählen und ausgeben

```bash
awk -F, '{print $1","$3}' mitarbeiter.csv   # Spalten 1 und 3, kommagetrennt
awk -F, '{print $1" wohnt in "$3}' mitarbeiter.csv
```

#### Berechnungen mit awk

`awk` kann auch rechnen:

```bash
awk -F, 'NR>1 {sum+=$2} END {print "Durchschnittsalter:", sum/(NR-1)}' mitarbeiter.csv
```

- `NR` ist die aktuelle Zeilennummer
- `NR>1` überspringt die Kopfzeile
- `END` wird nach allen Zeilen ausgeführt

#### Muster filtern

```bash
awk '/ERROR/' server.log            # Zeilen mit ERROR ausgeben (wie grep)
awk -F, '$2 > 30' mitarbeiter.csv  # Mitarbeiter älter als 30
```

### Kombination von sed und awk

`sed` und `awk` lassen sich mit Pipes kombinieren:

```bash
grep ERROR server.log | awk '{print $1, $2}'
sed 's/,/;/g' mitarbeiter.csv | awk -F\; '{print $1}'
```
