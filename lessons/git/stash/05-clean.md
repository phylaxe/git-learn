---
title: "Aufräumen mit Clean"
level: stash
order: 5
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'Projektdatei' > main.py"
  - cmd: "echo '*.log' > .gitignore"
  - cmd: "git add main.py .gitignore"
  - cmd: "git commit -m 'Projekt initialisiert'"
  - cmd: "echo 'temporär' > temp1.txt"
  - cmd: "echo 'auch temporär' > temp2.txt"
  - cmd: "echo 'Build-Log' > build.log"

task: |
  Dein Arbeitsverzeichnis ist voller Dateien, die nicht ins Repository gehören:
  temp1.txt, temp2.txt und build.log.

  Die .gitignore ist so konfiguriert, dass *.log-Dateien ignoriert werden.

  Entferne alle unverfolgten Dateien (ausser den ignorierten) mit `git clean`:

  1. Prüfe zuerst, was entfernt würde: `git clean -n`
  2. Führe das Aufräumen durch: `git clean -f`

  Am Ende sollen temp1.txt und temp2.txt verschwunden sein,
  aber build.log soll noch vorhanden sein (weil sie ignoriert wird).

hints:
  - "Mit `git clean -n` (Dry Run) siehst du, was entfernt würde, ohne etwas zu löschen"
  - "Mit `git clean -f` werden unverfolgte Dateien tatsächlich gelöscht – ignorierte Dateien bleiben"
  - "git clean -n && git clean -f"

solution: |
  git clean -n
  git clean -f

validation:
  - type: file_not_exists
    path: "temp1.txt"
  - type: file_not_exists
    path: "temp2.txt"
  - type: file_exists
    path: "build.log"
  - type: working_tree_clean
    expected: true
---

## Aufräumen mit Clean

Im Laufe der Entwicklung sammeln sich oft Dateien an, die nicht ins
Repository gehören: temporäre Dateien, Build-Artefakte, Editor-Backups.
Während `git checkout` und `git restore` nur **verfolgte** Dateien
zurücksetzen können, kümmert sich `git clean` um die **unverfolgten**.

### git clean Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `git clean -n` | Dry Run: zeigt an, was gelöscht würde |
| `git clean -f` | Unverfolgte Dateien löschen |
| `git clean -fd` | Unverfolgte Dateien und Verzeichnisse löschen |
| `git clean -fx` | Auch ignorierte Dateien löschen |
| `git clean -fX` | NUR ignorierte Dateien löschen |

### Sicherheitsnetz

Git verlangt bei `clean` immer das `-f` Flag (force) – das ist Absicht.
Gelöschte unverfolgte Dateien sind **unwiderruflich verloren**, da sie
nie in der Git-Geschichte waren.

Deshalb: **Immer zuerst `git clean -n` ausführen!**

### Zusammenspiel mit .gitignore

Standardmässig respektiert `git clean` die `.gitignore`-Datei:
- Dateien, die von `.gitignore` erfasst werden, bleiben **unangetastet**
- Nur mit `-x` werden auch ignorierte Dateien entfernt
- Mit `-X` (grosses X) werden **nur** ignorierte Dateien entfernt

### Was du lernst
- Wie du mit `git clean` unverfolgte Dateien entfernst
- Warum der Dry Run (`-n`) wichtig ist
- Wie `.gitignore` und `git clean` zusammenspielen
