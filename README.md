# Système intelligent de détection d’incendie basé sur l’IoT et l’IA

## Présentation du projet

Ce projet assemble un système complet de démonstration académique pour la détection d’incendie. Un simulateur Python génère des mesures de capteurs incendie, publie des messages JSON via MQTT, Node-RED traite ces messages, appelle le script d’IA `predict.py` pour classifier le risque, déclenche une alerte MQTT si nécessaire, puis transmet les données enrichies vers un tableau de bord ThingsBoard.

Le script Python joue le rôle d’un Raspberry Pi simulé dans la couche edge du système.

L’actionneur simulé correspond à une alarme virtuelle déclenchée via le champ `alert=true` et la publication sur le topic MQTT `iot/fire/alert`.

## Architecture globale

```text
Simulateur Python -> MQTT Mosquitto -> Node-RED -> IA predict.py -> Alerte MQTT -> ThingsBoard
```

## Structure du projet

| Dossier | Description |
|---|---|
| `simulator/` | Simulateur de capteurs incendie et configuration MQTT locale |
| `flow/` | Flow Node-RED de base |
| `ai/` | Dataset, entraînement, modèle et script de prédiction IA |
| `integration_ia_node_red/` | Flow Node-RED avec intégration IA et documentation associée |
| `cloud/` | Guide de démonstration cloud et preuve de test bout en bout |
| `screenshots/` | Captures d’écran de validation et de tableau de bord |
| `docs/` | Documentation complémentaire, formats MQTT et checklist |
| `tests/` | Scripts de test et de vérification MQTT |

## Technologies utilisées

Le projet utilise Python, MQTT, Mosquitto, Node-RED, JSON, Scikit-learn, Random Forest et ThingsBoard.

## Installation

```bash
pip install -r requirements.txt
sudo apt install mosquitto mosquitto-clients
```

## Configuration MQTT locale

La configuration locale par défaut repose sur :

- broker MQTT : `localhost:1883`
- topic capteurs : `iot/fire/sensor/data`
- topic alertes : `iot/fire/alert`

Des brokers publics peuvent être utilisés de manière optionnelle pour des essais distants, mais ils ne sont pas requis pour la démonstration locale.

## Exécution de la démonstration

1. Démarrer Mosquitto :
   ```bash
   sudo service mosquitto start
   ```
2. Démarrer Node-RED :
   ```bash
   node-red
   ```
3. Importer puis déployer le flow Node-RED.
4. Démarrer le simulateur :
   ```bash
   python simulator/simulate_fire_sensors.py
   ```
5. Observer le topic MQTT capteur :
   ```bash
   mosquitto_sub -h localhost -t iot/fire/sensor/data
   ```
6. Observer la sortie debug Node-RED et le tableau de bord ThingsBoard.

## Tests rapides

```bash
python simulator/simulate_fire_sensors.py --once
python simulator/simulate_fire_sensors.py --offline --once
python ai/predict.py 24 80 120 55
python ai/predict.py 48 340 300 40
python ai/predict.py 78 850 720 22
```

Sorties IA attendues :

- `normal` -> `{"ai_status": "normal", "alert": false}`
- `suspect` -> `{"ai_status": "suspect", "alert": false}`
- `danger` -> `{"ai_status": "danger", "alert": true}`

## Différence entre pre_alert, ai_status et alert

- `pre_alert` = première estimation basée sur des seuils dans Node-RED.
- `ai_status` = classification finale produite par `predict.py`.
- `alert` = `true` uniquement lorsque `ai_status == "danger"`.

Dans cette architecture, l’actionneur simulé est l’alarme virtuelle représentée par `alert=true` et par la publication du message d’alerte sur `iot/fire/alert`.

Exemple de JSON enrichi :

```json
{
  "device_id": "fire_sensor_01",
  "timestamp": "2026-05-31T15:40:00",
  "temperature": 78,
  "smoke": 850,
  "gas": 720,
  "humidity": 22,
  "location": "Salle_1",
  "scenario": "danger",
  "pre_alert": "danger",
  "ai_status": "danger",
  "risk_score": 1.0,
  "alert": true
}
```

## Configuration ThingsBoard

Chaque utilisateur doit configurer son propre token de device ThingsBoard ainsi que son tableau de bord.

La partie cloud est assurée par ThingsBoard Cloud. Les données enrichies par Node-RED sont envoyées vers ThingsBoard sous forme de télémétrie MQTT. ThingsBoard joue deux rôles : il stocke les valeurs reçues sous forme de séries temporelles et il permet leur visualisation à travers un tableau de bord. Les widgets affichent les mesures `temperature`, `smoke`, `gas` et `humidity`, ainsi que les champs `ai_status` et `alert`. Ainsi, le stockage et la visualisation demandés dans le cahier des charges sont couverts par ThingsBoard.

### Détails de configuration MQTT ThingsBoard

- ThingsBoard Cloud est la plateforme IoT cloud utilisée dans ce projet.
- Les données enrichies sont envoyées à ThingsBoard via MQTT.
- Le topic de télémétrie utilisé est `v1/devices/me/telemetry`.
- Le token d’accès du device est utilisé comme nom d’utilisateur MQTT.
- Aucun mot de passe n’est requis dans la configuration standard du device.
- ThingsBoard stocke la télémétrie entrante sous forme de données time-series et la visualise dans des tableaux de bord.
- Le tableau de bord affiche `temperature`, `smoke`, `gas`, `humidity`, `ai_status` et `alert`.
- Les tokens réels ne doivent jamais être commités dans GitHub.

## État actuel du projet

Éléments déjà implémentés :

- simulateur
- publication MQTT locale
- flow Node-RED de base
- modèle IA
- intégration IA dans Node-RED
- topic MQTT d’alerte
- captures et preuves ThingsBoard

Éléments à configurer localement :

- service Mosquitto
- chemin `predict.py` dans Node-RED si nécessaire
- token ThingsBoard

## Problèmes fréquents et corrections

- `paho-mqtt` non installé : exécuter `pip install -r requirements.txt`
- Mosquitto non démarré : exécuter `sudo service mosquitto start`
- mauvais chemin d’exécution Node-RED : ajuster la commande du node `Call predict.py`
- token ThingsBoard absent : configurer le token du device dans le flow concerné
- topic MQTT incohérent : vérifier `iot/fire/sensor/data` et `iot/fire/alert`
