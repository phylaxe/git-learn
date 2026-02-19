---
title: "Dateien lesen"
level: text
order: 1
points: 10

setup:
  - cmd: "for i in $(seq 1 20); do echo \"Zeile $i: Logeintrag vom $(date -d\"$i days ago\" +%Y-%m-%d 2>/dev/null || echo Tag-$i)\" >> logfile.txt; done"
  - cmd: "printf '[server]\nhost=localhost\nport=8080\n\n[database]\nname=myapp\nuser=admin\n' > config.ini"

task: |
  Du hast zwei Dateien: logfile.txt (20 Zeilen) und config.ini.

  Aufgaben:
  1. Zeige die ersten 5 Zeilen von logfile.txt und speichere sie in "erste.txt".
  2. Zeige die letzten 3 Zeilen von logfile.txt und speichere sie in "letzte.txt".
  3. Zähle die Anzahl der Zeilen in logfile.txt und gib das Ergebnis ein mit:
     check "20"

hints:
  - "Mit 'cat datei.txt' kannst du eine Datei vollständig ausgeben."
  - "Mit 'head -n 5 logfile.txt' gibst du die ersten 5 Zeilen aus."
  - "Mit 'tail -n 3 logfile.txt' gibst du die letzten 3 Zeilen aus."
  - "Mit '>' leitest du die Ausgabe in eine Datei um: head -n 5 logfile.txt > erste.txt"
  - "Mit 'wc -l logfile.txt' zählst du die Zeilen einer Datei."

solution: |
  head -n 5 logfile.txt > erste.txt
  tail -n 3 logfile.txt > letzte.txt
  wc -l logfile.txt
  check "20"

validation:
  - type: file_exists
    path: erste.txt
  - type: file_exists
    path: letzte.txt
  - type: check_answer
    contains: "20"
---

## Dateien lesen

Linux bietet mehrere Werkzeuge, um Textdateien anzuzeigen und zu analysieren.

### cat – Dateiinhalt ausgeben

`cat` (concatenate) gibt den vollständigen Inhalt einer Datei aus:

```bash
cat datei.txt
cat config.ini
```

Du kannst auch mehrere Dateien zusammenführen:

```bash
cat datei1.txt datei2.txt > gesamt.txt
```

### head – Anfang einer Datei

`head` zeigt standardmäßig die ersten 10 Zeilen einer Datei:

```bash
head logfile.txt          # erste 10 Zeilen
head -n 5 logfile.txt     # erste 5 Zeilen
```

### tail – Ende einer Datei

`tail` zeigt die letzten 10 Zeilen (Standard):

```bash
tail logfile.txt          # letzte 10 Zeilen
tail -n 3 logfile.txt     # letzte 3 Zeilen
tail -f logfile.txt       # Live-Ansicht (nützlich für Logs)
```

### wc – Wörter und Zeilen zählen

`wc` (word count) zählt Zeilen, Wörter und Zeichen:

```bash
wc -l datei.txt    # Anzahl Zeilen
wc -w datei.txt    # Anzahl Wörter
wc -c datei.txt    # Anzahl Zeichen (Bytes)
wc datei.txt       # alle drei auf einmal
```

### less und more – Seitenweises Lesen

Für lange Dateien eignen sich `less` und `more`:

```bash
less logfile.txt   # Pfeiltasten zum Scrollen, q zum Beenden
more logfile.txt   # Leertaste für nächste Seite
```

`less` ist flexibler als `more` und erlaubt auch rückwärts zu scrollen.

### Ausgabe umleiten mit >

Mit `>` speicherst du die Ausgabe eines Befehls in eine Datei:

```bash
head -n 5 logfile.txt > erste.txt
tail -n 3 logfile.txt > letzte.txt
```

Mit `>>` fügst du Inhalt an eine bestehende Datei an, ohne sie zu überschreiben.
