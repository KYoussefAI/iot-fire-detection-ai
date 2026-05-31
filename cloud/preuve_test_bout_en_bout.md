# Preuve de validation : test bout en bout

**Responsable :** LOUAHABI Abdenour  
**Composante :** Tâche 5 (simulation edge et finalisation de la pipeline cloud)

## Objectif du test

Ce document valide le fonctionnement global de la chaîne IoT et IA. Le test vise à montrer que les données environnementales simulées circulent du composant edge jusqu’au tableau de bord cloud, en passant par Node-RED et le modèle de classification.

Dans cette démonstration, le script Python joue le rôle d’un Raspberry Pi simulé au niveau edge.

## Architecture validée

Le chemin de traitement validé est le suivant :

1. **Génération edge :** le script Python génère des valeurs réalistes de température, fumée, gaz et humidité.
2. **Publication MQTT :** le script Python publie les données vers le broker MQTT configuré. Pour la démonstration locale, le broker utilisé est `localhost:1883`.
3. **Orchestration et IA :** Node-RED reçoit le payload, appelle `predict.py`, puis enrichit le JSON avec `ai_status`, `risk_score` et `alert`.
4. **Visualisation cloud :** ThingsBoard reçoit la télémétrie finale via MQTT sur `v1/devices/me/telemetry` et met à jour les widgets du tableau de bord.

L’actionneur simulé correspond à l’alarme virtuelle déclenchée lorsque `alert=true`, avec publication sur le topic MQTT `iot/fire/alert`.

La partie cloud est assurée par ThingsBoard Cloud. Les données enrichies par Node-RED sont envoyées vers ThingsBoard sous forme de télémétrie MQTT. ThingsBoard joue deux rôles : il stocke les valeurs reçues sous forme de séries temporelles et il permet leur visualisation à travers un tableau de bord. Les widgets affichent les mesures `temperature`, `smoke`, `gas` et `humidity`, ainsi que les champs `ai_status` et `alert`. Ainsi, le stockage et la visualisation demandés dans le cahier des charges sont couverts par ThingsBoard.

## Preuves visuelles

Les captures d’écran disponibles dans `screenshots/` documentent les trois scénarios du système :

- `dashboard_normal.png` : statut IA `normal`, alerte `false`
- `dashboard_suspect.png` : statut IA `suspect`, alerte `false`
- `dashboard_danger.png` : statut IA `danger`, alerte `true`

## Stockage et visualisation

ThingsBoard stocke les valeurs de télémétrie reçues sous forme de séries temporelles. Les captures `dashboard_normal.png`, `dashboard_suspect.png` et `dashboard_danger.png` prouvent la visualisation des trois états principaux du système sur le tableau de bord cloud.

L’exigence cloud du projet est donc satisfaite par la combinaison du stockage ThingsBoard et de la visualisation sur dashboard.

## Conclusion

Le flux de données de bout en bout est cohérent pour une démonstration académique. La communication entre composants, l’enrichissement des messages dans Node-RED et la visualisation côté ThingsBoard sont documentés par les preuves disponibles. Le prototype est prêt pour une démonstration académique.
