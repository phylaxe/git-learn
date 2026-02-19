---
title: "Den Bug jagen"
level: stash
order: 3
points: 20

setup:
  - cmd: "git init"
  - cmd: "echo 'status=ok' > test.txt"
  - cmd: "git add test.txt"
  - cmd: "git commit -m 'Projekt gestartet'"
  - cmd: "echo 'status=ok\nversion=2' > test.txt"
  - cmd: "git add test.txt"
  - cmd: "git commit -m 'Version aktualisiert'"
  - cmd: "echo 'status=ok\nversion=3' > test.txt"
  - cmd: "git add test.txt"
  - cmd: "git commit -m 'Stabile Version'"
  - cmd: "echo 'status=broken\nversion=4' > test.txt"
  - cmd: "git add test.txt"
  - cmd: "git commit -m 'Bug eingeführt'"
  - cmd: "echo 'readme' > README.md"
  - cmd: "git add README.md"
  - cmd: "git commit -m 'Dokumentation ergänzt'"
  - cmd: "echo 'config=default' > config.txt"
  - cmd: "git add config.txt"
  - cmd: "git commit -m 'Konfiguration hinzugefügt'"

task: |
  In deinem Repository hat sich irgendwann ein Bug eingeschlichen:
  In der Datei test.txt wurde `status=ok` zu `status=broken` geändert.
  Es gibt 6 Commits und du weisst nicht genau, welcher den Fehler verursacht hat.

  Nutze `git bisect`, um den schuldigen Commit zu finden:

  1. Starte mit `git bisect start`
  2. Markiere den aktuellen Stand als schlecht: `git bisect bad`
  3. Markiere den ersten Commit als gut: `git bisect good <hash>` (nutze `git log --oneline` um den Hash zu finden)
  4. Git springt nun automatisch zu einem mittleren Commit. Prüfe `test.txt` und markiere mit `git bisect good` oder `git bisect bad`
  5. Wiederhole, bis git den Commit gefunden hat
  6. Beende die Suche mit `git bisect reset`

  Übermittle die Commit-Nachricht des fehlerhaften Commits mit `check`.

hints:
  - "Schau dir mit `git log --oneline` alle Commits an – der älteste steht unten"
  - "Bei jedem Schritt: lies test.txt mit `cat test.txt`. Steht dort `status=ok`, ist es `good`, sonst `bad`"
  - "Der fehlerhafte Commit hat die Nachricht 'Bug eingeführt'. Starte bisect, markiere HEAD als bad, den ersten Commit als good, und folge den Schritten"

solution: |
  git log --oneline
  git bisect start
  git bisect bad
  git bisect good <hash-des-ersten-commits>
  # Bei jedem Schritt: cat test.txt, dann git bisect good/bad
  # Bis git den Commit findet
  git bisect reset
  check "Bug eingeführt"

validation:
  - type: check_answer
    contains: "Bug eingeführt"
---

## Den Bug jagen

Stell dir vor, dein Projekt funktionierte letzte Woche noch einwandfrei,
aber jetzt ist etwas kaputt. Irgendwo zwischen damals und heute hat sich
ein Bug eingeschlichen – aber in welchem der vielen Commits?

`git bisect` nutzt eine **binäre Suche**, um den fehlerhaften Commit
effizient zu finden. Statt jeden Commit einzeln zu prüfen, halbiert
bisect den Suchbereich bei jedem Schritt.

### Wie git bisect funktioniert

1. Du sagst Git, welcher Commit **schlecht** (bad) ist – normalerweise der aktuelle
2. Du sagst Git, welcher Commit **gut** (good) war – ein älterer, funktionierender Stand
3. Git springt zum mittleren Commit und du prüfst: gut oder schlecht?
4. Je nach Antwort halbiert Git den Suchbereich weiter
5. Nach wenigen Schritten ist der schuldige Commit gefunden

### Beispiel-Ablauf

```bash
git bisect start
git bisect bad              # Aktueller Commit ist kaputt
git bisect good abc1234     # Dieser alte Commit war ok

# Git springt zu einem mittleren Commit
cat test.txt                # Prüfen: Bug vorhanden?
git bisect good             # oder: git bisect bad

# Nach wenigen Schritten:
# abc5678 is the first bad commit
git bisect reset            # Zurück zum normalen Zustand
```

### Effizienz

Bei 1000 Commits braucht bisect nur etwa **10 Schritte** (log2 von 1000),
um den fehlerhaften Commit zu finden. Das ist deutlich schneller als
manuelles Durchsuchen.

### Was du lernst
- Wie du mit `git bisect` systematisch einen Bug-Commit findest
- Das Prinzip der binären Suche in der Git-Geschichte
- Wie du nach dem Bisect mit `reset` zum Normalzustand zurückkehrst
