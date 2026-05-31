# Statut du projet IoT et IA

## Synthèse

| Composant | Statut | Preuve | Notes |
|---|---|---|---|
| Simulateur capteurs | Implémente | `simulator/simulate_fire_sensors.py` | Génère des scénarios normal, suspect et danger |
| Broker MQTT local | À configurer localement | `simulator/config.json` | Démonstration prévue sur `localhost:1883` |
| Flow Node-RED de base | Implémente | `flow/flow_node_red_base.json` | Réception et traitement initial des messages |
| Dataset IA | Disponible | `ai/dataset_fire_detection.csv` | Base utilisée pour l’entraînement |
| Entraînement IA | Réalisé | `ai/evaluation_results.txt` | Évaluation et modèle déjà produits |
| Prédiction IA | Implémente | `ai/predict.py` | Retourne `ai_status`, `risk_score` et `alert` |
| Intégration IA Node-RED | Implémente | `integration_ia_node_red/flow_node_red_ai_alert.json` | Appel de `predict.py` et fusion des résultats |
| Topic alerte MQTT | Implémente | `integration_ia_node_red/flow_node_red_ai_alert.json` | Publication sur `iot/fire/alert` |
| Dashboard ThingsBoard | Documenté | `screenshots/` | Captures de tableaux de bord et états |
| Test bout en bout | Documenté | `cloud/preuve_test_bout_en_bout.md` | Preuve académique de la chaîne complète |

## Configuration requise avant exécution

- installer les dépendances avec `pip install -r requirements.txt`
- démarrer Mosquitto avec `sudo service mosquitto start`
- configurer le chemin `predict.py` dans Node-RED si nécessaire
- configurer le token ThingsBoard avant l’envoi de télémétrie
