---
title: "tee und xargs"
level: pipes
order: 2
points: 20

setup:
  - cmd: "mkdir -p cleanup"
  - cmd: "touch cleanup/old1.tmp cleanup/old2.tmp cleanup/old3.tmp cleanup/keep.txt"
  - cmd: "printf 'apple\nbanana\ncherry\napple\ndate\nbanana\napple\n' > fruits.txt"

task: |
  Du hast zwei Aufgaben:

  1. Finde alle einzigartigen Fruechte in fruits.txt (keine Duplikate).
     Nutze sort und uniq mit Pipes. Verwende tee um das Ergebnis gleichzeitig
     anzuzeigen UND in "unique-fruits.txt" zu speichern.

  2. Loesche alle .tmp-Dateien im Verzeichnis cleanup/ mit find und xargs.
     Die Datei keep.txt soll dabei erhalten bleiben.

  Tipp: sort fruits.txt | uniq | tee unique-fruits.txt
         find cleanup/ -name "*.tmp" | xargs rm

hints:
  - "sort sortiert die Ausgabe alphabetisch: sort fruits.txt"
  - "uniq entfernt aufeinanderfolgende Duplikate (daher erst sort): sort fruits.txt | uniq"
  - "tee schreibt gleichzeitig auf den Bildschirm UND in eine Datei: befehl | tee datei.txt"
  - "find gibt Dateinamen aus, xargs uebergibt sie als Argumente: find cleanup/ -name '*.tmp' | xargs rm"
  - "Vollstaendige Loesung: sort fruits.txt | uniq | tee unique-fruits.txt && find cleanup/ -name '*.tmp' | xargs rm"

solution: |
  sort fruits.txt | uniq | tee unique-fruits.txt
  find cleanup/ -name "*.tmp" | xargs rm

validation:
  - type: file_content
    path: unique-fruits.txt
    contains: "cherry"
  - type: file_not_exists
    path: cleanup/old1.tmp
  - type: file_exists
    path: cleanup/keep.txt
---

## tee und xargs

Zwei besonders nützliche Werkzeuge für die Arbeit mit Pipes sind `tee` und `xargs`.
Sie erweitern die Möglichkeiten der Pipeline erheblich.

### tee - Der T-Verteiler

`tee` liest von stdin und schreibt gleichzeitig auf stdout UND in eine Datei –
wie ein T-Rohr in der Wasserleitung:

```bash
befehl | tee ausgabe.txt          # Anzeigen UND speichern
befehl | tee -a ausgabe.txt       # Anhaengen statt ueberschreiben
befehl | tee datei.txt | weiter   # In Kette einbauen
```

Beispiel:
```bash
ls -la | tee dateiliste.txt | grep ".py"
# Speichert die vollstaendige Liste, zeigt nur .py-Dateien
```

### sort und uniq - Duplikate entfernen

Das klassische Muster zum Entfernen von Duplikaten:

```bash
sort datei.txt | uniq            # Einzigartige Zeilen
sort datei.txt | uniq -c         # Mit Haeufigkeit
sort datei.txt | uniq -d         # Nur Duplikate anzeigen
sort datei.txt | uniq -u         # Nur einmalige Zeilen
```

Wichtig: `uniq` prueft nur aufeinanderfolgende Zeilen, daher immer erst `sort`!

### xargs - Argumente aus stdin

`xargs` liest Zeilen von stdin und uebergibt sie als Argumente an einen Befehl:

```bash
find . -name "*.tmp" | xargs rm           # Dateien loeschen
find . -name "*.txt" | xargs wc -l        # Zeilen zaehlen
echo "datei1 datei2 datei3" | xargs ls    # Dateien auflisten
```

Nuetzliche xargs-Optionen:
```bash
xargs -n 1 befehl     # Einen Wert pro Aufruf
xargs -I {} befehl {} # Platzhalter {} fuer den Wert
xargs -p befehl       # Vor jedem Aufruf bestaetigen
```

### find - Dateien suchen und verarbeiten

```bash
find verzeichnis/ -name "*.tmp"           # Nach Name suchen
find verzeichnis/ -type f -name "*.log"   # Nur Dateien
find verzeichnis/ -mtime +7               # Aelter als 7 Tage
find verzeichnis/ -exec rm {} \;          # Ausfuehren fuer jede Datei
find verzeichnis/ -name "*.tmp" | xargs rm  # Mit xargs loeschen
```

### Befehlsverkettung mit Pipes

```bash
cat datei.txt | sort | uniq | tee ergebnis.txt | wc -l
# Liest -> sortiert -> dedupliziert -> speichert -> zaehlt
```
