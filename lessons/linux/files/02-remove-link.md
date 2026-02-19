---
title: "Löschen und Verlinken"
level: files
order: 2
points: 15

setup:
  - cmd: "mkdir -p alt/daten neu && echo 'wichtige daten' > alt/daten/config.txt && echo 'temporaer' > alt/temp.txt && echo 'log eintrag' > alt/debug.log"

task: |
  Lerne, wie man Dateien löscht und symbolische Links erstellt.
  Führe alle Befehle im Übungsverzeichnis (/exercise) aus.

  1. Lösche die Datei `alt/temp.txt` mit `rm`
  2. Lösche die Datei `alt/debug.log` mit `rm`
  3. Erstelle einen symbolischen Link:
     ln -s ../alt/daten/config.txt neu/config-link
     (Der relative Pfad wird vom Ort des Links aus aufgelöst:
      neu/ → .. → /exercise → alt/daten/config.txt)

hints:
  - "`rm alt/temp.txt` löscht die Datei unwiderruflich — es gibt keinen Papierkorb"
  - "`rm alt/debug.log` löscht die zweite Datei"
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

## Löschen und Verlinken

Das Löschen von Dateien und das Erstellen von symbolischen Links sind wichtige Werkzeuge für die Organisation eines Dateisystems.

### `rm` — Dateien löschen

`rm` löscht Dateien dauerhaft. Es gibt keinen Papierkorb — einmal gelöscht, ist die Datei weg.

| Befehl          | Bedeutung                                              |
|-----------------|--------------------------------------------------------|
| `rm datei.txt`  | Löscht eine einzelne Datei                             |
| `rm -r ordner/` | Löscht ein Verzeichnis rekursiv mit allem Inhalt       |
| `rm -i datei`   | Fragt vor dem Löschen nach Bestätigung                 |

### `rmdir` — Leere Verzeichnisse löschen

`rmdir` löscht nur leere Verzeichnisse. Ist das Verzeichnis nicht leer, schlägt der Befehl fehl:

```
$ rmdir leeres-verz/       # Funktioniert
$ rmdir volles-verz/       # Fehler: Verzeichnis nicht leer
$ rm -r volles-verz/       # Löscht alles rekursiv
```

### `ln -s` — Symbolische Links erstellen

Ein symbolischer Link (Symlink) ist wie eine Verknüpfung: Er zeigt auf eine andere Datei oder ein anderes Verzeichnis. Ändert man die Originaldatei, sieht man die Änderung auch über den Link.

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
| Verzeichnisse      | Möglich                    | Nicht möglich             |
| Anderes Dateisystem| Möglich                    | Nicht möglich             |
| Original gelöscht  | Link ist kaputt             | Daten bleiben erhalten     |

In der Praxis werden fast immer symbolische Links (`ln -s`) verwendet.
