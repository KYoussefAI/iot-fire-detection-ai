# README - Node-RED Base Flow

## Projet IoT & IA — Système intelligent de détection d’incendie

---

# 1. Objectif de la tâche

Cette tâche consiste à construire la première couche de traitement Node-RED du système IoT de détection intelligente d’incendie.

L’objectif principal est de :

* recevoir les données capteurs via MQTT,
* vérifier la validité des messages JSON,
* normaliser les valeurs numériques,
* appliquer une première logique de pré-détection de risque,
* produire un payload propre et exploitable pour la partie Intelligence Artificielle.

Cette étape joue un rôle central dans le pipeline du projet, car elle garantit que les données transmises au modèle IA sont cohérentes, propres et structurées.

---

# 2. Architecture du flow réalisé

Le flow Node-RED développé suit l’architecture suivante :

```text
MQTT Broker
     ↓
MQTT Input Node
     ↓
Payload Validation
     ↓
Data Normalization
     ↓
Pre-Alert Logic
     ↓
Debug Output
```

---

# 3. Technologies utilisées

| Technologie | Rôle                                    |
| ----------- | --------------------------------------- |
| Node-RED    | Orchestration et traitement des données |
| MQTT        | Communication publish/subscribe         |
| Mosquitto   | Broker MQTT local                       |
| Python      | Simulation des capteurs incendie        |
| JSON        | Format des messages échangés            |

---

# 4. Topic MQTT utilisé

```text
iot/fire/sensor/data
```

Le flow est abonné à ce topic afin de recevoir les données publiées par le simulateur Python.

---

# 5. Structure JSON traitée

Le flow traite les messages JSON suivants :

```json
{
  "device_id": "fire_sensor_01",
  "timestamp": "2026-05-26T23:41:52",
  "temperature": 76.8,
  "smoke": 904,
  "gas": 731,
  "humidity": 25,
  "location": "Salle_1",
  "scenario": "danger"
}
```

---

# 6. Fonctionnalités implémentées

## 6.1 Réception MQTT

Le node `MQTT Input` reçoit les données envoyées en temps réel par le simulateur de capteurs incendie.

---

## 6.2 Validation du payload

Le node `Validate Sensor Payload` vérifie :

* la présence des champs obligatoires,
* la cohérence minimale des données,
* la validité des valeurs numériques.

Les messages invalides sont automatiquement ignorés.

---

## 6.3 Normalisation des données

Le node `Normalize Sensor Values` convertit les valeurs reçues en types numériques afin d’éviter les erreurs de traitement dans les étapes suivantes du projet.

Les champs normalisés sont :

* temperature
* smoke
* gas
* humidity

---

## 6.4 Logique de pré-alerte

Le node `Fire Risk Pre-Alert Logic` applique une première logique simple basée sur des seuils.

Trois niveaux de risque sont générés :

| Niveau  | Description             |
| ------- | ----------------------- |
| normal  | Situation normale       |
| suspect | Valeurs inhabituelles   |
| danger  | Risque élevé d’incendie |

Le résultat est ajouté dans le champ :

```json
"pre_alert"
```

Exemple :

```json
{
  "pre_alert": "danger"
}
```

---

# 7. Exemple de payload final

```json
{
  "device_id": "fire_sensor_01",
  "timestamp": "2026-05-26T23:41:52",
  "temperature": 76.8,
  "smoke": 904,
  "gas": 731,
  "humidity": 25,
  "location": "Salle_1",
  "scenario": "danger",
  "pre_alert": "danger"
}
```

---

# 8. Exécution du projet

## Étape 1 — Démarrer Mosquitto

```bash
mosquitto
```

---

## Étape 2 — Démarrer Node-RED

```bash
node-red
```

Puis ouvrir :

```text
http://127.0.0.1:1880
```

---

## Étape 3 — Lancer le simulateur Python

```bash
python simulate_fire_sensors.py
```

---

## Étape 4 — Déployer le flow

Cliquer sur le bouton :

```text
Deploy
```

---

## Étape 5 — Observer les résultats

Les payloads propres et enrichis sont visibles dans le panneau Debug de Node-RED.

---

# 9. Livrables produits

| Fichier                         | Description                     |
| ------------------------------- | ------------------------------- |
| flow_node_red_base.json         | Flow Node-RED exporté           |
| README_node_red_base.md         | Documentation technique         |
| capture_node_red_reception.png  | Réception MQTT                  |
| capture_debug_payload_clean.png | Payload propre après traitement |

---

# 10. Résultat obtenu

Le flow Node-RED fonctionne correctement et permet :

* la réception des données MQTT,
* le traitement des payloads JSON,
* la validation des données,
* la normalisation des valeurs,
* la génération d’un niveau de pré-alerte.

Le système est maintenant prêt pour l’intégration de la partie Intelligence Artificielle dans la tâche suivante.

---
