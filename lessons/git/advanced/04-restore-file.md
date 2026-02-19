---
title: "Dateien aus der Vergangenheit"
level: advanced
order: 4
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo 'version=1' > config.txt"
  - cmd: "git add config.txt"
  - cmd: "git commit -m 'Konfiguration v1'"
  - cmd: "echo 'version=2' > config.txt"
  - cmd: "git add config.txt"
  - cmd: "git commit -m 'Konfiguration v2'"

task: |
  Die Datei `config.txt` wurde im letzten Commit auf `version=2` aktualisiert.
  Du stellst aber fest, dass die alte Version besser war.

  Stelle die Datei `config.txt` aus dem vorherigen Commit (HEAD~1) wieder her
  und erstelle einen neuen Commit mit der Nachricht "Konfiguration auf v1 zurückgesetzt".

  Am Ende soll das Repository 3 Commits haben und config.txt wieder "version=1" enthalten.

hints:
  - "Mit `git restore --source <commit> <datei>` kannst du eine Datei aus einem früheren Commit wiederherstellen"
  - "HEAD~1 verweist auf den Commit vor dem aktuellen – also auf die erste Version der Datei"
  - "git restore --source HEAD~1 config.txt && git add config.txt && git commit -m 'Konfiguration auf v1 zurückgesetzt'"

solution: |
  git restore --source HEAD~1 config.txt
  git add config.txt
  git commit -m "Konfiguration auf v1 zurückgesetzt"

validation:
  - type: file_content
    path: "config.txt"
    contains: "version=1"
  - type: commit_count
    expected: 3
  - type: working_tree_clean
    expected: true
---

## Dateien aus der Vergangenheit

Manchmal möchtest du nicht den gesamten Projekt-Stand zurücksetzen, sondern
nur eine einzelne Datei auf eine ältere Version bringen. Git macht das
einfach, denn jede Version jeder Datei ist in der Geschichte gespeichert.

### git restore --source

Der moderne Befehl dafür ist `git restore --source`:

```bash
# Eine Datei aus einem bestimmten Commit wiederherstellen
git restore --source HEAD~1 config.txt

# Aus einem bestimmten Commit-Hash
git restore --source a1b2c3d config.txt

# Aus einem Tag
git restore --source v1.0 config.txt
```

### Der ältere Weg: git checkout

Vor Git 2.23 wurde dafür `git checkout` verwendet:

```bash
# Ältere Syntax (funktioniert immer noch)
git checkout HEAD~1 -- config.txt
```

### Wichtig zu wissen

- Die wiederhergestellte Datei landet im **Arbeitsverzeichnis** und in der **Staging Area**
- Du musst danach noch einen **Commit** erstellen, um die Änderung zu speichern
- Der originale Commit mit der neuen Version bleibt in der Geschichte erhalten
- Das ist sicherer als `git reset`, weil keine Geschichte verloren geht

### Was du lernst
- Wie du mit `git restore --source` einzelne Dateien wiederherstellst
- Den Unterschied zwischen git restore und git reset
- Warum das Wiederherstellen einzelner Dateien sicherer ist als ein Reset
