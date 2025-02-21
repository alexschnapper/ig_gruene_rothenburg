# Instagram Dashboard GRÜNE Rothenburg ob der Tauber

Dieses Repository enthält ein Dashboard, das Daten von einem verwalteten Instagram-Account sammelt und visualisiert.

Als Beispiel wird der Instagram Account Grüne Rothenburg genommen:
https://www.instagram.com/gruene_rothenburg/ 

Wenn alles gut läuft, sind die Daten unter https://alexschnapper.github.io/ig_gruene_rothenburg/ einsehbar


1. collect_data.py

Diese Datei enthält den Code zum Abrufen der Daten von der Instagram API und zum Speichern der Daten in CSV-Dateien.


2. data_analysis.ipynb

Dieses Jupyter Notebook analysiert die Daten und erstellt die Diagramme.

3. app.py

Diese Datei erstellt ein Dash Dashboard zur interaktiven Darstellung der Diagramme.

4. .github/workflows/update_data.yml

Diese Datei erstellt einen GitHub Actions Workflow, um die Daten regelmäßig zu aktualisieren und die HTML-Datei zu generieren.

6. Website lokal aufrufen

Um die Website lokal aufzurufen, kannst du einen einfachen HTTP-Server verwenden. Navigiere in das Verzeichnis, in dem sich die HTML-Datei befindet, und führe den folgenden Befehl aus:

'python -m http.server'

Dies startet einen lokalen Server, und du kannst die Website in deinem Browser unter http://localhost:8000 aufrufen.