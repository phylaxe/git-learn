---
title: "Tags & Releases"
level: remotes
order: 4
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo 'Version 0.1' > app.txt"
  - cmd: "git add app.txt"
  - cmd: "git commit -m 'Erste Version'"
  - cmd: "echo 'Version 0.5' > app.txt"
  - cmd: "git add app.txt"
  - cmd: "git commit -m 'Zweite Version'"
  - cmd: "echo 'Version 1.0' > app.txt"
  - cmd: "git add app.txt"
  - cmd: "git commit -m 'Stabile Version'"

task: |
  Das Repository enthält drei Commits. Du sollst nun zwei Tags erstellen:

  1. Erstelle einen **leichtgewichtigen Tag** `v1.0` auf dem **ersten** Commit
     (nutze `git log --oneline` um den Hash zu finden)
  2. Erstelle einen **annotierten Tag** `v2.0` auf dem aktuellen HEAD
     mit der Nachricht "Release v2.0"

hints:
  - "Mit `git log --oneline` siehst du alle Commits und ihre Hashes"
  - "Leichtgewichtiger Tag: `git tag v1.0 <commit-hash>` – Annotierter Tag: `git tag -a v2.0 -m 'Nachricht'`"
  - "Finde den Hash des ersten Commits und nutze: `git tag v1.0 <hash>` und `git tag -a v2.0 -m 'Release v2.0'`"

solution: |
  git log --oneline
  git tag v1.0 <hash-des-ersten-commits>
  git tag -a v2.0 -m "Release v2.0"

validation:
  - type: tag_exists
    name: "v1.0"
  - type: tag_exists
    name: "v2.0"
---

## Tags & Releases

Tags sind benannte Markierungen für bestimmte Commits. Sie werden typischerweise
für Releases und Versionen verwendet – also für Punkte in der Geschichte, die
besonders wichtig sind.

### Arten von Tags

Es gibt zwei Arten von Tags:

**Leichtgewichtige Tags** – einfache Zeiger auf einen Commit:
```bash
# Tag auf aktuellem HEAD
git tag v1.0

# Tag auf einem bestimmten Commit
git tag v1.0 abc1234
```

**Annotierte Tags** – enthalten zusätzliche Metadaten (Autor, Datum, Nachricht):
```bash
git tag -a v2.0 -m "Release v2.0"
```

Annotierte Tags sind die empfohlene Variante für Releases, da sie mehr
Informationen enthalten.

### Tags verwalten

```bash
# Alle Tags auflisten
git tag

# Tag-Details anzeigen
git show v2.0

# Tag löschen
git tag -d v1.0

# Tags zum Remote pushen
git push origin v2.0

# Alle Tags zum Remote pushen
git push origin --tags
```

### Tags und Releases

Auf Plattformen wie GitHub werden annotierte Tags automatisch als
**Releases** angezeigt. Das ist der Standard-Workflow für Veröffentlichungen:

1. Code stabilisieren und testen
2. Annotierten Tag erstellen: `git tag -a v1.0 -m "Release 1.0"`
3. Tag pushen: `git push origin v1.0`

### Was du lernst
- Den Unterschied zwischen leichtgewichtigen und annotierten Tags
- Wie du Tags erstellst und auf bestimmte Commits setzt
- Wie Tags für Releases verwendet werden
