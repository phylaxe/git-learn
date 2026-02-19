---
title: "Dateien erstellen und kopieren"
level: files
order: 1
points: 10

setup:
  - cmd: "mkdir -p projekt/src && echo 'Hello World' > projekt/src/main.py"

task: |
  Lerne, wie man Verzeichnisse anlegt, Dateien kopiert und neue leere Dateien erstellt.

  1. Erstelle das Verzeichnis `projekt/backup` mit `mkdir -p`
  2. Kopiere `projekt/src/main.py` nach `projekt/backup/` mit `cp`
  3. Erstelle eine neue leere Datei `projekt/src/utils.py` mit `touch`

hints:
  - "`mkdir -p projekt/backup` erstellt das Verzeichnis inkl. fehlender Elternverzeichnisse"
  - "`cp projekt/src/main.py projekt/backup/` kopiert die Datei in das Zielverzeichnis"
  - "`touch projekt/src/utils.py` erstellt eine neue leere Datei"
  - "Die Reihenfolge der Schritte spielt keine Rolle"

solution: |
  mkdir -p projekt/backup
  cp projekt/src/main.py projekt/backup/
  touch projekt/src/utils.py

validation:
  - type: directory_structure
    expected:
      - "projekt/backup"
      - "projekt/backup/main.py"
      - "projekt/src/utils.py"
---

## Dateien erstellen und kopieren

Das Anlegen von Verzeichnissen und das Kopieren von Dateien sind grundlegende Aufgaben im Terminal. Diese drei Befehle wirst du ständig verwenden.

### `touch` — Leere Datei erstellen

`touch` erstellt eine neue leere Datei oder aktualisiert den Zeitstempel einer bestehenden Datei:

```
$ touch neue-datei.txt
$ touch src/utils.py
```

### `mkdir` — Verzeichnis erstellen

`mkdir` erstellt ein neues Verzeichnis:

```
$ mkdir bilder
```

Mit der Option `-p` werden alle fehlenden Elternverzeichnisse automatisch miterstellt:

```
$ mkdir -p projekte/webseite/css
```

Ohne `-p` würde der Befehl scheitern, wenn `projekte/webseite/` noch nicht existiert.

### `cp` — Dateien kopieren

`cp` kopiert eine Datei von einer Quelle zu einem Ziel:

| Befehl                    | Bedeutung                                        |
|---------------------------|--------------------------------------------------|
| `cp datei.txt kopie.txt`  | Kopiert `datei.txt` als `kopie.txt`              |
| `cp datei.txt verz/`      | Kopiert `datei.txt` in das Verzeichnis `verz/`   |
| `cp -r ordner/ ziel/`     | Kopiert einen ganzen Ordner rekursiv             |

Die Option `-r` (rekursiv) ist notwendig, um Verzeichnisse mit ihrem gesamten Inhalt zu kopieren.

### `mv` — Dateien verschieben oder umbenennen

`mv` funktioniert ähnlich wie `cp`, löscht aber die Quelldatei:

```
$ mv alt.txt neu.txt        # Umbenennen
$ mv datei.txt archiv/      # Verschieben
```
