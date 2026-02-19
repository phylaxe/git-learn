---
title: "Der Rettungsanker"
level: advanced
order: 5
points: 20

setup:
  - cmd: "git init"
  - cmd: "echo 'Erster Inhalt' > datei.txt"
  - cmd: "git add datei.txt"
  - cmd: "git commit -m 'Erster Commit'"
  - cmd: "echo 'Zweiter Inhalt' >> datei.txt"
  - cmd: "git add datei.txt"
  - cmd: "git commit -m 'Zweiter Commit'"
  - cmd: "echo 'Geheime Daten' > geheim.txt"
  - cmd: "git add geheim.txt"
  - cmd: "git commit -m 'Wichtige Daten hinzugefügt'"
  - cmd: "git tag geheim"
  - cmd: "git reset --hard HEAD~1"

task: |
  Jemand hat mit `git reset --hard HEAD~1` den letzten Commit „gelöscht".
  Die Datei `geheim.txt` ist verschwunden und `git log` zeigt nur noch 2 Commits.

  Aber Git vergisst nie wirklich etwas! Nutze `git reflog`, um den verlorenen
  Commit zu finden, und stelle ihn mit `git cherry-pick` oder `git reset` wieder her.

  Am Ende sollen wieder 3 Commits vorhanden sein und die Datei `geheim.txt`
  muss existieren.

hints:
  - "`git reflog` zeigt alle Bewegungen des HEAD-Zeigers – auch nach einem Reset"
  - "Suche im Reflog nach dem Eintrag 'Wichtige Daten hinzugefügt' und notiere den Hash"
  - "git cherry-pick geheim"

solution: |
  git reflog
  git cherry-pick geheim

validation:
  - type: commit_count
    expected: 3
  - type: file_exists
    path: "geheim.txt"
  - type: working_tree_clean
    expected: true
---

## Der Rettungsanker

Hast du schon einmal aus Versehen `git reset --hard` ausgeführt und gedacht,
deine Arbeit sei für immer verloren? Keine Panik! Git hat ein Sicherheitsnetz:
das **Reflog**.

### Was ist das Reflog?

Das Reflog (Reference Log) protokolliert jede Bewegung des HEAD-Zeigers.
Jedes Mal, wenn du commitest, checkoutest, rebasest oder resettest, wird
ein Eintrag im Reflog erstellt.

```bash
# Reflog anzeigen
git reflog

# Beispielausgabe:
# a1b2c3d HEAD@{0}: reset: moving to HEAD~1
# e4f5g6h HEAD@{1}: commit: Wichtige Daten hinzugefügt
# i7j8k9l HEAD@{2}: commit: Zweiter Commit
```

### Verlorene Commits wiederherstellen

Sobald du den Hash des verlorenen Commits im Reflog gefunden hast:

```bash
# Option 1: Cherry-Pick (erstellt neuen Commit)
git cherry-pick <hash>

# Option 2: Reset zurück zum Commit
git reset --hard <hash>

# Option 3: Neuen Branch vom verlorenen Commit erstellen
git branch rettung <hash>
```

### Wichtig zu wissen

- Das Reflog ist **lokal** – es existiert nur auf deinem Rechner
- Einträge werden nach ca. **90 Tagen** automatisch bereinigt
- Solange ein Commit im Reflog steht, wird er **nicht** vom Garbage Collector gelöscht
- `git reflog` ist dein wichtigstes Werkzeug, wenn etwas schiefgeht

### Was du lernst
- Wie du mit `git reflog` verlorene Commits findest
- Verschiedene Wege, gelöschte Commits wiederherzustellen
- Warum Git fast nie Daten wirklich verliert
