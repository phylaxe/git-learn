---
title: "Textsuche mit grep"
level: text
order: 2
points: 15

setup:
  - cmd: "mkdir -p src/components src/utils"
  - cmd: "printf 'import React from \"react\";\n\nfunction Button({ onClick, label }) {\n  return <button onClick={onClick}>{label}</button>;\n}\n\nexport default Button;\n' > src/components/Button.jsx"
  - cmd: "printf 'import React from \"react\";\n\nfunction Header({ title }) {\n  return <h1 className=\"header\">{title}</h1>;\n}\n\nexport default Header;\n' > src/components/Header.jsx"
  - cmd: "printf 'export function formatDate(date) {\n  return date.toISOString();\n}\n\nexport function calculateTotal(items) {\n  return items.reduce((sum, item) => sum + item.price, 0);\n}\n' > src/utils/helpers.js"
  - cmd: "printf 'DEBUG: Server started\nINFO: Listening on port 3000\nERROR: Connection refused to database\nINFO: Retrying connection\nDEBUG: Cache cleared\nERROR: Timeout after 30s\nINFO: Connection established\n' > server.log"

task: |
  Du hast eine Logdatei (server.log) und ein Quellcode-Verzeichnis (src/).

  Aufgaben:
  1. Finde alle Zeilen mit "ERROR" in server.log und speichere sie in "errors.txt".
  2. Finde rekursiv alle Dateien in src/, die das Wort "export" enthalten,
     und speichere die Dateinamen in "exports.txt" (verwende grep -rl).

hints:
  - "Mit 'grep Muster datei' suchst du nach einem Muster in einer Datei."
  - "Mit 'grep ERROR server.log > errors.txt' findest und speicherst du alle Fehlerzeilen."
  - "Mit 'grep -r' suchst du rekursiv in Verzeichnissen."
  - "Mit 'grep -l' gibt grep nur die Dateinamen aus (ohne die Trefferzeilen)."
  - "Kombiniert: 'grep -rl export src/ > exports.txt'"

solution: |
  grep ERROR server.log > errors.txt
  grep -rl export src/ > exports.txt

validation:
  - type: file_content
    path: errors.txt
    contains: "ERROR"
  - type: file_content
    path: exports.txt
    contains: "helpers.js"
---

## Textsuche mit grep

`grep` (Global Regular Expression Print) ist eines der mächtigsten Textsuch-Werkzeuge in Linux.

### Grundlegende Verwendung

```bash
grep "Muster" datei.txt
grep ERROR server.log
```

`grep` gibt alle Zeilen aus, die das gesuchte Muster enthalten.

### Nützliche Optionen

| Option | Bedeutung | Beispiel |
|--------|-----------|---------|
| `-i` | Groß-/Kleinschreibung ignorieren | `grep -i error server.log` |
| `-n` | Zeilennummern anzeigen | `grep -n ERROR server.log` |
| `-r` | Rekursiv in Verzeichnissen suchen | `grep -r import src/` |
| `-l` | Nur Dateinamen ausgeben | `grep -l export src/` |
| `-rl` | Rekursiv, nur Dateinamen | `grep -rl export src/` |
| `-c` | Anzahl der Treffer pro Datei | `grep -c ERROR server.log` |
| `-v` | Zeilen ohne Treffer ausgeben | `grep -v DEBUG server.log` |

### Beispiele

Alle Fehlerzeilen in einer Logdatei finden:

```bash
grep ERROR server.log
grep -i error server.log    # auch "error", "Error", usw.
```

Zeilen mit Zeilennummern anzeigen:

```bash
grep -n import src/components/Button.jsx
```

Rekursiv in einem Verzeichnis suchen:

```bash
grep -r "function" src/
grep -rl "export" src/      # nur Dateinamen, die "export" enthalten
```

### Grundlegende reguläre Ausdrücke

`grep` unterstützt reguläre Ausdrücke für flexiblere Suchen:

```bash
grep "^ERROR" server.log    # Zeilen, die mit ERROR beginnen
grep "30s$" server.log      # Zeilen, die mit 30s enden
grep "ERR.R" server.log     # . steht für ein beliebiges Zeichen
```

### Ausgabe umleiten

Suchergebnisse lassen sich direkt in Dateien speichern:

```bash
grep ERROR server.log > errors.txt
grep -rl export src/ > exports.txt
```
