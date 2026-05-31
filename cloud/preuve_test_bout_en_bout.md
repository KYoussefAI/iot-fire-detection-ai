# Preuve de validation : test bout en bout

**Responsable :** LOUAHABI Abdenour  
**Composante :** Tâche 5 (simulation edge et finalisation de la pipeline cloud)

## Objectif du test

Ce document valide le fonctionnement global de la chaîne IoT et IA. Le test vise à montrer que les données environnementales simulées circulent du composant edge jusqu’au tableau de bord cloud, en passant par Node-RED et le modèle de classification.

## Architecture validée

Le chemin de traitement validé est le suivant :

1. **Génération edge :** le script Python génère des valeurs réalistes de température, fumée, gaz et humidité.
2. **Publication MQTT :** le script Python publie les données vers le broker MQTT configuré. Pour la démonstration locale, le broker utilisé est `localhost:1883`.
3. **Orchestration et IA :** Node-RED reçoit le payload, appelle `predict.py`, puis enrichit le JSON avec `ai_status`, `risk_score` et `alert`.
4. **Visualisation cloud :** ThingsBoard reçoit la télémétrie finale via MQTT sur `v1/devices/me/telemetry` et met à jour les widgets du tableau de bord.

## Preuves visuelles

Les captures d’écran disponibles dans `screenshots/` documentent les trois scénarios du système :

- `dashboard_normal.png` : statut IA `normal`, alerte `false`
- `dashboard_suspect.png` : statut IA `suspect`, alerte `false`
- `dashboard_danger.png` : statut IA `danger`, alerte `true`

## Conclusion

Le flux de données de bout en bout est cohérent pour une démonstration académique. La communication entre composants, l’enrichissement des messages dans Node-RED et la visualisation côté ThingsBoard sont documentés par les preuves disponibles. Le prototype est prêt pour une démonstration académique.
