---
title: "Den Überblick behalten"
level: navigation
order: 3
points: 15

setup:
  - cmd: "mkdir -p src/components src/utils src/api tests/unit tests/integration docs"
  - cmd: "touch src/components/Button.tsx src/components/Header.tsx src/utils/helpers.ts src/api/routes.ts tests/unit/test_button.py tests/integration/test_api.py docs/README.md"

task: |
  Verschaffe dir einen Überblick über die Projektstruktur und finde alle TypeScript-Dateien.

  1. Zeige die Verzeichnisstruktur mit `tree` an
  2. Finde alle `.ts` und `.tsx` Dateien mit `find`
  3. Leite die Ausgabe in eine Datei namens `typescript-files.txt` um:

     find . -name "*.ts" -o -name "*.tsx" > typescript-files.txt

hints:
  - "`tree` zeigt den Verzeichnisbaum übersichtlich an (ggf. mit `sudo apt install tree` installieren)"
  - "`find . -name \"*.ts\"` sucht alle Dateien mit der Endung `.ts` ab dem aktuellen Verzeichnis"
  - "Mit `-o` (oder) kannst du mehrere Suchmuster kombinieren: `find . -name \"*.ts\" -o -name \"*.tsx\"`"
  - "`>` leitet die Ausgabe in eine Datei um (überschreibt die Datei)"
  - "`>>` hängt die Ausgabe an eine bestehende Datei an"

solution: |
  tree
  find . -name "*.ts" -o -name "*.tsx" > typescript-files.txt

validation:
  - type: file_exists
    path: "typescript-files.txt"
  - type: file_content
    path: "typescript-files.txt"
    contains: "Button.tsx"
---

## Den Überblick behalten

In größeren Projekten ist es wichtig, sich schnell einen Überblick über die Dateistruktur zu verschaffen und gezielt nach Dateien suchen zu können.

### `tree` — Verzeichnisbaum anzeigen

`tree` visualisiert die Verzeichnisstruktur als Baumdiagramm:

```
$ tree
.
├── docs
│   └── README.md
├── src
│   ├── api
│   │   └── routes.ts
│   ├── components
│   │   ├── Button.tsx
│   │   └── Header.tsx
│   └── utils
│       └── helpers.ts
└── tests
    ├── integration
    │   └── test_api.py
    └── unit
        └── test_button.py
```

Nützliche Optionen:

| Befehl          | Beschreibung                              |
|-----------------|-------------------------------------------|
| `tree`          | Komplette Struktur anzeigen               |
| `tree -L 2`     | Nur 2 Ebenen tief anzeigen               |
| `tree -a`       | Auch versteckte Dateien anzeigen          |
| `tree -d`       | Nur Verzeichnisse anzeigen               |
| `tree -I node_modules` | Verzeichnis ausschließen          |

### `find` — Dateien suchen

`find` durchsucht das Dateisystem nach Dateien und Verzeichnissen:

```
find [startpfad] [optionen] [suchmuster]
```

Häufige Anwendungsbeispiele:

```bash
find . -name "*.py"           # Alle Python-Dateien
find . -name "*.ts" -o -name "*.tsx"  # TypeScript-Dateien (oder)
find . -type d                # Nur Verzeichnisse
find . -type f -size +1M      # Dateien größer als 1 MB
find . -newer README.md       # Dateien neuer als README.md
find . -name "*.log" -delete  # Alle Log-Dateien löschen
```

### Ausgabe umleiten mit `>`

Mit `>` kannst du die Ausgabe eines Befehls in eine Datei schreiben:

```bash
find . -name "*.ts" > typescript-files.txt   # Ergebnis speichern
ls -la >> log.txt                            # An Datei anhängen
```

Das ist besonders nützlich, um Suchergebnisse für spätere Verwendung zu speichern.
