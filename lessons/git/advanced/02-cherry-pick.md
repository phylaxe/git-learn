---
title: "Kirschen pflücken"
level: advanced
order: 2
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo '# Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "echo 'Version 1' > app.txt"
  - cmd: "git add app.txt"
  - cmd: "git commit -m 'App erstellt'"
  - cmd: "git checkout -b feature"
  - cmd: "echo 'Neues Feature' > feature.txt"
  - cmd: "git add feature.txt"
  - cmd: "git commit -m 'Feature hinzugefügt'"
  - cmd: "echo 'bugfix' > hotfix.txt"
  - cmd: "git add hotfix.txt"
  - cmd: "git commit -m 'Kritischen Bug behoben'"
  - cmd: "git tag hotfix"
  - cmd: "git checkout master"

task: |
  Auf dem `feature`-Branch wurde ein kritischer Bugfix gemacht (der Commit
  mit dem Tag `hotfix`). Dieser Fix wird dringend auf `master` gebraucht,
  aber der Rest des Features ist noch nicht fertig.

  Pflücke nur den Hotfix-Commit vom `feature`-Branch auf `master`,
  ohne den gesamten Branch zu mergen. Du sollst am Ende auf `master` bleiben.

hints:
  - "Mit `git cherry-pick` kannst du einzelne Commits auf einen anderen Branch übertragen"
  - "Du kannst einen Tag-Namen statt eines Commit-Hashes verwenden: `git cherry-pick <tag>`"
  - "git cherry-pick hotfix"

solution: |
  git cherry-pick hotfix

validation:
  - type: branch_active
    expected: "master"
  - type: file_exists
    path: "hotfix.txt"
  - type: file_content
    path: "hotfix.txt"
    contains: "bugfix"
---

## Kirschen pflücken

Manchmal brauchst du nur einen bestimmten Commit aus einem anderen Branch –
nicht den ganzen Branch. Genau dafür gibt es `git cherry-pick`. Der Befehl
kopiert einen einzelnen Commit und wendet ihn auf den aktuellen Branch an.

### Wann ist Cherry-Pick nützlich?

- Ein **Bugfix** auf einem Feature-Branch muss dringend auf `master`
- Ein bestimmter Commit soll in einen **Release-Branch** übernommen werden
- Du möchtest gezielt einzelne Änderungen **portieren**

### Wie Cherry-Pick funktioniert

```bash
# Einen bestimmten Commit anwenden
git cherry-pick <commit-hash>

# Einen getaggten Commit anwenden
git cherry-pick <tag-name>

# Mehrere Commits auf einmal
git cherry-pick <hash1> <hash2>
```

### Wichtig zu wissen

- Cherry-Pick erstellt einen **neuen Commit** mit neuem Hash
- Der ursprüngliche Commit auf dem anderen Branch bleibt unverändert
- Bei Konflikten musst du diese manuell lösen, genau wie bei einem Merge
- Übermässiger Einsatz von Cherry-Pick kann zu doppelten Commits führen

### Was du lernst
- Wie du mit `git cherry-pick` einzelne Commits übernimmst
- Den Unterschied zwischen Cherry-Pick und Merge
- Wann Cherry-Pick die richtige Wahl ist
