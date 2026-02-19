---
title: "Durch den Dateibaum navigieren"
level: navigation
order: 2
points: 10

setup:
  - cmd: "mkdir -p projekte/webseite/css projekte/webseite/js projekte/api/src docs/archiv"
  - cmd: "touch projekte/webseite/index.html projekte/api/src/main.py"

task: |
  Navigiere durch den Verzeichnisbaum und hinterlasse eine Spur.

  1. Wechsle in das Verzeichnis `projekte/webseite/css` (relativer Pfad)
  2. Wechsle zurueck nach `/exercise` (absoluter Pfad)
  3. Wechsle nach `docs/archiv` (relativer Pfad)
  4. Erstelle dort eine Datei namens `hier.txt`:

     touch hier.txt

hints:
  - "`cd verzeichnis` wechselt in ein Unterverzeichnis (relativer Pfad)"
  - "Absolute Pfade beginnen mit `/`, z.B. `cd /tmp/git-learn/exercise`"
  - "`cd ..` wechselt ins uebergeordnete Verzeichnis"
  - "`cd ~` oder einfach `cd` wechselt ins Home-Verzeichnis"
  - "`cd -` wechselt zurueck ins zuletzt besuchte Verzeichnis"

solution: |
  cd projekte/webseite/css
  cd /tmp/git-learn/exercise
  cd docs/archiv
  touch hier.txt

validation:
  - type: file_exists
    path: "docs/archiv/hier.txt"
---

## Durch den Dateibaum navigieren

Das Dateisystem ist wie ein Baum aufgebaut: Es gibt eine Wurzel (`/`) und von dort verzweigen sich Verzeichnisse in Unterverzeichnisse. Mit `cd` bewegst du dich durch diesen Baum.

### `cd` — Change Directory

```
cd verzeichnis     # Wechsle in ein Unterverzeichnis
cd ..              # Wechsle ins uebergeordnete Verzeichnis
cd ~               # Wechsle ins Home-Verzeichnis
cd /               # Wechsle ins Wurzelverzeichnis
cd -               # Zurueck ins zuletzt besuchte Verzeichnis
```

### Absolute vs. relative Pfade

**Relative Pfade** beginnen vom aktuellen Verzeichnis aus:

```
$ pwd
/exercise
$ cd projekte/webseite/css
$ pwd
/exercise/projekte/webseite/css
```

**Absolute Pfade** beginnen immer mit `/` und sind unabhaengig vom aktuellen Verzeichnis:

```
$ cd /exercise/docs/archiv
$ pwd
/exercise/docs/archiv
```

### Navigationshilfen

| Symbol | Bedeutung                        |
|--------|----------------------------------|
| `.`    | Aktuelles Verzeichnis            |
| `..`   | Uebergeordnetes Verzeichnis      |
| `~`    | Home-Verzeichnis des Benutzers   |
| `/`    | Wurzelverzeichnis des Systems    |

### Tipp: Mehrere Ebenen auf einmal

```
$ cd ../../..     # Drei Ebenen nach oben
$ cd ../geschwister  # Eine Ebene hoch, dann in "geschwister"
```

### Tab-Vervollstaendigung

Druecke `Tab`, um Pfade automatisch zu vervollstaendigen. Das spart Tipparbeit und verhindert Tippfehler.
