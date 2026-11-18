# Deployment auf PythonAnywhere

Das Tool läuft auf [PythonAnywhere](https://eu.pythonanywhere.com) im **EU-Rechenzentrum** mit einem kostenlosen Beginner-Account.
Öffentliche Adresse: `https://<benutzername>.eu.pythonanywhere.com/`

Platzhalter in dieser Anleitung:

- `<benutzername>`: PythonAnywhere-Benutzername
- `3.X`: Python-Version auf dem Server (muss bei venv und Web-App identisch sein)

## 1. Account

1. Auf **eu.pythonanywhere.com** (nicht www.pythonanywhere.com) einen Beginner-Account anlegen.
2. Starkes Passwort aus dem Passwortmanager verwenden, Zwei-Faktor-Anmeldung unter „Account“ aktivieren.

## 2. Code und Umgebung (Bash-Konsole auf dem Server)

Im Dashboard unter „Consoles“ eine **Bash**-Konsole öffnen:

```bash
git clone https://github.com/finnpfl/Partizipations-Tool-E-Lade-Standorte.git
cd Partizipations-Tool-E-Lade-Standorte
ls /usr/bin/python3.*          # verfügbare Python-Versionen anzeigen
python3.X -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Die lokale `.venv` wird nicht übertragen: Sie enthält feste Pfade und das Python des lokalen Rechners. Der Server baut sich aus der `requirements.txt` eine eigene Umgebung mit denselben Paketversionen.

## 3. Web-App einrichten

1. Reiter **Web** → **Add a new web app** → **Manual configuration** → Python `3.X` (dieselbe Version wie bei der venv).
2. Auf der Seite der Web-App eintragen:
   - **Source code:** `/home/<benutzername>/Partizipations-Tool-E-Lade-Standorte`
   - **Virtualenv:** `/home/<benutzername>/Partizipations-Tool-E-Lade-Standorte/.venv`
3. Unter „Code“ die **WSGI configuration file** öffnen und den Inhalt ersetzen:

   ```python
   import sys

   path = '/home/<benutzername>/Partizipations-Tool-E-Lade-Standorte'
   if path not in sys.path:
       sys.path.insert(0, path)

   from app import app as application
   ```

4. Speichern, oben auf **Reload** klicken.
5. Unter „Security“ **Force HTTPS** aktivieren.
6. Test: `https://<benutzername>.eu.pythonanywhere.com/` und `/health` müssen antworten.

### Was die WSGI-Datei macht

Auf PythonAnywhere läuft ein fertiger Webserver. Die WSGI-Datei startet keinen Server, sondern sagt diesem Webserver, wo die App liegt. WSGI (Web Server Gateway Interface) ist die standardisierte Schnittstelle zwischen Webserver und Python-App, vergleichbar mit WMS zwischen GIS-Client und Kartenserver.

- `sys.path.insert(0, path)`: Die WSGI-Datei liegt unter `/var/www/`, nicht im Projektordner. Damit `import app` die `app.py` findet, wird der Projektordner an den Anfang des Suchpfads gesetzt.
- `from app import app as application`: Importiert das Flask-Objekt `app` aus der Datei `app.py` und stellt es unter dem Namen `application` bereit. Diesen Namen erwartet der Webserver.

### Fehlersuche

Auf dem Reiter **Web** stehen Links zum **Error log** und **Server log**. Den Traceback von unten nach oben lesen. Häufigste Fehler:

- `ModuleNotFoundError: No module named 'app'`: Pfad in der WSGI-Datei falsch.
- `ModuleNotFoundError: No module named 'flask'`: Virtualenv-Pfad fehlt oder falsch, oder `pip install` lief außerhalb der venv.

## 4. Updates einspielen

Neuer Code kommt immer über einen gemergten Pull Request auf `main`. Danach auf dem Server:

```bash
cd ~/Partizipations-Tool-E-Lade-Standorte
git pull
# nur wenn sich requirements.txt geändert hat:
source .venv/bin/activate
pip install -r requirements.txt
```

Anschließend auf dem Reiter **Web** auf **Reload** klicken. Ohne Reload läuft weiter der alte Code im Arbeitsspeicher.

Regeln:

- Auf dem Server wird nie Code bearbeitet, nur `git pull`. So ist `main` auf GitHub immer der Stand, der live ist.
- Nach jedem Update kurz `/` und `/health` aufrufen (Smoke-Test).

## 5. Umgebungsvariablen (Ausblick auf #7)

Geheimnisse wie der Admin-Schlüssel gehören nicht ins Repo. Auf PythonAnywhere gibt es zwei übliche Wege:

- in der WSGI-Datei vor dem Import setzen: `os.environ['ADMIN_KEY'] = '...'` (die WSGI-Datei liegt nicht im Repo), oder
- eine `.env`-Datei im Projektordner anlegen (steht in der `.gitignore`) und sie in der WSGI-Datei mit `python-dotenv` laden.

Die Entscheidung fällt in #7.

## 6. Grenzen des kostenlosen Tarifs

Stand: November 2026, Quelle: [Free Accounts Features](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/) und Preisseite. Die Bedingungen ändern sich, deshalb vor dem Go-Live erneut prüfen.

| Grenze | Wert | Bedeutung für das Projekt |
|---|---|---|
| Laufzeit der Web-App | **1 Monat**, danach wird sie deaktiviert | Auf dem Reiter **Web** regelmäßig verlängern. Termine im Projektplan: zum Go-Live (30.11.), Ende Dezember, Ende Januar (vor der Präsentation). Eine abgelaufene App lässt sich dort auch wieder aktivieren. |
| Web-Apps | 1 App mit 1 Web-Worker | Anfragen werden nacheinander bearbeitet. Für eine Umfrage mit wenigen Zugriffen gleichzeitig reicht das. |
| Adresse | nur `<benutzername>.eu.pythonanywhere.com`, keine eigene Domain | Benutzername steht auf dem QR-Code, deshalb neutral wählen. |
| Speicherplatz | 512 MiB | venv mit Flask braucht wenig. Für GeoPandas auf dem Server ggf. knapp, deshalb Geodaten lokal aufbereiten und nur GeoJSON hochladen. |
| CPU-Sekunden | 100 pro Tag | Gilt für Konsolen und geplante Aufgaben, nicht für die Web-App. Rechenintensive Skripte (Analyse, Export) lokal ausführen. |
| Ausgehende Verbindungen | nur HTTP(S) zu Seiten auf einer Allowlist | Die App ruft zur Laufzeit keine externen Dienste auf. Die BNetzA-Daten werden lokal aufbereitet und als Datei mitgeliefert (#3). `git pull` von GitHub funktioniert. |
| Konsolen | max. 2 gleichzeitig | Nicht benötigte Konsolen schließen. |
| Geplante Aufgaben | eingeschränkt bzw. nicht verfügbar | Automatisches Backup (#13) im Reiter „Tasks“ prüfen, sonst Backup manuell (Datenbank herunterladen) im wöchentlichen Monitoring. |
| Support | kein direkter Support für kostenlose Accounts, nur Forum | Probleme rechtzeitig vor dem Go-Live testen. |

**Risiko:** Läuft die Verlängerung ab, ist die Umfrage nicht erreichbar, und der QR-Code führt ins Leere. Gegenmaßnahme: Verlängerungstermine im Kalender und im Notion-Tasks-Tracker.
