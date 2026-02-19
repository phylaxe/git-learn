---
title: "Wo bin ich?"
level: navigation
order: 1
points: 10

setup:
  - cmd: "mkdir -p projekte/webseite docs"
  - cmd: "touch projekte/webseite/index.html projekte/webseite/style.css docs/notizen.txt README.md"

task: |
  Finde heraus, in welchem Verzeichnis du dich befindest, und liste alle Dateien auf.

  1. Zeige dein aktuelles Verzeichnis an mit `pwd`
  2. Liste alle Dateien inkl. versteckter Dateien auf mit `ls -la`
  3. Gib den aktuellen Pfad mit `check` ab:

     check "/dein/pfad/hier"

hints:
  - "`pwd` steht für \"print working directory\" und zeigt den aktuellen Pfad an"
  - "`ls -la` kombiniert `-l` (Langformat) und `-a` (alle Dateien, auch versteckte)"
  - "Versteckte Dateien beginnen mit einem Punkt, z.B. `.gitignore`"
  - "Der Pfad zum Übungsverzeichnis enthält \"exercise\""

solution: |
  pwd
  ls -la
  check "/tmp/git-learn/exercise"

validation:
  - type: check_answer
    contains: "/exercise"
---

## Wo bin ich?

Das Terminal kennt immer ein aktuelles Arbeitsverzeichnis. Bevor du Dateien erstellst oder bearbeitest, ist es wichtig zu wissen, wo du dich im Dateisystem befindest.

### `pwd` — Print Working Directory

`pwd` gibt den vollständigen Pfad des aktuellen Verzeichnisses aus:

```
$ pwd
/home/benutzername/projekte
```

### `ls` — Dateien auflisten

`ls` zeigt den Inhalt eines Verzeichnisses an. Es gibt verschiedene nützliche Optionen:

| Befehl    | Bedeutung                                          |
|-----------|----------------------------------------------------|
| `ls`      | Einfache Auflistung                                |
| `ls -l`   | Langformat mit Berechtigungen, Größe und Datum     |
| `ls -a`   | Alle Dateien, auch versteckte (beginnen mit `.`)   |
| `ls -la`  | Kombination: Langformat und versteckte Dateien     |
| `ls -lh`  | Langformat mit lesbaren Dateigrößen (KB, MB)       |

### Beispiel: `ls -la`

```
$ ls -la
total 32
drwxr-xr-x  4 user group  128 Feb 19 10:00 .
drwxr-xr-x 12 user group  384 Feb 19 09:55 ..
-rw-r--r--  1 user group    0 Feb 19 10:00 README.md
drwxr-xr-x  3 user group   96 Feb 19 10:00 docs
drwxr-xr-x  3 user group   96 Feb 19 10:00 projekte
```

- `.` steht für das aktuelle Verzeichnis
- `..` steht für das übergeordnete Verzeichnis
- Die erste Spalte zeigt die Dateiberechtigungen (z.B. `drwxr-xr-x` für Verzeichnisse)
