---
title: "Signale und Hintergrundprozesse"
level: processes
order: 2
points: 20

setup:
  - cmd: "printf '#!/bin/bash\\nwhile true; do echo running >> /exercise/bg-output.txt; sleep 2; done\\n' > worker.sh && chmod +x worker.sh"

task: |
  Lerne, Prozesse im Hintergrund zu starten und mit Signalen zu steuern.

  Aufgaben:
  1. Starte worker.sh im Hintergrund: ./worker.sh &
     Das & am Ende schickt den Prozess in den Hintergrund.

  2. Warte 3 Sekunden damit der Worker etwas schreibt: sleep 3

  3. Finde die PID des worker.sh-Prozesses mit jobs -l oder ps aux | grep worker.
     Speichere die PID in "worker-pid.txt":  echo $! > worker-pid.txt
     (Tipp: $! ist die PID des zuletzt gestarteten Hintergrundprozesses)

  4. Beende den Prozess: kill $(cat worker-pid.txt)

  5. Verifiziere mit jobs dass keine Hintergrundprozesse mehr laufen.

hints:
  - "Programm im Hintergrund starten: ./worker.sh &"
  - "$! enthaelt die PID des letzten Hintergrundprozesses: echo $! > worker-pid.txt"
  - "jobs -l zeigt alle Hintergrundprozesse mit PID an"
  - "ps aux | grep worker findet den Prozess falls $! nicht mehr verfuegbar ist"
  - "Prozess beenden: kill PIDNUMMER oder kill $(cat worker-pid.txt)"
  - "Vollstaendige Loesung: ./worker.sh & && sleep 3 && echo $! > worker-pid.txt && kill $(cat worker-pid.txt)"

solution: |
  ./worker.sh &
  sleep 3
  echo $! > worker-pid.txt
  kill $(cat worker-pid.txt)
  sleep 1

validation:
  - type: file_exists
    path: worker-pid.txt
  - type: file_exists
    path: bg-output.txt
---

## Signale und Hintergrundprozesse

Linux ermöglicht es, Prozesse im Hintergrund laufen zu lassen und sie über
Signale zu steuern. Dies ist fundamental für die Arbeit mit Servern und
lang laufenden Prozessen.

### Hintergrundprozesse starten

Mit `&` am Ende eines Befehls wird er im Hintergrund gestartet:

```bash
./langzeit.sh &              # Im Hintergrund starten
sleep 100 &                  # sleep im Hintergrund
```

Die Shell zeigt die Job-Nummer und PID an: `[1] 12345`

### jobs - Hintergrundprozesse verwalten

```bash
jobs                         # Alle Hintergrundprozesse
jobs -l                      # Mit PID anzeigen
```

### Prozesse in Vorder-/Hintergrund verschieben

```bash
Ctrl+Z                       # Aktuellen Prozess pausieren (SIGTSTP)
bg                           # Pausierten Prozess im Hintergrund fortsetzen
fg                           # Hintergrundprozess in den Vordergrund holen
fg %2                        # Job-Nummer 2 in den Vordergrund
```

### Signale und kill

Signale sind Nachrichten an Prozesse:

```bash
kill PID                     # SIGTERM senden (hoeflich beenden)
kill -9 PID                  # SIGKILL senden (sofort beenden)
kill -15 PID                 # SIGTERM explizit
kill -SIGTERM PID            # Mit Signalname
killall firefox              # Alle firefox-Prozesse beenden
pkill -f worker.sh           # Nach Prozessname suchen und beenden
```

### Wichtige Signale

| Signal   | Nummer | Bedeutung                          |
|----------|--------|------------------------------------|
| SIGTERM  | 15     | Bitte beenden (kann ignoriert werden) |
| SIGKILL  | 9      | Sofort beenden (nicht ignorierbar) |
| SIGINT   | 2      | Interrupt (wie Ctrl+C)             |
| SIGTSTP  | 20     | Pause (wie Ctrl+Z)                 |
| SIGHUP   | 1      | Konfiguration neu laden            |
| SIGCONT  | 18     | Pausierten Prozess fortsetzen      |

### Tastenkuerzel fuer Prozesse

- `Ctrl+C` – Prozess beenden (SIGINT)
- `Ctrl+Z` – Prozess pausieren (SIGTSTP)
- `Ctrl+D` – Eingabe beenden (kein Signal, schliesst stdin)

### Spezielle Shell-Variablen fuer Prozesse

```bash
echo $$              # PID der aktuellen Shell
echo $!              # PID des letzten Hintergrundprozesses
echo $?              # Exit-Code des letzten Befehls
```

### Prozesse beim Logout weiterlaufen lassen

Normalerweise werden Hintergrundprozesse beendet wenn man sich ausloggt:

```bash
nohup ./langzeit.sh &        # Ignoriert HUP-Signal beim Logout
disown %1                    # Job aus Shell-Verwaltung entfernen
nohup ./script.sh > ausgabe.log 2>&1 &  # Mit Ausgabe in Datei
```

### screen und tmux

Fuer persistente Sessions gibt es screen und tmux:

```bash
screen -S meinesession       # Neue screen-Session
screen -ls                   # Sessions auflisten
screen -r meinesession       # Session wieder aufnehmen
```
