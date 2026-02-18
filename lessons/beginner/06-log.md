---
title: "Die Geschichte lesen"
level: beginner
order: 6
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'Erste Datei' > datei1.txt"
  - cmd: "git add datei1.txt"
  - cmd: "git commit -m 'Erste Datei erstellt'"
  - cmd: "echo 'Zweite Datei' > datei2.txt"
  - cmd: "git add datei2.txt"
  - cmd: "git commit -m 'Zweite Datei hinzugefügt'"
  - cmd: "echo 'Dritte Datei' > datei3.txt"
  - cmd: "git add datei3.txt"
  - cmd: "git commit -m 'Dritte Datei hinzugefügt'"

task: |
  Nutze `git log` um die Geschichte deines Repositories anzuzeigen.
  Finde die Commit-Nachricht des zweiten Commits.
  Übermittle sie mit: check "die commit nachricht"
  Probiere auch `git log --oneline` für eine kompakte Ansicht.

hints:
  - "Mit `git log` siehst du alle Commits mit Details"
  - "Mit `git log --oneline` bekommst du eine kompakte Übersicht"
  - "Der zweite Commit hat die Nachricht 'Zweite Datei hinzugefügt'"

solution: |
  git log --oneline
  check "Zweite Datei hinzugefügt"

validation:
  - type: check_answer
    contains: "Zweite Datei"
---

## Die Geschichte lesen

Mit `git log` kannst du die gesamte Geschichte deines Repositories
anzeigen. Jeder Eintrag zeigt den Commit-Hash, den Autor, das Datum
und die Commit-Nachricht.

Für eine kompaktere Ansicht gibt es `git log --oneline`, das jeden
Commit in einer einzigen Zeile zusammenfasst.

### Was du lernst
- Wie du mit `git log` die Commit-Geschichte anzeigst
- Wie `git log --oneline` eine kompakte Übersicht liefert
- Wie du dich in der Geschichte orientierst
