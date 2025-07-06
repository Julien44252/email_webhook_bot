# test_smtp.py

import os, smtplib
from dotenv import load_dotenv

# Charge les variables depuis .env
load_dotenv()

# Affiche les valeurs pour vérifier
print("🔍 ENV RÉCUPÉRÉ :")
print("  EMAIL_ADDRESS =", os.getenv("EMAIL_ADDRESS"))
print("  EMAIL_PASSWORD set?", bool(os.getenv("EMAIL_PASSWORD")))
print("  TO_EMAIL       =", os.getenv("TO_EMAIL"), "\n")

# Test de connexion SMTP
try:
    print("🔗 Tentative de connexion SMTP_SSL…")
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5)
    print("🔑 Tentative de login…")
    server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
    print("✅ Login réussi !")
    server.quit()
except Exception as e:
    print("❌ Erreur SMTP :", repr(e))
