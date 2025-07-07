# bot.py
from flask import Flask, request
import traceback

import strategy
from email_sender import send_email

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        payload = request.get_json()
        symbol  = payload.get("symbol")
        if not symbol:
            return "Pas de symbol dans payload", 400

        # 1) fetch + indicateurs
        df  = strategy.fetch_ohlcv(symbol, timeframe="1h", limit=100)
        print(f"🔔 DEBUG : récupéré {len(df)} bougies pour {symbol}")
        df2 = strategy.compute_indicators(df)
        print("🔔 DEBUG : indicateurs calculés")

        # 2) signal ICT
        sig = strategy.generate_signal(df2)
        print("🔔 DEBUG : signal généré :", sig)

        # 3) envoi mail si BUY/SELL
        if sig in ("BUY", "SELL"):
            subject = f"[BOT ICT] {sig} {symbol}"
            body    = (
                f"Signal {sig} sur {symbol} à {df2.index[-1]}\n"
                f"Clôture = {df2['close'].iloc[-1]:.2f}\n"
                f"EMA8 = {df2['EMA8'].iloc[-1]:.2f}, EMA21 = {df2['EMA21'].iloc[-1]:.2f}\n"
                f"ATR  = {df2['ATR'].iloc[-1]:.2f}"
            )
            send_email(subject, body)
            print("✅ DEBUG – Email envoyé avec succès !")
        else:
            print("ℹ️  Aucun signal (rien envoyé)")

        return "OK", 200

    except Exception as e:
        traceback.print_exc()
        return f"Erreur interne : {e}", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
