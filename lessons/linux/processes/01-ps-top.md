---
title: "Prozesse beobachten"
level: processes
order: 1
points: 15

setup:
  - cmd: "echo '#!/bin/bash' > langzeit.sh && echo 'while true; do sleep 1; done' >> langzeit.sh && chmod +x langzeit.sh"

task: |
  Prozesse sind laufende Programme auf deinem System. Lerne, sie zu beobachten.

  Aufgaben:
  1. Führe ps aux aus und speichere die komplette Ausgabe in "prozesse.txt".
     Beispiel: ps aux > prozesse.txt

  2. Zähle wie viele Prozesse gerade laufen (ohne die Kopfzeile).
     Reiche die Anzahl mit check ein.
     Beispiel: ps aux | wc -l  (dann 1 abziehen für die Kopfzeile)
     Dann: check "42"  (mit der tatsächlichen Zahl)

hints:
  - "ps aux zeigt alle laufenden Prozesse"
  - "ps aux > prozesse.txt speichert die Ausgabe in eine Datei"
  - "ps aux | wc -l zählt alle Zeilen inklusive Kopfzeile"
  - "Ziehe 1 ab für die Kopfzeile: ps aux | tail -n +2 | wc -l"
  - "Reiche die Anzahl ein: check \"42\" (mit deiner tatsächlichen Zahl)"

solution: |
  ps aux > prozesse.txt
  ps aux | tail -n +2 | wc -l
  check "$(ps aux | tail -n +2 | wc -l | tr -d ' ')"

validation:
  - type: file_exists
    path: prozesse.txt
  - type: file_content
    path: prozesse.txt
    contains: "bash"
---

## Prozesse beobachten

Ein Prozess ist ein laufendes Programm mit eigenem Speicherbereich und einer
eindeutigen Prozess-ID (PID). Linux gibt dir viele Werkzeuge, um Prozesse zu
beobachten und zu verwalten.

### ps - Prozessliste

Der grundlegende Befehl zur Prozessanzeige:

```bash
ps              # Prozesse im aktuellen Terminal
ps aux          # Alle Prozesse aller Benutzer (am nützlichsten)
ps -ef          # Alternative Darstellung
ps aux --sort=-%cpu  # Nach CPU-Auslastung sortiert
ps aux --sort=-%mem  # Nach Speicher sortiert
```

Die Spalten von `ps aux`:
- **USER** – Besitzer des Prozesses
- **PID** – Prozess-ID (eindeutige Nummer)
- **%CPU** – CPU-Auslastung in Prozent
- **%MEM** – Speicherauslastung in Prozent
- **VSZ** – Virtueller Speicher (KB)
- **RSS** – Echter Arbeitsspeicher (KB)
- **STAT** – Prozessstatus (R=Running, S=Sleeping, Z=Zombie, ...)
- **COMMAND** – Name des Programms

### Prozesse suchen

```bash
ps aux | grep firefox         # Firefox-Prozesse finden
ps aux | grep -v grep         # grep selbst ausblenden
pgrep bash                    # PIDs von bash-Prozessen
pgrep -l bash                 # Mit Namen anzeigen
```

### Meine eigene PID

```bash
echo $$                       # PID der aktuellen Shell
echo $PPID                    # PID des Eltern-Prozesses
```

### top und htop - Interaktive Prozessanzeige

`top` zeigt Prozesse in Echtzeit:
```bash
top                           # Interaktive Anzeige (q zum Beenden)
top -u username               # Nur Prozesse eines Benutzers
```

Tastenkürzel in top:
- `q` – Beenden
- `k` – Prozess beenden (kill)
- `M` – Nach Speicher sortieren
- `P` – Nach CPU sortieren
- `u` – Nach Benutzer filtern

`htop` (falls installiert) ist eine modernere Alternative mit Farben und Maus-Unterstützung.

### Das /proc-Dateisystem

Linux stellt Prozessinformationen als Dateien bereit:

```bash
ls /proc/                     # Verzeichnisse für jeden Prozess
cat /proc/$$/status           # Status der aktuellen Shell
cat /proc/$$/cmdline          # Befehl der aktuellen Shell
ls /proc/1/                   # Informationen über Prozess 1 (init/systemd)
```

### Prozessstatus-Codes

- **R** (Running) – Läuft gerade oder wartet auf CPU
- **S** (Sleeping) – Schläft und wartet auf Ereignis
- **D** (Uninterruptible Sleep) – Wartet auf I/O (z.B. Festplatte)
- **Z** (Zombie) – Beendet, aber Elternprozess hat noch nicht abgeholt
- **T** (Stopped) – Durch Signal gestoppt
