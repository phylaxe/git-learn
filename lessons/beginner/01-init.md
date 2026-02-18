---
title: "Willkommen in der Zeitmaschine"
level: beginner
order: 1
points: 10

setup:
  - cmd: "git init"

task: |
  Schau dir den Inhalt des .git Ordners an.
  Was siehst du?

hints:
  - "Nutze `ls -la` um versteckte Dateien zu sehen"
  - "Der .git Ordner enthält die gesamte Git-Datenbank"

solution: |
  ls -la .git

validation:
  - type: working_tree_clean
    expected: true
---

## Willkommen in der Zeitmaschine

Jedes Git-Repository beginnt mit `git init`. Dieser Befehl erstellt
einen versteckten `.git` Ordner, der die gesamte Geschichte deines
Projekts speichern wird.

### Was du lernst
- Was `git init` macht
- Was im `.git` Ordner steckt
