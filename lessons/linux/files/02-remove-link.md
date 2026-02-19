---
title: "Loeschen und Verlinken"
level: files
order: 2
points: 15

setup:
  - cmd: "mkdir -p alt/daten neu && echo 'wichtige daten' > alt/daten/config.txt && echo 'temporaer' > alt/temp.txt && echo 'log eintrag' > alt/debug.log"

task: |
  Lerne, wie man Dateien loescht und symbolische Links erstellt.

  1. Loesche die Datei `alt/temp.txt` mit `rm`
  2. Loesche die Datei `alt/debug.log` mit `rm`
  3. Erstelle einen symbolischen Link `neu/config-link`, der auf `../alt/daten/config.txt` zeigt, mit `ln -s`

hints:
  - "`rm alt/temp.txt` loescht die Datei unwiderruflich — es gibt keinen Papierkorb"
  - "`rm alt/debug.log` loescht die zweite Datei"
  - "`ln -s ../alt/daten/config.txt neu/config-link` erstellt den symbolischen Link"
  - "Bei `ln -s` kommt zuerst das Ziel, dann der Name des Links"
  - "Der Pfad `../alt/daten/config.txt` ist relativ zum Ort des Links (`neu/`)"

solution: |
  rm alt/temp.txt
  rm alt/debug.log
  ln -s ../alt/daten/config.txt neu/config-link

validation:
  - type: file_not_exists
    path: "alt/temp.txt"
  - type: file_not_exists
    path: "alt/debug.log"
  - type: symlink_target
    path: "neu/config-link"
    expected: "../alt/daten/config.txt"
---

## Loeschen und Verlinken

Das Loeschen von Dateien und das Erstellen von symbolischen Links sind wichtige Werkzeuge fuer die Organisation eines Dateisystems.

### `rm` — Dateien loeschen

`rm` loescht Dateien dauerhaft. Es gibt keinen Papierkorb — einmal geloescht, ist die Datei weg.

| Befehl          | Bedeutung                                              |
|-----------------|--------------------------------------------------------|
| `rm datei.txt`  | Loescht eine einzelne Datei                            |
| `rm -r ordner/` | Loescht ein Verzeichnis rekursiv mit allem Inhalt      |
| `rm -i datei`   | Fragt vor dem Loeschen nach Bestaetigung               |

### `rmdir` — Leere Verzeichnisse loeschen

`rmdir` loescht nur leere Verzeichnisse. Ist das Verzeichnis nicht leer, schlaegt der Befehl fehl:

```
$ rmdir leeres-verz/       # Funktioniert
$ rmdir volles-verz/       # Fehler: Verzeichnis nicht leer
$ rm -r volles-verz/       # Loescht alles rekursiv
```

### `ln -s` — Symbolische Links erstellen

Ein symbolischer Link (Symlink) ist wie eine Verknuepfung: Er zeigt auf eine andere Datei oder ein anderes Verzeichnis. Aendert man die Originaldatei, sieht man die Aenderung auch ueber den Link.

```
$ ln -s /pfad/zum/ziel name-des-links
```

**Wichtig:** Zuerst kommt das Ziel, dann der Name des Links.

```
$ ln -s ../original.txt link.txt
$ ls -la
lrwxr-xr-x  1 user group  13 Feb 19 10:00 link.txt -> ../original.txt
```

### Symlinks vs. Hardlinks

| Eigenschaft        | Symbolischer Link (`ln -s`) | Hardlink (`ln`)            |
|--------------------|-----------------------------|----------------------------|
| Zeigt auf          | Pfad (Name)                 | Inode (Daten direkt)       |
| Verzeichnisse      | Moeglich                    | Nicht moeglich             |
| Anderes Dateisystem| Moeglich                    | Nicht moeglich             |
| Original geloescht | Link ist kaputt             | Daten bleiben erhalten     |

In der Praxis werden fast immer symbolische Links (`ln -s`) verwendet.
