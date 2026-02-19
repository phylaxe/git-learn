---
title: "Berechtigungen aendern"
level: permissions
order: 2
points: 15

setup:
  - cmd: "printf '#!/bin/bash\\necho hello\\n' > deploy.sh && echo 'config_key=value' > config.txt && echo 'public info' > public.txt && chmod 644 deploy.sh && chmod 644 config.txt && chmod 644 public.txt"

task: |
  Berechtigungen aendern mit chmod

  Das Uebungsverzeichnis enthaelt drei Dateien, alle mit Berechtigung 644:
    - deploy.sh  — ein Deployment-Skript
    - config.txt — eine Konfigurationsdatei mit sensiblen Daten
    - public.txt — eine oeffentliche Datei

  Setze die Berechtigungen wie folgt:

  Schritt 1: deploy.sh ausfuehrbar machen (Eigentuemer: lesen/schreiben/ausfuehren,
             Gruppe und Andere: lesen/ausfuehren):
    chmod 755 deploy.sh

  Schritt 2: config.txt nur fuer den Eigentuemer lesbar machen
             (Gruppe und Andere: kein Zugriff):
    chmod 600 config.txt

  Schritt 3: public.txt fuer Eigentuemer und Gruppe beschreibbar machen
             (Andere: nur lesen):
    chmod 664 public.txt

  Ueberpruefe das Ergebnis mit:
    ls -l

hints:
  - "chmod aendert Berechtigungen. Syntax: chmod MODUS DATEI — z.B. chmod 755 deploy.sh"
  - "Im Oktal-System steht jede Ziffer fuer eine Dreiergruppe: 4=r, 2=w, 1=x. Addiere die Werte: 7=rwx, 6=rw-, 5=r-x, 4=r--, 0=---"
  - "755 bedeutet: Eigentuemer=7(rwx), Gruppe=5(r-x), Andere=5(r-x). 600 bedeutet: Eigentuemer=6(rw-), Gruppe=0(---), Andere=0(---). 664 bedeutet: Eigentuemer=6(rw-), Gruppe=6(rw-), Andere=4(r--)."
  - "Alternativ zur Zahlen-Methode: chmod u+x deploy.sh (Eigentuemer: x hinzufuegen), chmod go-rw config.txt (Gruppe und Andere: r und w entfernen), chmod g+w public.txt (Gruppe: w hinzufuegen)"

solution: |
  chmod 755 deploy.sh
  chmod 600 config.txt
  chmod 664 public.txt

validation:
  - type: file_permissions
    path: deploy.sh
    expected: "755"
  - type: file_permissions
    path: config.txt
    expected: "600"
  - type: file_permissions
    path: public.txt
    expected: "664"
---

## Berechtigungen aendern mit chmod

Mit `chmod` (change mode) kannst du die Berechtigungen von Dateien und Verzeichnissen
anpassen. Es gibt zwei Schreibweisen: die numerische (Oktal) und die symbolische.

### Numerische Schreibweise (Oktal)

Jede Berechtigung hat einen numerischen Wert:

| Wert | Symbol | Bedeutung |
|------|--------|-----------|
| 4    | r      | Lesen |
| 2    | w      | Schreiben |
| 1    | x      | Ausfuehren |
| 0    | -      | Keine Berechtigung |

Die Werte werden addiert, um eine Ziffer pro Gruppe zu bilden:

```
7 = 4+2+1 = rwx   (lesen + schreiben + ausfuehren)
6 = 4+2+0 = rw-   (lesen + schreiben)
5 = 4+0+1 = r-x   (lesen + ausfuehren)
4 = 4+0+0 = r--   (nur lesen)
0 = 0+0+0 = ---   (kein Zugriff)
```

Eine dreistellige Oktalzahl steht fuer Eigentuemer, Gruppe, Andere:

```bash
chmod 755 script.sh    # rwxr-xr-x
chmod 644 datei.txt    # rw-r--r--
chmod 600 geheim.txt   # rw-------
chmod 777 shared/      # rwxrwxrwx (Vorsicht!)
```

### Symbolische Schreibweise

```bash
chmod u+x script.sh    # Eigentuemer: x hinzufuegen
chmod g-w datei.txt    # Gruppe: w entfernen
chmod o=r public.txt   # Andere: nur r setzen
chmod a+r datei.txt    # Alle (a=all): r hinzufuegen
chmod u+x,go-rw geheim # Kombiniert: u+x und go-rw
```

Kuerzel fuer die Gruppen: `u` = user (Eigentuemer), `g` = group, `o` = others, `a` = all.

### Gaengige Berechtigungsmuster

| Oktal | Symbolisch | Typische Verwendung |
|-------|------------|---------------------|
| 755   | rwxr-xr-x  | Ausfuehrbare Dateien, Verzeichnisse |
| 644   | rw-r--r--  | Normale Textdateien, Webinhalte |
| 600   | rw-------  | Konfigurationsdateien, SSH-Schluessel |
| 664   | rw-rw-r--  | Gemeinsam bearbeitete Dateien |
| 700   | rwx------  | Private Skripte |
| 777   | rwxrwxrwx  | Voller Zugriff (vermeiden!) |

### Rekursive Aenderungen

```bash
chmod -R 755 verzeichnis/   # Alle Dateien und Unterordner aendern
```

Vorsicht: `-R` aendert auch Dateien in Unterverzeichnissen. Oft ist es besser,
Verzeichnisse (755) und Dateien (644) getrennt zu behandeln:

```bash
find . -type d -exec chmod 755 {} +
find . -type f -exec chmod 644 {} +
```
