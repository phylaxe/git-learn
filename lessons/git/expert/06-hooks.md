---
title: "Git Hooks"
level: expert
order: 6
points: 20

setup:
  - cmd: "git init"
  - cmd: "echo 'Projekt Code' > app.py"
  - cmd: "git add app.py"
  - cmd: "git commit -m 'Initial commit'"

task: |
  Git Hooks sind Skripte, die bei bestimmten Git-Aktionen automatisch ausgeführt werden.
  Sie eignen sich hervorragend, um Qualitätschecks zu automatisieren.

  Erstelle einen **pre-commit Hook**, der verhindert, dass Code mit "TODO" committed wird.

  1. Erstelle die Datei `.git/hooks/pre-commit`
  2. Der Hook soll in allen gestagten Dateien nach "TODO" suchen
  3. Falls "TODO" gefunden wird, soll der Commit mit einer Fehlermeldung abgebrochen werden (Exit-Code 1)
  4. Mache den Hook ausführbar mit `chmod +x`

  Tipp: Der Hook muss ein ausführbares Shell-Skript sein.

hints:
  - "Ein Hook ist ein Shell-Skript unter `.git/hooks/` – es braucht eine Shebang-Zeile (`#!/bin/sh`) und muss ausführbar sein"
  - "Mit `git diff --cached --name-only` bekommst du alle gestagten Dateien. Mit `grep -r 'TODO'` kannst du darin suchen"
  - |
    Erstelle die Datei mit:
    printf '#!/bin/sh\nif git diff --cached | grep -q "TODO"; then\n  echo "FEHLER: TODO im Code gefunden!"\n  exit 1\nfi\n' > .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit

solution: |
  printf '#!/bin/sh\nif git diff --cached | grep -q "TODO"; then\n  echo "FEHLER: TODO im Code gefunden!"\n  exit 1\nfi\n' > .git/hooks/pre-commit
  chmod +x .git/hooks/pre-commit

validation:
  - type: hook_exists
    name: "pre-commit"
---

## Git Hooks

Git Hooks sind Skripte, die automatisch bei bestimmten Git-Ereignissen ausgeführt
werden. Sie leben im Ordner `.git/hooks/` und ermöglichen es, Workflows zu
automatisieren und Qualitätsstandards durchzusetzen.

### Arten von Hooks

#### Client-seitige Hooks (lokal)

| Hook | Wird ausgelöst | Typische Nutzung |
|------|----------------|------------------|
| `pre-commit` | Vor jedem Commit | Linting, Tests, TODO-Check |
| `commit-msg` | Nach Eingabe der Nachricht | Commit-Nachricht validieren |
| `pre-push` | Vor dem Push | Vollständige Tests ausführen |
| `post-commit` | Nach dem Commit | Benachrichtigungen |

#### Server-seitige Hooks

| Hook | Wird ausgelöst | Typische Nutzung |
|------|----------------|------------------|
| `pre-receive` | Beim Empfangen eines Push | Berechtigungen prüfen |
| `post-receive` | Nach dem Empfangen | CI/CD auslösen |

### Einen Hook erstellen

```bash
# 1. Skript erstellen
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# Prüfe, ob TODO im gestagten Code vorkommt
if git diff --cached | grep -q "TODO"; then
  echo "FEHLER: TODO im Code gefunden!"
  echo "Bitte entferne alle TODOs vor dem Commit."
  exit 1
fi
EOF

# 2. Ausführbar machen
chmod +x .git/hooks/pre-commit
```

### Hooks mit dem Team teilen

Hooks in `.git/hooks/` werden **nicht** mit dem Repository geteilt. Lösungen:

- Hooks in einem Ordner im Repository ablegen (z.B. `.githooks/`) und
  `git config core.hooksPath .githooks` setzen
- Tools wie **Husky** (JavaScript) oder **pre-commit** (Python) verwenden
- Ein Setup-Skript bereitstellen, das die Hooks installiert

### Hook umgehen

In Ausnahmefällen kannst du einen Hook überspringen:

```bash
git commit --no-verify -m "Dringende Änderung"
```

### Was du lernst
- Wie du Git Hooks erstellst und aktivierst
- Welche Hook-Typen es gibt und wann sie ausgelöst werden
- Wie du mit Hooks Qualitätsstandards automatisierst
