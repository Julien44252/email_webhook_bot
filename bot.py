# bot.py
from flask import Flask, request
import json
import os
from email_sender import send_email   # ou comme tu as nommé ton module

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    # DEBUG pour savoir que ton webhook est bien reçu
    print("🔔 DEBUG: webhook reçu :", data)

    # Prépare sujet et message
    subject = "🚀 Nouveau webhook reçu!"
    body    = json.dumps(data, indent=2)

    # Envoie l’email
    send_email(subject, body)

    return {"status": "email sent"}

if __name__ == "__main__":
    # optionnel : pour pouvoir lancer via `python bot.py`
    app.run()
