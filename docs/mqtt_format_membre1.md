# Membre 1 - Simulation des capteurs et publication MQTT

## Rôle technique

Cette partie représente la couche objets / edge du projet IoT. Elle simule les capteurs d’un système intelligent de détection d’incendie et publie des messages JSON vers un broker MQTT configuré localement.

## Capteurs simulés

| Capteur | Description |
|---|---|
| `temperature` | Température ambiante en degres Celsius |
| `smoke` | Indice simule de fumee |
| `gas` | Indice simule de gaz |
| `humidity` | Humidite de l’air en pourcentage |

## Configuration MQTT standard

- broker local par defaut : `localhost:1883`
- topic capteurs : `iot/fire/sensor/data`
- topic alertes : `iot/fire/alert`

Des brokers publics peuvent etre utilises a titre optionnel pour des essais distants, mais ils ne sont pas requis pour la demonstration locale.

## Format JSON commun

```json
{
  "device_id": "fire_sensor_01",
  "timestamp": "2026-05-26T10:30:00",
  "temperature": 35.2,
  "smoke": 180,
  "gas": 220,
  "humidity": 45,
  "location": "Salle_1",
  "scenario": "normal"
}
```

## Scénarios simulés

### Normal

- Température : 20 à 35 °C
- Fumée : 20 à 200
- Gaz : 50 à 250
- Humidité : 45 à 65 %

### Suspect

- Température : 40 à 60 °C
- Fumée : 250 à 600
- Gaz : 300 à 550
- Humidité : 30 à 45 %

### Danger

- Température : 65 à 90 °C
- Fumée : 650 à 1000
- Gaz : 600 à 900
- Humidité : 15 à 30 %

## Ce que le Membre 2 utilisera

Le Membre 2 doit configurer Node-RED avec :

```text
MQTT IN topic = iot/fire/sensor/data
MQTT OUT topic = iot/fire/alert
Broker local = localhost:1883
```

Puis parser le payload JSON reçu.
