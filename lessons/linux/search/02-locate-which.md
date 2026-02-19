---
title: "Programme und Befehle finden"
level: search
order: 2
points: 10

setup:
  - cmd: "mkdir -p ~/bin"
  - cmd: "printf '#!/bin/bash\\necho hello\\n' > ~/bin/myscript.sh && chmod +x ~/bin/myscript.sh"

task: |
  Heute lernst du, wie du herausfindest, wo Programme auf deinem System installiert sind.

  Aufgaben:
  1. Finde heraus, wo das Programm "bash" auf deinem System liegt.
     Nutze dazu den Befehl which. Reiche den Pfad mit check ein.
     Beispiel: check "/bin/bash"

  2. Finde heraus, was fuer ein Typ der Befehl "cd" ist (built-in, alias, etc.).
     Nutze dazu den Befehl type und speichere die Ausgabe in "cd-type.txt".
     Beispiel: type cd > cd-type.txt

hints:
  - "which zeigt den vollstaendigen Pfad eines Programms: which bash"
  - "type zeigt an, was ein Befehl ist: type cd"
  - "type cd > cd-type.txt speichert die Ausgabe in eine Datei"
  - "Reiche den Pfad von bash ein: check \"/bin/bash\" oder check \"/usr/bin/bash\""
  - "whereis zeigt noch mehr Informationen: whereis bash"

solution: |
  which bash
  check "$(which bash)"
  type cd > cd-type.txt

validation:
  - type: check_answer
    contains: "bash"
  - type: file_exists
    path: cd-type.txt
---

## Programme und Befehle finden

Wenn du wissen willst, wo ein Programm auf deinem System installiert ist oder
was genau hinter einem Befehl steckt, gibt es mehrere nützliche Werkzeuge.

### which - Wo liegt das Programm?

`which` sucht in den Verzeichnissen der `PATH`-Variable und zeigt den vollen Pfad:

```bash
which bash          # /bin/bash oder /usr/bin/bash
which python3       # /usr/bin/python3
which ls            # /bin/ls
which nichtda       # Keine Ausgabe wenn nicht gefunden
```

### type - Was ist dieser Befehl?

`type` zeigt an, was hinter einem Befehl steckt:

```bash
type cd             # cd is a shell builtin
type ls             # ls is /bin/ls (oder aliased to ...)
type ll             # ll is aliased to `ls -la`
type python3        # python3 is /usr/bin/python3
```

Mouegliche Typen:
- **builtin** – Eingebauter Shell-Befehl (z.B. cd, echo, pwd)
- **alias** – Ein Alias fuer einen anderen Befehl
- **function** – Eine Shell-Funktion
- **file** – Ein externes Programm (eine Datei)

### whereis - Noch mehr Informationen

`whereis` sucht nach Binaerdatei, Quellcode und Manpage:

```bash
whereis bash        # bash: /bin/bash /usr/share/man/man1/bash.1.gz
whereis python3     # Zeigt alle bekannten Pfade
```

### command -v - Portabler als which

`command -v` ist POSIX-kompatibel und funktioniert in allen Shells:

```bash
command -v bash     # /bin/bash
command -v cd       # cd (bei builtins)
```

### Die PATH-Variable

Wenn du einen Befehl eingibst, sucht die Shell in den Verzeichnissen der `PATH`-Variable:

```bash
echo $PATH          # Zeigt alle Suchpfade
# Ausgabe z.B.: /usr/local/bin:/usr/bin:/bin:/home/user/bin
```

Eigene Skripte in `~/bin/` erreichbar machen:
```bash
export PATH="$PATH:$HOME/bin"   # Zu .bashrc hinzufuegen
```

### Praxisbeispiel

```bash
# Wo ist Python installiert?
which python3
type python3

# Ist git installiert?
which git && echo "git ist installiert" || echo "git fehlt"

# Alle Orte wo python gefunden wird
type -a python
```
