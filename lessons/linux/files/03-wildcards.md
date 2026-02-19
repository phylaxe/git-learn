---
title: "Wildcards: Die Macht der Muster"
level: files
order: 3
points: 15

setup:
  - cmd: "mkdir -p sortiert/bilder sortiert/dokumente sortiert/code && touch foto1.jpg foto2.jpg foto3.png dokument.pdf notizen.txt readme.md script.sh helper.sh main.py utils.py"

task: |
  Lerne, wie man mit Wildcards viele Dateien auf einmal verarbeitet.

  1. Verschiebe alle `.jpg` und `.png` Dateien nach `sortiert/bilder/`
  2. Verschiebe alle `.md`, `.txt` und `.pdf` Dateien nach `sortiert/dokumente/`
  3. Verschiebe alle `.py` und `.sh` Dateien nach `sortiert/code/`

hints:
  - "`mv *.jpg *.png sortiert/bilder/` verschiebt alle Bild-Dateien auf einmal"
  - "`mv *.md *.txt *.pdf sortiert/dokumente/` verschiebt alle Dokument-Dateien"
  - "`mv *.py *.sh sortiert/code/` verschiebt alle Code-Dateien"
  - "Das `*` Muster passt auf beliebig viele Zeichen im Dateinamen"
  - "Du kannst auch `{*.jpg,*.png}` als alternative Schreibweise verwenden"

solution: |
  mv *.jpg *.png sortiert/bilder/
  mv *.md *.txt *.pdf sortiert/dokumente/
  mv *.py *.sh sortiert/code/

validation:
  - type: directory_structure
    expected:
      - "sortiert/bilder/foto1.jpg"
      - "sortiert/bilder/foto2.jpg"
      - "sortiert/bilder/foto3.png"
      - "sortiert/dokumente/dokument.pdf"
      - "sortiert/dokumente/notizen.txt"
      - "sortiert/dokumente/readme.md"
      - "sortiert/code/script.sh"
      - "sortiert/code/helper.sh"
      - "sortiert/code/main.py"
      - "sortiert/code/utils.py"
---

## Wildcards: Die Macht der Muster

Wildcards (auch Glob-Muster genannt) erlauben es, viele Dateien auf einmal mit einem einzigen Befehl anzusprechen. Die Shell expandiert diese Muster, bevor der Befehl ausgeführt wird.

### `*` — Beliebig viele Zeichen

`*` passt auf beliebig viele Zeichen (auch kein Zeichen):

```
$ ls *.txt          # Alle Dateien mit Endung .txt
$ ls foto*          # Alle Dateien, die mit "foto" beginnen
$ mv *.jpg bilder/  # Alle JPG-Dateien in bilder/ verschieben
```

### `?` — Genau ein Zeichen

`?` passt auf genau ein beliebiges Zeichen:

```
$ ls foto?.jpg      # foto1.jpg, foto2.jpg, aber nicht foto10.jpg
$ ls datei-?.txt    # datei-a.txt, datei-b.txt, ...
```

### `[abc]` — Zeichen aus einer Menge

Eckige Klammern passen auf genau eines der angegebenen Zeichen:

```
$ ls foto[123].jpg    # foto1.jpg, foto2.jpg, foto3.jpg
$ ls [aeiou]*.txt     # Dateien, die mit einem Vokal beginnen
```

### `[a-z]` — Zeichenbereiche

Mit einem Bindestrich kann ein Bereich angegeben werden:

```
$ ls [a-z]*.py    # Python-Dateien, die mit Kleinbuchstabe beginnen
$ ls [0-9]*.log   # Log-Dateien, die mit einer Zahl beginnen
```

### `{muster1,muster2}` — Alternativen (Brace Expansion)

Geschweifte Klammern erlauben mehrere Alternativen in einem Ausdruck:

```
$ mv {*.jpg,*.png} bilder/         # JPG und PNG verschieben
$ ls {*.txt,*.md,*.pdf}            # Verschiedene Dokument-Typen auflisten
$ touch datei{1,2,3}.txt           # datei1.txt, datei2.txt, datei3.txt erstellen
```

### Beispiel: Dateien sortieren

```
$ ls
foto1.jpg  foto2.jpg  foto3.png  skript.py  notizen.txt

$ mv *.jpg *.png bilder/
$ mv *.txt dokumente/
$ mv *.py code/

$ ls bilder/
foto1.jpg  foto2.jpg  foto3.png
```

Wildcards funktionieren mit fast allen Befehlen: `ls`, `cp`, `mv`, `rm`, `grep` und vielen mehr.
