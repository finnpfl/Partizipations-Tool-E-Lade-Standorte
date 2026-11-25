# Partizipations-Tool-E-Lade-Standorte

Dieses Tool dient als Beteiligungsinstrument zur Bedarfsermittlung von E-Ladesäulen in der Stadt Frankfurt (Pilotgebiet: Stadtteil Sossenheim). Es wird im Rahmen eines studentischen Projektes im WiSe 2026/2027 entwickelt. Die Kernfunktionalität besteht aus der kartenbasierten Erfassung von Standortwünschen der Bürger:innen, ergänzt um anonymisierte Sachinformationen (E-Auto-Status, Stellplatzsituation, bevorzugter Standorttyp). Die Wünsche werden aus Datenschutzgründen nicht als exakte Standorte, sondern je 250-m-Zelle des INSPIRE-Rasters erfasst.

## Unterschied conda und python -m venv
Der Unterschied besteht in erster Linie in den betreuten Paketen. `conda` verwaltet Python selbst und externe Nicht-Python-Bibliotheken. `venv` hingegen nutzt eine vorhandene Python-Installation und verwaltet Python-Pakete per `pip`.

## Lokal starten
- getestet mit: Python 3.14.5

1. Um das Projekt lokal auszuführen, muss zunächst das Repo von GitHub mit  
```bash
git clone https://github.com/finnpfl/Partizipations-Tool-E-Lade-Standorte.git
cd Partizipations-Tool-E-Lade-Standorte
``` 
geklont und in den jeweiligen Bearbeitungsordner gewechselt werden. 

2. Zur Paketverwaltung wird `venv` verwendet. Bei einer aktivierten conda Umgebung muss diese zunächst deaktiviert werden `conda deactivate`. Danach wird `venv` angelegt und aktiviert 
```bash 
python3 -m venv .venv 
source .venv/bin/activate
```
3. Nun werden die benötigten Pakete installiert. Hierzu wird 
```bash 
pip install -r requirements.txt
``` 
ausgeführt. 
*Achtung!*: Hier sicherheitshalber auf `pip install flask` verzichten, da es sonst zu Komplikation in Bezug auf die Installation neuerer Versionen kommen kann.
4. Anschließend kann der Server mit `flask --app app run --debug` gestartet werden. Zum Testen der Funktionsfähigkeit des Servers können folgende zwei URLs verwendet werden: `http://127.0.0.1:5000/` und `http://127.0.0.1:5000/health`

## Datenquellen
**Daten der Stadtteile** \
Open Data Datenlizenz Deutschland – Namensnennung – Version 2.0 \
Stadt Frankfurt a.M., Bürgeramt Statistik und Wahlen, 2025 (Daten verändert)

**Daten der Ladesäulen** \
Creative Commons Lizenz „CC BY 4.0 - Namensnennung 4.0 International“ \
Herausgeber der Daten: bundesnetzagentur.de

## Daten aufbereiten

Das Skript `scripts/prepare_data.py` erzeugt aus den Rohdaten die Geodaten für die Karte: Stadtteilgrenze, INSPIRE-Raster (250 m, EPSG:3035) und Ladesäulen mit Zellen-ID. Die Ergebnisse liegen in `data/` und sind bereits im Repository enthalten. Neu erzeugen muss man sie nur, wenn sich die Rohdaten ändern.

1. Rohdaten herunterladen und unter diesen Namen in `data/raw/` ablegen (der Ordner ist nicht im Repository):
   - Stadtteilgrenzen Frankfurt (Open Data Frankfurt): `Frankfurt_am_Main_Stadtteile_5461406520595846193.geojson`
   - Ladesäulenregister der Bundesnetzagentur (CSV): `Ladesaeulenregister_BNetzA_2026-11-12.csv`

   **Achtung:** Die CSV nach dem Download nicht in Excel oder einem Editor öffnen und speichern. Sie ist in Windows-Kodierung (cp1252) gespeichert, beim erneuten Speichern gehen die Umlaute verloren.

2. Entwicklungs-Pakete installieren (zusätzlich zu Flask wird GeoPandas benötigt):
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Skript aus dem Projektordner ausführen:
   ```bash
   python scripts/prepare_data.py
   ```

Das Skript erzeugt `data/area_boundary.geojson`, `data/grid_250m.geojson` und `data/stations.geojson` (WGS84) und gibt eine Übersicht der Betreiber mit Anzahl der Ladeeinrichtungen und Ladepunkte aus. Bei neuen Rohdaten mit anderem Dateinamen oder Stand die Konstanten oben im Skript anpassen.