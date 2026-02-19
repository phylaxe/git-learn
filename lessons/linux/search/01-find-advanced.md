---
title: "Dateien finden wie ein Profi"
level: search
order: 1
points: 15

setup:
  - cmd: "mkdir -p projekt/{src,tests,docs,build}"
  - cmd: "touch projekt/src/app.py projekt/src/utils.py projekt/tests/test_app.py projekt/docs/README.md"
  - cmd: "echo 'big file' > projekt/build/output.bin"
  - cmd: "touch -t 202301011200 projekt/docs/README.md"
  - cmd: "find projekt -name '*.py' -exec chmod 644 {} \\;"

task: |
  Im Verzeichnis projekt/ gibt es mehrere Unterordner und Dateien.

  Aufgaben:
  1. Finde alle .py-Dateien in projekt/ und speichere die Liste in "python-files.txt".
     Jeder Pfad soll auf einer eigenen Zeile stehen.

  2. Füge allen Dateien im Verzeichnis projekt/tests/ die Ausführ-Berechtigung hinzu
     (chmod 755). Nutze dazu find mit -exec.

  Tipp: find projekt/ -name "*.py" > python-files.txt

hints:
  - "find sucht rekursiv: find projekt/ -name '*.py'"
  - "Die Ausgabe in eine Datei umleiten: find projekt/ -name '*.py' > python-files.txt"
  - "find mit -exec: find projekt/tests/ -type f -exec chmod 755 {} \\;"
  - "Der Platzhalter {} steht für den gefundenen Dateinamen, \\; beendet den exec-Ausdruck"
  - "Vollständige Lösung: find projekt/ -name '*.py' > python-files.txt && find projekt/tests/ -type f -exec chmod 755 {} \\;"

solution: |
  find projekt/ -name "*.py" > python-files.txt
  find projekt/tests/ -type f -exec chmod 755 {} \;

validation:
  - type: file_content
    path: python-files.txt
    contains: "app.py"
  - type: file_content
    path: python-files.txt
    contains: "test_app.py"
  - type: file_permissions
    path: projekt/tests/test_app.py
    expected: "755"
---

## Dateien finden wie ein Profi

Der `find`-Befehl ist eines der mächtigsten Werkzeuge in Linux. Er durchsucht
Verzeichnisbäume nach Dateien und kann direkt Aktionen auf die gefundenen Dateien anwenden.

### Grundlagen von find

```bash
find pfad/ -name "muster"          # Nach Dateiname suchen
find pfad/ -iname "muster"         # Ohne Groß-/Kleinschreibung
find . -name "*.py"                # Alle Python-Dateien hier
find / -name "config.txt" 2>/dev/null  # Im ganzen System
```

### Nach Typ filtern

```bash
find pfad/ -type f                 # Nur Dateien (files)
find pfad/ -type d                 # Nur Verzeichnisse (directories)
find pfad/ -type l                 # Nur symbolische Links
find pfad/ -type f -name "*.sh"    # Dateien mit .sh-Endung
```

### Nach Größe filtern

```bash
find pfad/ -size +10M              # Größer als 10 Megabyte
find pfad/ -size -1k               # Kleiner als 1 Kilobyte
find pfad/ -size 100c              # Genau 100 Bytes
```

### Nach Zeit filtern

```bash
find pfad/ -mtime -7               # Geändert in letzten 7 Tagen
find pfad/ -mtime +30              # Älter als 30 Tage
find pfad/ -newer andere.txt       # Neuer als andere.txt
find pfad/ -atime -1               # Letzter Zugriff heute
```

### Aktionen mit -exec

Mit `-exec` kann find direkt Befehle auf gefundene Dateien anwenden:

```bash
find pfad/ -name "*.tmp" -exec rm {} \;        # Löschen
find pfad/ -name "*.sh" -exec chmod +x {} \;   # Ausführbar machen
find pfad/ -type f -exec ls -lh {} \;          # Details anzeigen
```

Der `{}` Platzhalter steht für den Dateinamen, `\;` beendet den exec-Ausdruck.

Effizienter mit `+` statt `\;` (übergibt alle auf einmal):
```bash
find pfad/ -name "*.tmp" -exec rm {} +
```

### Logische Verknüpfungen

```bash
find pfad/ -name "*.py" -and -type f          # Beides muss stimmen
find pfad/ -name "*.py" -or -name "*.js"      # Eines muss stimmen
find pfad/ -not -name "*.tmp"                 # Nicht diese
find pfad/ \( -name "*.py" -or -name "*.js" \) -type f
```

### find mit xargs kombinieren

```bash
find pfad/ -name "*.log" | xargs rm           # Schneller als -exec
find pfad/ -name "*.py" | xargs wc -l         # Zeilen zählen
find pfad/ -name "*.txt" | xargs grep "Fehler"  # In Dateien suchen
```

### Ausgabe anpassen mit -printf

```bash
find pfad/ -name "*.py" -printf "%f\n"        # Nur Dateiname
find pfad/ -type f -printf "%s %p\n"          # Größe und Pfad
```
