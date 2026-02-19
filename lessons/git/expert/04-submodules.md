---
title: "Submodules"
level: expert
order: 4
points: 15

setup:
  - cmd: "git init"
  - cmd: "echo '# Hauptprojekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Hauptprojekt erstellt'"
  - cmd: "git init --bare ../library.git"
  - cmd: "git clone ../library.git ../library-work && cd ../library-work && git config user.email 'lib@test.ch' && git config user.name 'Lib' && echo 'library v1' > lib.txt && git add . && git commit -m 'Library v1' && git push origin master"

task: |
  Du hast ein Hauptprojekt mit einem Commit. Ausserdem existiert ein separates
  Git-Repository unter `../library.git`, das eine wiederverwendbare Bibliothek enthält.

  Statt den Code der Bibliothek zu kopieren, sollst du sie als **Submodul** einbinden.
  So bleibt die Bibliothek ein eigenständiges Repository, das du jederzeit aktualisieren kannst.

  1. Füge das Repository `../library.git` als Submodul im Ordner `lib` hinzu
  2. Committe die Änderungen mit der Nachricht "Library als Submodul hinzugefügt"

hints:
  - "Mit `git submodule add <url> <pfad>` fügst du ein Submodul hinzu"
  - "Nach dem Hinzufügen musst du die neuen Dateien (`.gitmodules` und den Submodul-Ordner) committen"
  - |
    git submodule add ../library.git lib
    git commit -m 'Library als Submodul hinzugefügt'

solution: |
  git submodule add ../library.git lib
  git commit -m "Library als Submodul hinzugefügt"

validation:
  - type: file_exists
    path: ".gitmodules"
  - type: file_exists
    path: "lib/lib.txt"
  - type: working_tree_clean
    expected: true
---

## Submodules

Wenn dein Projekt von einer externen Bibliothek oder einem gemeinsam genutzten
Code-Repository abhängt, kannst du dieses als **Submodul** einbinden. Ein
Submodul ist ein Git-Repository innerhalb eines anderen Git-Repositories.

### Submodul hinzufügen

```bash
# Externes Repository als Submodul einbinden
git submodule add https://github.com/example/library.git lib

# Die Änderungen committen
git add .
git commit -m "Library als Submodul hinzugefügt"
```

Nach dem Hinzufügen entstehen zwei Änderungen:
- Eine `.gitmodules`-Datei mit der Konfiguration
- Ein spezieller Eintrag im Git-Index für den Submodul-Ordner

### Submodule klonen

Wenn jemand dein Repository klont, sind die Submodul-Ordner zunächst leer:

```bash
# Repository klonen und Submodule initialisieren
git clone --recurse-submodules <url>

# Oder nachträglich:
git submodule init
git submodule update
```

### Submodule aktualisieren

```bash
# Alle Submodule auf den neuesten Stand bringen
git submodule update --remote

# Änderungen committen
git add lib
git commit -m "Library aktualisiert"
```

### Wichtig zu wissen

- Das Hauptprojekt speichert einen **festen Commit-Hash** des Submoduls
- Submodule werden nicht automatisch aktualisiert
- Jedes Submodul ist ein eigenständiges Repository mit eigener Geschichte
- Submodule können verschachtelt sein (Submodule in Submodulen)

### Alternativen zu Submodules

- **git subtree**: Integriert den Code direkt (kein separates Repository nötig)
- **Paketmanager**: npm, pip, etc. für Bibliotheks-Abhängigkeiten
- **Monorepo**: Alles in einem grossen Repository

### Was du lernst
- Wie du mit `git submodule add` externe Repositories einbindest
- Wie Submodule funktionieren und welche Dateien sie erzeugen
- Wie du Submodule klonst und aktualisierst
