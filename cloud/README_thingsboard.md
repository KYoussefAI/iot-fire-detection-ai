# ThingsBoard Cloud dans le projet

## Rôle de ThingsBoard

ThingsBoard Cloud constitue la plateforme IoT cloud du projet. Node-RED lui envoie les données enrichies sous forme de télémétrie MQTT après traitement des mesures capteurs et ajout des champs `ai_status`, `risk_score` et `alert`.

Cette plateforme couvre deux besoins du cahier des charges :

- le stockage des données reçues sous forme de séries temporelles
- la visualisation de ces données dans un tableau de bord

Les widgets du dashboard peuvent afficher `temperature`, `smoke`, `gas`, `humidity`, `ai_status` et `alert`.

## Configuration requise

- Host : `mqtt.thingsboard.cloud`
- Port : `1883`
- Topic : `v1/devices/me/telemetry`
- Username : `PUT_YOUR_DEVICE_TOKEN_HERE`
- Password : vide

## Exemple de télémétrie JSON

```json
{
  "temperature": 79.35,
  "smoke": 851,
  "gas": 836,
  "humidity": 23,
  "ai_status": "danger",
  "risk_score": 1,
  "alert": true
}
```

## Confidentialité du token

Le token réel appartient au compte ThingsBoard du membre du groupe qui a créé le device cloud. Il doit rester privé et ne doit jamais être publié dans GitHub ou dans un fichier versionné.
