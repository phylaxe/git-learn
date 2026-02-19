---
title: "Upstream Tracking"
level: remotes
order: 6
points: 10

setup:
  - cmd: "git init"
  - cmd: "echo '# Projekt' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Initial commit'"
  - cmd: "git clone --bare . ../remote.git"
  - cmd: "git remote add origin ../remote.git"
  - cmd: "git push origin master"
  - cmd: "git checkout -b feature"
  - cmd: "echo 'Neues Feature' > feature.txt"
  - cmd: "git add feature.txt"
  - cmd: "git commit -m 'Feature begonnen'"

task: |
  Du bist auf dem Branch `feature`, der noch keine Upstream-Verbindung hat.
  Wenn du jetzt `git push` ohne Argumente versuchst, weiss Git nicht, wohin
  gepusht werden soll.

  Pushe den Branch `feature` zum Remote `origin` und richte dabei gleichzeitig
  das Upstream-Tracking ein, sodass `git push` und `git pull` in Zukunft
  ohne weitere Argumente funktionieren.

hints:
  - "Mit der Option `-u` (oder `--set-upstream`) richtest du beim Push gleichzeitig das Tracking ein"
  - "Der Befehl lautet: `git push -u origin feature`"
  - "Nach dem Push kannst du mit `git branch -vv` überprüfen, ob das Tracking eingerichtet ist"

solution: |
  git push -u origin feature

validation:
  - type: branch_active
    expected: "feature"
  - type: config_value
    key: "branch.feature.remote"
    expected: "origin"
---

## Upstream Tracking

Upstream-Tracking verbindet einen lokalen Branch mit einem Remote-Branch.
Dadurch wissen `git push` und `git pull`, wohin sie Daten senden bzw.
woher sie Daten holen sollen – ohne dass du es jedes Mal angeben musst.

### Upstream beim Push einrichten

Der einfachste Weg ist die `-u` Option beim ersten Push:

```bash
# Branch pushen UND Tracking einrichten
git push -u origin feature

# Danach reicht:
git push
git pull
```

### Upstream nachträglich setzen

Du kannst das Tracking auch separat einrichten:

```bash
# Upstream für den aktuellen Branch setzen
git branch -u origin/feature

# Upstream für einen bestimmten Branch setzen
git branch -u origin/main main
```

### Tracking überprüfen

```bash
# Alle Branches mit Tracking-Info anzeigen
git branch -vv

# Beispiel-Ausgabe:
#   feature  abc1234 [origin/feature] Feature begonnen
# * master   def5678 [origin/master] Initial commit
```

### Warum ist Tracking wichtig?

- **Kurzformen** wie `git push` und `git pull` funktionieren nur mit Tracking
- `git status` zeigt an, ob dein Branch **vor** oder **hinter** dem Remote ist
- Befehle wie `git pull --rebase` wissen automatisch, von wo sie pullen sollen

### Tracking beim Klonen

Wenn du ein Repository klonst, wird der Standard-Branch automatisch mit
Upstream-Tracking eingerichtet. Neue lokale Branches musst du selbst verbinden.

```bash
# Branch vom Remote auschecken (setzt Tracking automatisch)
git checkout feature
# → Branch 'feature' folgt 'origin/feature'
```

### Was du lernst
- Was Upstream-Tracking ist und warum es nützlich ist
- Wie du mit `git push -u` das Tracking einrichtest
- Wie du den Tracking-Status mit `git branch -vv` überprüfst
