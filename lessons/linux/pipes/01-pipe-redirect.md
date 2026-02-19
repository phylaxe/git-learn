---
title: "Pipes und Umleitung"
level: pipes
order: 1
points: 15

setup:
  - cmd: "printf '192.168.1.1 GET /index.html 200\n192.168.1.2 GET /about.html 200\n10.0.0.1 POST /api/login 401\n192.168.1.1 GET /style.css 200\n10.0.0.1 POST /api/login 200\n192.168.1.3 GET /index.html 404\n10.0.0.2 GET /api/users 403\n192.168.1.1 GET /script.js 200\n' > access.log"

task: |
  In der Datei access.log befinden sich Web-Server-Zugriffe.
  Jede Zeile endet mit einem HTTP-Statuscode.

  Aufgaben:
  1. Finde alle Zeilen mit dem Statuscode "200" und zähle sie.
     Speichere die Anzahl (nur die Zahl) in die Datei "ok-count.txt".
  2. Leite alle Fehler-Zeilen (also Zeilen OHNE "200") in die Datei "errors.log" um.

  Tipp: grep "200" access.log | wc -l > ok-count.txt

hints:
  - "Nutze den Pipe-Operator | um Befehle zu verketten: grep '200' access.log | wc -l"
  - "Der Umleitungsoperator > schreibt die Ausgabe in eine Datei: Befehl > datei.txt"
  - "grep -v kehrt die Suche um und zeigt Zeilen die NICHT passen: grep -v '200' access.log"
  - "Vollständige Lösung: grep '200' access.log | wc -l > ok-count.txt && grep -v '200' access.log > errors.log"

solution: |
  grep "200" access.log | wc -l > ok-count.txt
  grep -v "200" access.log > errors.log

validation:
  - type: file_content
    path: ok-count.txt
    contains: "5"
  - type: file_content
    path: errors.log
    contains: "401"
---

## Pipes und Umleitung

In Linux ist die Shell eine mächtige Werkzeugkiste. Einzelne Befehle sind nützlich,
aber erst wenn man sie miteinander verbindet, entfaltet sich ihre wahre Stärke.

### Der Pipe-Operator `|`

Der senkrechte Strich `|` (Pipe) leitet die Ausgabe eines Befehls direkt als
Eingabe an den nächsten Befehl weiter:

```bash
befehl1 | befehl2 | befehl3
```

Beispiele:
```bash
ls -la | grep ".txt"          # Nur .txt-Dateien anzeigen
cat datei.txt | wc -l         # Zeilen einer Datei zählen
ps aux | grep firefox         # Firefox-Prozesse suchen
```

### Ausgabeumleitung `>`

Mit `>` wird die Ausgabe eines Befehls in eine Datei geschrieben (Datei wird überschrieben):

```bash
echo "Hallo Welt" > ausgabe.txt
ls -la > dateiliste.txt
```

Mit `>>` wird an eine bestehende Datei angehängt (kein Überschreiben):

```bash
echo "Zeile 1" > log.txt
echo "Zeile 2" >> log.txt    # Fügt hinzu statt zu überschreiben
```

### Eingabeumleitung `<`

Mit `<` liest ein Befehl aus einer Datei statt von der Tastatur:

```bash
wc -l < datei.txt
sort < unsortiert.txt
```

### Fehlerausgabe umleiten `2>`

Standardmäßig gibt es zwei Ausgabeströme: stdout (1) und stderr (2):

```bash
befehl 2> fehler.log          # Nur Fehler in Datei
befehl > ausgabe.txt 2>&1     # Alles in eine Datei
befehl > ausgabe.txt 2> /dev/null  # Fehler verwerfen
```

### grep - Muster suchen

```bash
grep "200" access.log         # Zeilen mit "200" anzeigen
grep -v "200" access.log      # Zeilen OHNE "200" anzeigen
grep -c "200" access.log      # Anzahl der Treffer
grep -n "200" access.log      # Mit Zeilennummern
```

### wc - Wörter und Zeilen zählen

```bash
wc -l datei.txt               # Anzahl der Zeilen
wc -w datei.txt               # Anzahl der Wörter
wc -c datei.txt               # Anzahl der Zeichen
```
