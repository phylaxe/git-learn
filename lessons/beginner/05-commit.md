---
title: "Dein erster Commit"
level: beginner
order: 5
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Mein Projekt' > README.md"

task: |
  Erstelle deinen ersten Commit! Fuege zuerst README.md zur Staging Area
  hinzu und erstelle dann einen Commit mit der Nachricht "initial commit".
  Ein Commit ist wie ein Snapshot deines Projekts zu einem bestimmten Zeitpunkt.

hints:
  - "Du brauchst zwei Schritte: zuerst stagen, dann committen"
  - "Zum Stagen: `git add README.md`, zum Committen: `git commit -m 'nachricht'`"
  - "git add README.md && git commit -m 'initial commit'"

solution: |
  git add README.md
  git commit -m "initial commit"

validation:
  - type: commit_count
    expected: 1
  - type: commit_message
    contains: "initial commit"
  - type: working_tree_clean
    expected: true
---

## Dein erster Commit

Ein Commit ist das Herzstuck von Git. Er speichert einen Snapshot
aller gestagten Aenderungen zusammen mit:
- Einer **Commit-Nachricht**, die beschreibt, was geaendert wurde
- Einem **Autor** und **Zeitstempel**
- Einem **Hash** (eine eindeutige ID wie `a1b2c3d`)

Jeder Commit zeigt auf seinen Vorgaenger -- so entsteht die
Geschichte deines Projekts.

### Was du lernst
- Wie du mit `git commit -m "nachricht"` einen Commit erstellst
- Was ein Commit enthaelt (Nachricht, Autor, Hash)
- Den kompletten Workflow: bearbeiten -> stagen -> committen
