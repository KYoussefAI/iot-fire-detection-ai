# Démonstration : Système intelligent de détection d'incendie

Ce document décrit la procédure de démonstration locale du système IoT de détection d’incendie, depuis le simulateur Python jusqu’au tableau de bord ThingsBoard.

## Prérequis

- Python 3.x installé
- dépendances Python installées avec `pip install -r requirements.txt`
- Mosquitto installé et disponible localement
- Node-RED installé et accessible sur `http://localhost:1880`
- flow `integration_ia_node_red/flow_node_red_ai_alert.json` importé et déployé
- tableau de bord ThingsBoard configuré avec votre propre device token

## Configuration MQTT locale

La démonstration locale utilise par défaut :

- broker MQTT : `localhost:1883`
- topic capteurs : `iot/fire/sensor/data`
- topic alertes : `iot/fire/alert`

Un broker public peut être utilisé à titre optionnel pour des tests distants, mais il n’est pas requis pour la démonstration locale.

## Étapes de lancement

### 1. Démarrer Mosquitto

```bash
sudo service mosquitto start
```

### 2. Démarrer Node-RED

```bash
node-red
```

### 3. Déployer le flow Node-RED

Importer `integration_ia_node_red/flow_node_red_ai_alert.json`, vérifier le broker local, puis déployer le flow.

### 4. Démarrer le simulateur

Depuis la racine du projet :

```bash
python simulator/simulate_fire_sensors.py
```

Le script publie les données vers le broker MQTT configuré. Pour la démonstration locale, le broker utilisé est `localhost:1883`.

### 5. Vérifier la réception MQTT

```bash
mosquitto_sub -h localhost -t iot/fire/sensor/data
```

### 6. Vérifier l’orchestration et le cloud

- observer la sortie debug dans Node-RED
- vérifier l’enrichissement avec `pre_alert`, `ai_status`, `risk_score` et `alert`
- confirmer l’affichage des données sur le tableau de bord ThingsBoard
