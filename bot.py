# bot.py

from flask import Flask, request
import json
import os
from email_sender import send_email
from strategy import fetch_ohlcv, compute_indicators, generate_signal, place_order

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("🔔 DEBUG: webhook reçu :", data)

    # --- Exécution de la stratégie ICT ---
    symbol = data.get("symbol", "BTC/USDT")
    df     = fetch_ohlcv(symbol)
    df     = compute_indicators(df)
    signal = generate_signal(df)
    if signal:
        order = place_order(symbol, signal.lower(), amount=0.001)
        note  = f"Signal {signal}, order placed: {order}"
    else:
        note  = "Pas de signal clair"

    # Prépare sujet et message enrichis
    subject = f"🤖 Stratégie ICT – {signal or 'NEUTRE'}"
    body    = json.dumps({
        "webhook": data,
        "signal":  signal,
        "note":    note
    }, indent=2)

    # Envoie l’email
    send_email(subject, body)

    return {"status": "done"}

if __name__ == "__main__":
    # Pour exécuter en local avec python bot.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
