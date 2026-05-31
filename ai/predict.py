"""
=============================================================
  Tâche 3 - Bourti Ayoub
  Projet IoT - Système intelligent de détection d'incendie
  predict.py : Script de prédiction compatible Node-RED
=============================================================

USAGE :
  Mode arguments positionnels (Node-RED exec node) :
    python predict.py <temperature> <smoke> <gas> <humidity>
    Exemple : python predict.py 78 850 720 22

  Mode JSON stdin (API / pipe) :
    echo '{"temperature":78,"smoke":850,"gas":720,"humidity":22}' | python predict.py

SORTIE JSON :
  {"ai_status": "danger", "risk_score": 0.97, "alert": true}
=============================================================
"""

import sys
import json
import os
import joblib
import numpy as np

# ─────────────────────────────────────────────────────────────
# Chemin du modèle (même dossier que ce script)
# ─────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(SCRIPT_DIR, "model_fire_detection.joblib")

# ─────────────────────────────────────────────────────────────
# Chargement du modèle (une seule fois)
# ─────────────────────────────────────────────────────────────
def load_model():
    if not os.path.exists(MODEL_PATH):
        error = {"error": f"Modèle introuvable : {MODEL_PATH}. Lancer train_model.py d'abord."}
        print(json.dumps(error))
        sys.exit(1)
    bundle = joblib.load(MODEL_PATH)
    return bundle["model"], bundle["label_encoder"], bundle["features"]

# ─────────────────────────────────────────────────────────────
# Fonction de prédiction principale
# ─────────────────────────────────────────────────────────────
def predict(temperature: float, smoke: float, gas: float, humidity: float) -> dict:
    """
    Prédit le niveau de risque d'incendie.

    Paramètres :
        temperature : float  — température en °C
        smoke       : float  — indice de fumée
        gas         : float  — indice de gaz
        humidity    : float  — humidité en %

    Retourne :
        dict avec ai_status (str), risk_score (float), alert (bool)
    """
    model, le, features = load_model()

    X = np.array([[temperature, smoke, gas, humidity]])

    # Classe prédite
    y_enc   = model.predict(X)[0]
    ai_status = le.inverse_transform([y_enc])[0]

    # Probabilités par classe
    probas  = model.predict_proba(X)[0]           # shape (n_classes,)
    classes = le.inverse_transform(model.classes_) # noms des classes encodées

    # risk_score = probabilité de la classe prédite
    class_index = list(classes).index(ai_status)
    risk_score  = round(float(probas[class_index]), 4)

    # Alerte : true uniquement si danger
    alert = ai_status == "danger"

    return {
        "ai_status":  ai_status,
        "risk_score": risk_score,
        "alert":      alert,
    }

# ─────────────────────────────────────────────────────────────
# Lecture des entrées (args ou JSON stdin)
# ─────────────────────────────────────────────────────────────
def parse_inputs():
    # Mode 1 : arguments positionnels python predict.py T S G H
    if len(sys.argv) == 5:
        try:
            return (
                float(sys.argv[1]),
                float(sys.argv[2]),
                float(sys.argv[3]),
                float(sys.argv[4]),
            )
        except ValueError:
            err = {"error": "Arguments invalides. Attendu : python predict.py <temperature> <smoke> <gas> <humidity>"}
            print(json.dumps(err))
            sys.exit(1)

    # Mode 2 : JSON via stdin (pipe ou exec node avec payload)
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            try:
                data = json.loads(raw)
                return (
                    float(data["temperature"]),
                    float(data["smoke"]),
                    float(data["gas"]),
                    float(data["humidity"]),
                )
            except (json.JSONDecodeError, KeyError) as e:
                err = {"error": f"JSON invalide : {str(e)}. Clés attendues : temperature, smoke, gas, humidity"}
                print(json.dumps(err))
                sys.exit(1)

    # Aucune entrée valide
    print(json.dumps({"error": "Usage : python predict.py <temp> <smoke> <gas> <humidity>"}))
    sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Point d'entrée
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    temperature, smoke, gas, humidity = parse_inputs()
    result = predict(temperature, smoke, gas, humidity)
    # Sortie JSON propre — directement parseable par Node-RED
    print(json.dumps(result))
