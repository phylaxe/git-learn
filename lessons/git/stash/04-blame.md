---
title: "Schuldfrage"
level: stash
order: 4
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'host=localhost' > config.txt"
  - cmd: "git add config.txt"
  - cmd: "git commit -m 'Server konfiguriert'"
  - cmd: "printf 'host=localhost\\nport=8080\\n' > config.txt"
  - cmd: "git add config.txt"
  - cmd: "git commit -m 'Port hinzugefügt'"
  - cmd: "printf 'host=localhost\\nport=8080\\ndebug=true\\n' > config.txt"
  - cmd: "git add config.txt"
  - cmd: "git commit -m 'Debug aktiviert'"

task: |
  Die Datei config.txt wurde über drei Commits hinweg aufgebaut.
  Jede Zeile wurde in einem anderen Commit hinzugefügt.

  Nutze `git blame config.txt`, um herauszufinden, welcher Commit die
  Zeile `port=8080` hinzugefügt hat.

  Übermittle die Commit-Nachricht dieses Commits mit `check`.

hints:
  - "Mit `git blame <datei>` siehst du für jede Zeile, welcher Commit sie zuletzt geändert hat"
  - "Die Ausgabe zeigt pro Zeile: Commit-Hash, Autor, Datum und den Inhalt"
  - "Suche die Zeile mit `port=8080` in der blame-Ausgabe. Die Commit-Nachricht lautet 'Port hinzugefügt'"

solution: |
  git blame config.txt
  check "Port hinzugefügt"

validation:
  - type: check_answer
    contains: "Port hinzugefügt"
---

## Schuldfrage

Wer hat diese Zeile geschrieben? Wann wurde sie geändert? Und warum?
Diese Fragen stellen sich Entwickler täglich. `git blame` liefert die
Antworten.

### Was git blame zeigt

`git blame` annotiert jede Zeile einer Datei mit dem Commit, der sie
zuletzt verändert hat:

```
a1b2c3d4 (Max Muster 2024-01-15 10:30:00 +0100 1) host=localhost
e5f6g7h8 (Max Muster 2024-01-16 14:20:00 +0100 2) port=8080
i9j0k1l2 (Max Muster 2024-01-17 09:45:00 +0100 3) debug=true
```

Jede Zeile zeigt:
- Den **Commit-Hash** (abgekürzt)
- Den **Autor**
- Das **Datum**
- Die **Zeilennummer**
- Den **Inhalt** der Zeile

### Nützliche Optionen

| Befehl | Beschreibung |
|--------|-------------|
| `git blame datei.txt` | Blame für die gesamte Datei |
| `git blame -L 5,10 datei.txt` | Nur Zeilen 5 bis 10 anzeigen |
| `git blame -w datei.txt` | Whitespace-Änderungen ignorieren |

### Wann ist blame nützlich?

- Du findest eine **fragwürdige Codezeile** und willst wissen, warum sie so ist
- Du suchst den **richtigen Ansprechpartner** für einen bestimmten Code-Abschnitt
- Du willst den **Kontext** einer Änderung verstehen (dann: `git show <hash>`)

### Was du lernst
- Wie du mit `git blame` den Ursprung jeder Zeile nachverfolgst
- Wie du die blame-Ausgabe liest und interpretierst
- Wann `git blame` im Entwickleralltag hilfreich ist
