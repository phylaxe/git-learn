---
title: "Besitzer und Gruppen"
level: permissions
order: 3
points: 15

setup:
  - cmd: "echo 'server config' > server.conf && echo 'app data' > app.dat && mkdir shared"

task: |
  Besitzer und Gruppen verstehen

  Das Übungsverzeichnis enthält:
    - server.conf — eine Server-Konfigurationsdatei
    - app.dat     — eine Anwendungsdatei
    - shared/     — ein gemeinsames Verzeichnis

  Schritt 1: Finde deinen aktuellen Benutzer und deine primäre Gruppe heraus:
    id

  Die Ausgabe sieht etwa so aus:
    uid=0(root) gid=0(root) groups=0(root)

  Schritt 2: Wie heißt deine primäre Gruppe?
  Lies den Gruppennamen aus der Ausgabe von 'id' ab (steht nach 'gid=...' in Klammern).

  Reiche den Gruppennamen ein mit:
    check "root"

  Schritt 3: Erstelle eine Datei im gemeinsamen Verzeichnis:
    echo "Team-Inhalt" > shared/team.txt

hints:
  - "Führe den Befehl 'id' aus. Er zeigt uid (Benutzer-ID), gid (Gruppen-ID) und alle Gruppen an."
  - "Die primäre Gruppe steht nach 'gid=' in der Ausgabe von 'id', z.B. 'gid=0(root)' bedeutet, die Gruppe heißt 'root'."
  - "Erstelle die Datei mit: echo \"Team-Inhalt\" > shared/team.txt — oder mit einem beliebigen anderen Inhalt."
  - "In dieser Übungsumgebung läuft alles als Benutzer root. Daher ist die Antwort auf die Frage nach der Gruppe: root"

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

In Linux hat jede Datei einen **Eigentümer** (owner) und eine **Gruppe** (group).
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
- **gid** — numerische primäre Gruppen-ID und Gruppenname
- **groups** — alle Gruppen, denen der Benutzer angehört

### Eigentümer anzeigen

```bash
ls -l               # Eigentümer und Gruppe in Spalten 3 und 4
stat datei.txt      # Detaillierte Metadaten inklusive uid/gid
```

Beispiel-Ausgabe von `ls -l`:

```
-rw-r--r-- 1 alice devs 512 Jan 15 10:00 datei.txt
              ^^^^^  ^^^
              |      Gruppe
              Eigentümer
```

### Eigentümer ändern mit chown

```bash
chown bob datei.txt            # Eigentümer zu bob ändern
chown bob:devs datei.txt       # Eigentümer und Gruppe ändern
chown :devs datei.txt          # Nur Gruppe ändern
chown -R alice:alice ordner/   # Rekursiv für ganzen Ordner
```

Hinweis: `chown` erfordert in der Regel Root-Rechte (`sudo`), um den Eigentümer
einer Datei zu ändern, die einem anderen Benutzer gehört.

### Gruppe ändern mit chgrp

```bash
chgrp devs datei.txt           # Gruppe zu devs ändern
chgrp -R devs projekt/         # Rekursiv für ganzen Ordner
```

`chgrp` ändert nur die Gruppe. Benutzer können die Gruppe ihrer eigenen Dateien
auf eine Gruppe setzen, der sie selbst angehören.

### Benutzer und Gruppen verwalten

Die Systemdatenbanken für Benutzer und Gruppen:

```bash
cat /etc/passwd    # Alle Benutzer (Name:Passwort:uid:gid:Info:Home:Shell)
cat /etc/group     # Alle Gruppen (Name:Passwort:gid:Mitglieder)
groups             # Eigene Gruppen anzeigen
groups bob         # Gruppen von Benutzer bob anzeigen
```

### Warum sind Eigentümer wichtig?

Das Eigentümer-Konzept ist fundamental für die Linux-Sicherheit:

- **Isolation:** Prozesse laufen als bestimmter Benutzer und können nur auf
  Dateien zugreifen, für die sie berechtigt sind.
- **Dienste:** Webserver (z.B. `www-data`), Datenbanken (`postgres`) und andere
  Dienste laufen als eigene Benutzer ohne Root-Rechte.
- **Zusammenarbeit:** Gruppen erlauben mehreren Benutzern gemeinsamen Zugriff
  auf Dateien, ohne allen vollen Zugriff zu geben.
- **Sicherheit:** Konfigurationsdateien mit Passwörtern (z.B. SSH-Schlüssel)
  sollten nur dem Eigentümer gehören und nur von ihm lesbar sein (`600`).

### Praktisches Beispiel: Webserver-Setup

```bash
# Webdateien gehören root, aber der Webserver-Gruppe zugänglich
chown -R root:www-data /var/www/html/
chmod -R 750 /var/www/html/

# Uploads-Verzeichnis darf vom Webserver beschrieben werden
chown www-data:www-data /var/www/html/uploads/
chmod 755 /var/www/html/uploads/
```
