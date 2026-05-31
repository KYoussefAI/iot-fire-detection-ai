# Tâche 4 - Intégration IA dans Node-RED et logique d’alerte

## 1. Objectif

L’objectif de cette tâche est d’intégrer le modèle d’intelligence artificielle dans le flow Node-RED afin de classifier automatiquement le niveau de risque d’incendie.

Node-RED reçoit les données des capteurs via MQTT, appelle le script Python `predict.py`, récupère la prédiction IA, enrichit le message avec les champs `ai_status`, `risk_score` et `alert`, puis déclenche une alerte lorsque le risque détecté est `danger`.

---

## 2. Entrées utilisées

Cette tâche utilise les fichiers suivants :

- `flow_node_red_base.json` : flow Node-RED de base fourni par la tâche 2.
- `predict.py` : script Python de prédiction fourni par la tâche 3.
- `model_fire_detection.joblib` : modèle IA entraîné fourni par la tâche 3.
- Messages MQTT publiés par le simulateur sur le topic :

```text
iot/fire/sensor/data
```

---

## 3. Format du message reçu

Le message reçu par Node-RED respecte le format JSON commun du projet :

```json
{
  "device_id": "fire_sensor_01",
  "timestamp": "2026-05-27T17:31:05",
  "temperature": 32.91,
  "smoke": 115,
  "gas": 172,
  "humidity": 62,
  "location": "Salle_1",
  "scenario": "normal"
}
```

Les variables utilisées par l’IA sont :

- `temperature`
- `smoke`
- `gas`
- `humidity`

---

## 4. Fonctionnement du flow Node-RED

Le flow final suit cette chaîne de traitement :

```text
MQTT in
→ Validate Sensor Payload
→ Normalize Sensor Values
→ Fire Risk Pre-Alert Logic
→ Prepare IA Command
→ Call predict.py
→ Parse IA JSON
→ Merge IA Result
→ Is Danger?
→ Publish Alert MQTT
```

---

## 5. Préparation de la commande IA

Le node `Prepare IA Command` prépare les quatre valeurs nécessaires pour le script `predict.py`.

Exemple :

```text
24 80 120 55
```

Ces valeurs correspondent à :

```text
temperature smoke gas humidity
```

Le message capteur original est sauvegardé dans `msg.sensor` afin de pouvoir être fusionné ensuite avec le résultat IA.

---

## 6. Appel du script Python

Le node `Call predict.py` utilise un node `exec` pour exécuter le script Python suivant :

```text
python ai/predict.py
```

L’option `Joindre msg.payload` est activée afin d’ajouter automatiquement les valeurs des capteurs à la commande.

Exemple de commande exécutée :

```text
python ai/predict.py 78 850 720 22
```

## Important : configuration du chemin predict.py

- Si Node-RED est lance depuis la racine du projet, utiliser : `python ai/predict.py`
- Si Node-RED est lance depuis un autre dossier, definir manuellement un chemin absolu.
- Exemple Linux/WSL : `python /mnt/e/projects/iot-fire-detection-ai/ai/predict.py`
- Exemple Windows : `python C:\path\to\iot-fire-detection-ai\ai\predict.py`

---

## 7. Résultat retourné par l’IA

Le script `predict.py` retourne un résultat JSON contenant :

```json
{
  "ai_status": "danger",
  "risk_score": 1.0,
  "alert": true
}
```

Le node `Parse IA JSON` transforme cette réponse texte en objet JSON exploitable par Node-RED.

---

## 8. Enrichissement du message

Le node `Merge IA Result` fusionne le message original avec la prédiction IA.

Exemple de message enrichi :

```json
{
  "device_id": "fire_sensor_01",
  "timestamp": "2026-05-27T17:31:41",
  "temperature": 41.73,
  "smoke": 576,
  "gas": 324,
  "humidity": 41,
  "location": "Salle_1",
  "scenario": "suspect",
  "pre_alert": "suspect",
  "ai_status": "suspect",
  "risk_score": 1,
  "alert": false
}
```

---

## 9. Logique d’alerte

La règle d’alerte utilisée est :

```text
Si ai_status == "danger"
alors alert = true
sinon alert = false
```

Le node `Is Danger?` vérifie la valeur :

```text
msg.payload.alert
```

Si cette valeur est `true`, le message est envoyé vers :

- le debug `ALERTE DANGER`
- le node MQTT out `Publish Alert MQTT`

---

## 10. Publication de l’alerte MQTT

Lorsqu’un danger est détecté, l’alerte est publiée sur le topic MQTT :

```text
iot/fire/alert
```

Le node utilisé est :

```text
Publish Alert MQTT
```

Le broker utilisé est :

```text
Local Mosquitto
```

---

## 11. Tests réalisés

### Test normal

Commande testée :

```text
python ai\predict.py 24 80 120 55
```

Résultat obtenu :

```json
{
  "ai_status": "normal",
  "risk_score": 1.0,
  "alert": false
}
```

### Test suspect

Commande testée :

```text
python ai\predict.py 48 340 300 40
```

Résultat obtenu :

```json
{
  "ai_status": "suspect",
  "risk_score": 1.0,
  "alert": false
}
```

### Test danger

Commande testée :

```text
python ai\predict.py 78 850 720 22
```

Résultat obtenu :

```json
{
  "ai_status": "danger",
  "risk_score": 1.0,
  "alert": true
}
```

---

## 12. Résultats observés dans Node-RED

Les messages MQTT sont bien reçus depuis le simulateur sur le topic :

```text
iot/fire/sensor/data
```

Node-RED enrichit correctement les messages avec les champs suivants :

- `pre_alert`
- `ai_status`
- `risk_score`
- `alert`

Exemple normal observé :

```text
scenario: "normal"
ai_status: "normal"
risk_score: 1
alert: false
```

Exemple suspect observé :

```text
scenario: "suspect"
ai_status: "suspect"
risk_score: 1
alert: false
```

Exemple danger attendu :

```text
scenario: "danger"
ai_status: "danger"
risk_score: 1
alert: true
```

---

## 13. Problème rencontré et correction

Au début du test MQTT, le simulateur fonctionnait en mode hors ligne avec le message suivant :

```text
paho-mqtt n'est pas installé : passage en mode hors ligne.
```

Cela signifiait que les messages étaient générés, mais non publiés vers MQTT.

La correction a été d’installer la bibliothèque `paho-mqtt` :

```text
pip install paho-mqtt
```

La vérification a ensuite été faite avec :

```text
python -c "import paho.mqtt.client as mqtt; print('paho-mqtt OK')"
```

Résultat :

```text
paho-mqtt OK
```

Après correction, le simulateur a affiché :

```text
Connexion MQTT réussie.
Message publié.
```

---

## 14. Livrables de la tâche 4

Les livrables produits pour cette tâche sont :

- `flow_node_red_ai_alert.json`
- `README_integration_ia.md`
- `capture_flow_node_red_ai_alert.png`
- `capture_prediction_normal.png`
- `capture_prediction_suspect.png`
- `capture_alert_danger.png`
- `capture_mqtt_publish_simulator.png`

---

## 15. Conclusion

La tâche 4 permet de connecter Node-RED au modèle IA Python afin de classifier le risque d’incendie en temps réel.

Le flow final reçoit les données MQTT, appelle `predict.py`, enrichit le message avec la prédiction IA et déclenche automatiquement une alerte lorsque le statut IA est `danger`.

Cette tâche constitue la liaison entre la partie IA et la partie cloud/dashboard de la tâche 5.
