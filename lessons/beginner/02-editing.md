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
  Bearbeite die Datei README.md und fuege eine neue Zeile hinzu,
  z.B. "Dies ist mein erstes Projekt".
  Fuehre danach `git status` aus und beobachte, was Git dir anzeigt.
  Die Datei soll veraendert, aber NICHT gestaged sein.

hints:
  - "Oeffne README.md mit einem Editor oder nutze `echo`"
  - "Mit `echo 'neuer Text' >> README.md` kannst du Text anhaengen"
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

Wenn du eine Datei in deinem Repository veraenderst, erkennt Git das
sofort. Mit `git status` kannst du jederzeit sehen, welche Dateien
veraendert wurden.

Git unterscheidet dabei zwischen:
- **Untracked**: Neue Dateien, die Git noch nicht kennt
- **Modified**: Bekannte Dateien, die veraendert wurden
- **Staged**: Dateien, die fuer den naechsten Commit vorgemerkt sind

### Was du lernst
- Wie Git Aenderungen im Working Directory erkennt
- Was `git status` dir anzeigt
- Den Unterschied zwischen tracked und modified Dateien
