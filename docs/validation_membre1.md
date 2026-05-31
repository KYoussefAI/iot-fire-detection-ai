# Validation du travail - Membre 1

## Commandes de test

### Test hors ligne rapide

```bash
python simulator/simulate_fire_sensors.py --offline --once
```

Résultat attendu : un seul message JSON généré.

### Test continu

```bash
python simulator/simulate_fire_sensors.py
```

Résultat attendu :

- si MQTT est accessible : `Message publié` ;
- si MQTT est inaccessible : `Message généré (mode hors ligne)`.

## Checklist

- [ ] Le script démarre sans erreur.
- [ ] Le fichier `config.json` est lu correctement.
- [ ] Le topic est `iot/fire/sensor/data`.
- [ ] Un message JSON est généré toutes les 3 secondes.
- [ ] Le JSON contient `device_id`, `timestamp`, `temperature`, `smoke`, `gas`, `humidity`, `location`, `scenario`.
- [ ] Les scénarios `normal`, `suspect` et `danger` sont présents.
- [ ] Le script ne s'arrête pas brutalement si Internet ou le broker public est inaccessible.

## Validation pour passer au Membre 2

Le Membre 2 peut commencer lorsque le Membre 1 fournit :

```text
simulator/simulate_fire_sensors.py
simulator/config.json
docs/mqtt_format_membre1.md
```
