---
title: "Besitzer und Gruppen"
level: permissions
order: 3
points: 15

setup:
  - cmd: "echo 'server config' > server.conf && echo 'app data' > app.dat && mkdir shared"

task: |
  Besitzer und Gruppen verstehen

  Das Uebungsverzeichnis enthaelt:
    - server.conf — eine Server-Konfigurationsdatei
    - app.dat     — eine Anwendungsdatei
    - shared/     — ein gemeinsames Verzeichnis

  Schritt 1: Finde deinen aktuellen Benutzer und deine primaere Gruppe heraus:
    id

  Die Ausgabe sieht etwa so aus:
    uid=0(root) gid=0(root) groups=0(root)

  Schritt 2: Wie heisst deine primaere Gruppe?
  Lies den Gruppennamen aus der Ausgabe von 'id' ab (steht nach 'gid=...' in Klammern).

  Reiche den Gruppennamen ein mit:
    check "root"

  Schritt 3: Erstelle eine Datei im gemeinsamen Verzeichnis:
    echo "Team-Inhalt" > shared/team.txt

hints:
  - "Fuehre den Befehl 'id' aus. Er zeigt uid (Benutzer-ID), gid (Gruppen-ID) und alle Gruppen an."
  - "Die primaere Gruppe steht nach 'gid=' in der Ausgabe von 'id', z.B. 'gid=0(root)' bedeutet, die Gruppe heisst 'root'."
  - "Erstelle die Datei mit: echo \"Team-Inhalt\" > shared/team.txt — oder mit einem beliebigen anderen Inhalt."
  - "In dieser Uebungsumgebung laeuft alles als Benutzer root. Daher ist die Antwort auf die Frage nach der Gruppe: root"

solution: |
  id
  check "root"
  echo "Team-Inhalt" > shared/team.txt

validation:
  - type: check_answer
    contains: "root"
  - type: file_exists
    path: shared/team.txt
---

## Besitzer und Gruppen

In Linux hat jede Datei einen **Eigentuemer** (owner) und eine **Gruppe** (group).
Das Berechtigungssystem arbeitet auf Basis dieser Zuordnungen.

### Der id-Befehl

```bash
id
```

Beispielausgabe:

```
uid=1001(alice) gid=1001(alice) groups=1001(alice),27(sudo),1002(devs)
```

- **uid** — numerische Benutzer-ID und Benutzername
- **gid** — numerische primaere Gruppen-ID und Gruppenname
- **groups** — alle Gruppen, denen der Benutzer angehoert

### Eigentuemer anzeigen

```bash
ls -l               # Eigentuemer und Gruppe in Spalten 3 und 4
stat datei.txt      # Detaillierte Metadaten inklusive uid/gid
```

Beispiel-Ausgabe von `ls -l`:

```
-rw-r--r-- 1 alice devs 512 Jan 15 10:00 datei.txt
              ^^^^^  ^^^
              |      Gruppe
              Eigentuemer
```

### Eigentuemer aendern mit chown

```bash
chown bob datei.txt            # Eigentuemer zu bob aendern
chown bob:devs datei.txt       # Eigentuemer und Gruppe aendern
chown :devs datei.txt          # Nur Gruppe aendern
chown -R alice:alice ordner/   # Rekursiv fuer ganzen Ordner
```

Hinweis: `chown` erfordert in der Regel Root-Rechte (`sudo`), um den Eigentuemer
einer Datei zu aendern, die einem anderen Benutzer gehoert.

### Gruppe aendern mit chgrp

```bash
chgrp devs datei.txt           # Gruppe zu devs aendern
chgrp -R devs projekt/         # Rekursiv fuer ganzen Ordner
```

`chgrp` aendert nur die Gruppe. Benutzer koennen die Gruppe ihrer eigenen Dateien
auf eine Gruppe setzen, der sie selbst angehoeren.

### Benutzer und Gruppen verwalten

Die Systemdatenbanken fuer Benutzer und Gruppen:

```bash
cat /etc/passwd    # Alle Benutzer (Name:Passwort:uid:gid:Info:Home:Shell)
cat /etc/group     # Alle Gruppen (Name:Passwort:gid:Mitglieder)
groups             # Eigene Gruppen anzeigen
groups bob         # Gruppen von Benutzer bob anzeigen
```

### Warum sind Eigentuemer wichtig?

Das Eigentuemer-Konzept ist fundamental fuer die Linux-Sicherheit:

- **Isolation:** Prozesse laufen als bestimmter Benutzer und koennen nur auf
  Dateien zugreifen, fuer die sie berechtigt sind.
- **Dienste:** Webserver (z.B. `www-data`), Datenbanken (`postgres`) und andere
  Dienste laufen als eigene Benutzer ohne Root-Rechte.
- **Zusammenarbeit:** Gruppen erlauben mehreren Benutzern gemeinsamen Zugriff
  auf Dateien, ohne allen vollen Zugriff zu geben.
- **Sicherheit:** Konfigurationsdateien mit Passwoertern (z.B. SSH-Schluessel)
  sollten nur dem Eigentuemer gehoeren und nur von ihm lesbar sein (`600`).

### Praktisches Beispiel: Webserver-Setup

```bash
# Webdateien gehoeren root, aber der Webserver-Gruppe zugaenglich
chown -R root:www-data /var/www/html/
chmod -R 750 /var/www/html/

# Uploads-Verzeichnis darf vom Webserver beschrieben werden
chown www-data:www-data /var/www/html/uploads/
chmod 755 /var/www/html/uploads/
```
