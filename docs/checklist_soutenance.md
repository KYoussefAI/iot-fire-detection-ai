# Checklist de soutenance

## Démonstration

- Démarrer Mosquitto
- Démarrer Node-RED
- Importer et déployer le flow Node-RED
- Démarrer le simulateur
- Montrer la réception MQTT
- Montrer la sortie debug Node-RED
- Montrer la prédiction IA
- Montrer l’alerte danger
- Montrer le dashboard ThingsBoard

## Problèmes fréquents et corrections

- `paho-mqtt` non installé : exécuter `pip install -r requirements.txt`
- Mosquitto non démarré : exécuter `sudo service mosquitto start`
- chemin `predict.py` incorrect dans Node-RED : ajuster la commande du node `Call predict.py`
- token ThingsBoard absent : renseigner le token du device
- topic MQTT incohérent : vérifier `iot/fire/sensor/data` et `iot/fire/alert`
