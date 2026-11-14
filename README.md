# Partizipations-Tool-E-Lade-Standorte

Dieses Tool dient als Beteiligungsinstrument zur Bedarfsermittlung von E-Ladesäulen in der Stadt Frankfurt (Stadtteil Nordend). Es wird im Rahmen eines studentischen Projektes im WiSe 2026/2027 entwickelt. Die Kernfunktionalität besteht aus der kartenbasierten Erfassung von Standortwünschen der Bürger:innen, welche mit einigen anonymisierten Sachinformationen (bspw. Lade-Typ, Fahrzeugdaten, Status) untermauert werden.

## Unterschied conda und python -m venv
Der Unterschied besteht in erster Linie in den betreuten Paketen. Python -m venv isoliert ein Python-Projekt, conda kann auch andere Komponenten isolieren. Venv ist in der Python-Installation enthalten, während conda seperat installiert werden muss.

## Lokal starten
- Voraussetzung: Python 3.14.5

1. Um das Projekt lokal auszuführen, muss zunächst das Repo von GitHub geklont und in den jeweiligen Bearbeitungsordner gewechselt werden. 
2. Zur Paketverwaltung wird ```venv``` verwendet. Bei einer aktivierten conda Umgebung muss diese zunächst deaktiviert werden ```bash conda deactivate```. Danach wird ```venv``` angelegt und aktiviert ```bash python3 -m venv .venv source .venv/bin/activate```
3. Nun werden die benötigten Pakete installiert. Hierzu wird ```bash pip install -r requirements.txt``` ausgeführt. Dies sorgt im Gegensatz zu ```bash pip install flask``` dafür, dass nur die für das Projekt benötigten Ressourcen heruntergeladen werden.
4. Anschließend kann der Server mit ```flask --app app run --debug``` gestartet werden. Zum Testen der Funktionsfähigkeit des Servers können folgende zwei URLs verwendet werden: ```http://127.0.0.1:5000/``` und ```http://127.0.0.1:5000/health``` 