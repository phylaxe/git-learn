---
title: "Berechtigungen lesen"
level: permissions
order: 1
points: 10

setup:
  - cmd: "touch datei.txt && chmod 644 datei.txt && mkdir ordner && chmod 755 ordner && echo '#!/bin/bash' > script.sh && chmod 700 script.sh"

task: |
  Berechtigungen lesen mit ls -l

  Das Übungsverzeichnis enthält drei Objekte:
    - datei.txt  — eine einfache Textdatei
    - ordner/    — ein Verzeichnis
    - script.sh  — ein Shell-Skript

  Schritt 1: Zeige die Berechtigungen aller Dateien an:
    ls -l

  Schritt 2: Lies die Berechtigungszeichenkette von script.sh ab.
  Die Ausgabe sieht so aus:
    -rwx------ 1 user group 13 Jan  1 00:00 script.sh

  Die ersten 10 Zeichen sind die Berechtigungen:
    - Zeichen 1:    Dateityp (- = Datei, d = Verzeichnis)
    - Zeichen 2-4:  Berechtigungen des Eigentümers (rwx)
    - Zeichen 5-7:  Berechtigungen der Gruppe (---)
    - Zeichen 8-10: Berechtigungen für alle anderen (---)

  Was sind die Berechtigungen von script.sh in symbolischer Notation?
  Gib nur den 9-stelligen Berechtigungsstring ohne den Dateityp ein,
  also z.B. rwxr-xr-x

  Reiche deine Antwort ein mit:
    check "rwx------"

hints:
  - "Führe 'ls -l' aus und lies die erste Spalte der Ausgabe."
  - "Die Berechtigungszeichenkette hat 10 Zeichen. Das erste Zeichen ist der Dateityp (- oder d). Die nächsten 9 Zeichen sind die eigentlichen Berechtigungen."
  - "Die 9 Berechtigungszeichen sind in drei Gruppen zu je 3 aufgeteilt: Eigentümer (owner), Gruppe (group), Andere (others). r=lesen, w=schreiben, x=ausführen, -=keine Berechtigung."
  - "script.sh wurde mit chmod 700 erstellt. Das bedeutet: Eigentümer darf alles (rwx), Gruppe darf nichts (---), Andere dürfen nichts (---). Die Antwort ist also: rwx------"

solution: |
  ls -l
  check "rwx------"

validation:
  - type: check_answer
    contains: "rwx------"
---

## Berechtigungen lesen

Linux verwaltet den Zugriff auf Dateien und Verzeichnisse über ein Berechtigungssystem.
Mit `ls -l` kannst du diese Berechtigungen sichtbar machen.

### Das Berechtigungsformat

Eine typische `ls -l`-Ausgabe sieht so aus:

```
-rwxr-xr-- 2 alice devs 1024 Jan 15 10:00 script.sh
drwxr-x--- 3 alice devs 4096 Jan 15 09:00 ordner/
-rw-r--r-- 1 alice devs  512 Jan 15 08:00 datei.txt
```

Die erste Spalte (z.B. `-rwxr-xr--`) enthält 10 Zeichen:

| Position | Bedeutung |
|----------|-----------|
| 1        | Dateityp: `-` = Datei, `d` = Verzeichnis, `l` = Symlink |
| 2–4      | Eigentümer-Berechtigungen (owner) |
| 5–7      | Gruppen-Berechtigungen (group) |
| 8–10     | Berechtigungen für alle anderen (others) |

### Die drei Berechtigungstypen

Jede der drei Gruppen besteht aus drei Zeichen:

- **r** (read) — Lesen erlaubt
- **w** (write) — Schreiben erlaubt
- **x** (execute) — Ausführen erlaubt (bei Verzeichnissen: Betreten)
- **-** — diese Berechtigung fehlt

### Beispiel: `rwxr-x---`

```
rwx  r-x  ---
 |    |    |
 |    |    Andere: kein Zugriff
 |    Gruppe: lesen + ausführen
 Eigentümer: lesen + schreiben + ausführen
```

### Weitere nützliche Optionen

```bash
ls -la          # Auch versteckte Dateien anzeigen (beginnen mit .)
ls -lh          # Dateigrößen lesbar formatieren (K, M, G)
stat datei.txt  # Detaillierte Metadaten einer Datei
```

### Warum sind Berechtigungen wichtig?

Berechtigungen schützen Dateien vor unbeabsichtigtem oder bösartigem Zugriff.
Skripte müssen ausführbar sein (`x`), Konfigurationsdateien mit Passwörtern
sollten nur vom Eigentümer lesbar sein (`600`), und öffentliche Webinhalte
benötigen Leserechte für alle (`644` oder `755`).
