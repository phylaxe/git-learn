---
title: "Dateien bearbeiten"
level: beginner
order: 2
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Mein Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"

task: |
  Bearbeite die Datei README.md und füge eine neue Zeile hinzu,
  z.B. "Dies ist mein erstes Projekt".
  Führe danach `git status` aus und beobachte, was Git dir anzeigt.
  Die Datei soll verändert, aber NICHT gestaged sein.

hints:
  - "Öffne README.md mit einem Editor oder nutze `echo`"
  - "Mit `echo 'neuer Text' >> README.md` kannst du Text anhängen"
  - "echo 'Dies ist mein erstes Projekt' >> README.md"

solution: |
  echo 'Dies ist mein erstes Projekt' >> README.md

validation:
  - type: file_content
    path: README.md
    contains: "Projekt"
  - type: working_tree_clean
    expected: false
  - type: staging_area_empty
    expected: true
---

## Dateien bearbeiten

Wenn du eine Datei in deinem Repository veränderst, erkennt Git das
sofort. Mit `git status` kannst du jederzeit sehen, welche Dateien
verändert wurden.

Git unterscheidet dabei zwischen:
- **Untracked**: Neue Dateien, die Git noch nicht kennt
- **Modified**: Bekannte Dateien, die verändert wurden
- **Staged**: Dateien, die für den nächsten Commit vorgemerkt sind

### Was du lernst
- Wie Git Änderungen im Working Directory erkennt
- Was `git status` dir anzeigt
- Den Unterschied zwischen tracked und modified Dateien
