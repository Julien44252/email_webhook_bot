# webhook_test.py
import requests

WEBHOOK_URL = "http://127.0.0.1:5000/webhook"

payload = {
    "ticker": "BTCUSD",
    "price": 50000,
    "side": "buy"
}

try:
    resp = requests.post(WEBHOOK_URL, json=payload, timeout=5)
    print(f"Statut HTTP : {resp.status_code}")
    print("Corps de la réponse :", resp.text)
except Exception as e:
    print("Erreur lors de l'envoi du webhook :", e)
