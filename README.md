# Partizipations-Tool-E-Lade-Standorte

Dieses Tool dient als Beteiligungsinstrument zur Bedarfsermittlung von E-Ladesäulen in der Stadt Frankfurt (Stadtteil Nordend). Es wird im Rahmen eines studentischen Projektes im WiSe 2026/2027 entwickelt. Die Kernfunktionalität besteht aus der kartenbasierten Erfassung von Standortwünschen der Bürger:innen, welche mit einigen anonymisierten Sachinformationen (bspw. Lade-Typ, Fahrzeugdaten, Status) untermauert werden.

## Unterschied conda und python -m venv
Der Unterschied besteht in erster Linie in den betreuten Paketen. `conda` verwaltet Python selbst und externe Nicht-Python-Bibliotheken. `venv` hingegen nutzt eine vorhandene Python-Installation und verwaltet Python-Pakete per `pip`.

## Lokal starten
- getestet mit: Python 3.14.5

1. Um das Projekt lokal auszuführen, muss zunächst das Repo von GitHub mit `git clone https://github.com/finnpfl/Partizipations-Tool-E-Lade-Standorte.git` geklont und mit `cd ...` in den jeweiligen Bearbeitungsordner gewechselt werden. 
2. Zur Paketverwaltung wird `venv` verwendet. Bei einer aktivierten conda Umgebung muss diese zunächst deaktiviert werden `conda deactivate`. Danach wird `venv` angelegt und aktiviert 
```bash 
python3 -m venv .venv 
source .venv/bin/activate
```
3. Nun werden die benötigten Pakete installiert. Hierzu wird `bash pip install -r requirements.txt` ausgeführt. 
*Achtung!*: Hier sicherheitshalber auf `pip install flask` verzichten, da es sonst zu Komplikation in Bezug auf die Installation neuerer Versionen kommen kann.
4. Anschließend kann der Server mit `flask --app app run --debug` gestartet werden. Zum Testen der Funktionsfähigkeit des Servers können folgende zwei URLs verwendet werden: `http://127.0.0.1:5000/` und `http://127.0.0.1:5000/health`

