import os
import sys
from datetime import datetime
import requests
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)

GARMIN_USER = os.environ.get("GARMIN_LOGIN", "").strip()
GARMIN_PASS = os.environ.get("GARMIN_PASSWORD", "").strip()
FITBIT_USER = os.environ.get("FITBIT_LOGIN", "").strip()
FITBIT_PASS = os.environ.get("FITBIT_PASSWORD", "").strip()

def sync():
    if not all([GARMIN_USER, GARMIN_PASS, FITBIT_USER, FITBIT_PASS]):
        print("❌ Fehler: Eines der Secrets (GARMIN_LOGIN, GARMIN_PASSWORD, FITBIT_LOGIN, FITBIT_PASSWORD) fehlt!")
        sys.exit(1)

    print("🚀 1. Starte Garmin-Login...")
    try:
        garmin = Garmin(GARMIN_USER, GARMIN_PASS)
        garmin.login()
        print("✅ Garmin-Login erfolgreich!")
    except (GarminConnectAuthenticationError, GarminConnectConnectionError) as e:
        print(f"❌ Garmin-Authentifizierungsfehler: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unerwarteter Garmin-Fehler: {e}")
        sys.exit(1)

    print("🚀 2. Initialisiere Fitbit-Verbindung...")
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"✅ Bereit für den Datenabgleich bis {today}.")

if __name__ == "__main__":
    sync()
Klicke oben rechts auf den grünen Button Commit changes... und bestätige das Pop-up nochmals mit Commit changes.

Schritt 3: Den GitHub Actions Workflow aktualisieren (sync.yml)
Bleibe im Reiter Code.

Klicke dich durch den Ordnerpfad: .github ➔ workflows ➔ klicke auf die Datei sync.yml.

Klicke oben rechts auf das Stift-Symbol (Edit this file).

Lösche den gesamten bisherigen Inhalt heraus und füge diese Konfiguration ein:

YAML
name: Sync

on:
  schedule:
    - cron: "0 */6 * * *"
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Dependencies
        run: |
          pip install --upgrade pip
          pip install garminconnect requests garth

      - name: Run Python Sync
        env:
          GARMIN_LOGIN: ${{ secrets.GARMIN_LOGIN }}
          GARMIN_PASSWORD: ${{ secrets.GARMIN_PASSWORD }}
          FITBIT_LOGIN: ${{ secrets.FITBIT_LOGIN }}
          FITBIT_PASSWORD: ${{ secrets.FITBIT_PASSWORD }}
        run: |
          python sync.py
