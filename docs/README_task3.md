# Tâche 3 — Dataset IA, Entraînement et Prédiction Python
**Projet IoT - Système intelligent de détection d'incendie**  
**Responsable : Bourti Ayoub**

---

## Contenu du dossier `ai/`

| Fichier | Rôle |
|---|---|
| `dataset_fire_detection.csv` | Dataset équilibré (120 lignes, 3 classes) |
| `train_model.py` | Script d'entraînement, évaluation et sauvegarde |
| `predict.py` | Script de prédiction compatible Node-RED |
| `model_fire_detection.joblib` | Modèle sauvegardé (généré par `train_model.py`) |
| `evaluation_results.txt` | Métriques complètes : accuracy, CV, rapport, scénarios |
| `confusion_matrix.png` | Matrice de confusion visuelle |

---

## Prérequis

```bash
pip install scikit-learn pandas numpy matplotlib seaborn joblib
```

Python 3.8+ recommandé.

---

## Étape 1 — Entraîner le modèle

```bash
python train_model.py
```

Ce script :
1. Charge `dataset_fire_detection.csv`
2. Divise les données (75% train / 25% test)
3. Entraîne un **Random Forest Classifier** (100 arbres)
4. Évalue avec accuracy, cross-validation 5-fold et rapport de classification
5. Génère `model_fire_detection.joblib`, `evaluation_results.txt`, `confusion_matrix.png`

Résultat attendu :
```
Accuracy   : 100.00 %
CV Moyenne : 100.00 %
[✓] Normal   → normal
[✓] Suspect  → suspect
[✓] Danger   → danger
```

---

## Étape 2 — Utiliser predict.py

### Mode 1 : Arguments positionnels (Node-RED `exec` node)

```bash
python predict.py <temperature> <smoke> <gas> <humidity>
```

Exemples des 3 scénarios :

```bash
# Scénario normal
python predict.py 24 80 120 55
# → {"ai_status": "normal", "risk_score": 1.0, "alert": false}

# Scénario suspect
python predict.py 48 340 300 40
# → {"ai_status": "suspect", "risk_score": 1.0, "alert": false}

# Scénario danger
python predict.py 78 850 720 22
# → {"ai_status": "danger", "risk_score": 1.0, "alert": true}
```

### Mode 2 : JSON via stdin (pipe / API)

```bash
echo '{"temperature":78,"smoke":850,"gas":720,"humidity":22}' | python predict.py
# → {"ai_status": "danger", "risk_score": 1.0, "alert": true}
```

---

## Sortie JSON de predict.py

```json
{
  "ai_status": "danger",
  "risk_score": 0.97,
  "alert": true
}
```

| Champ | Type | Description |
|---|---|---|
| `ai_status` | string | Classe prédite : `normal`, `suspect` ou `danger` |
| `risk_score` | float | Probabilité de la classe prédite (0.0 → 1.0) |
| `alert` | boolean | `true` uniquement si `ai_status == "danger"` |

---

## Intégration dans Node-RED (pour la Tâche 4)

Dans Node-RED, ajouter un **`exec` node** avec la commande :

```
python /chemin/vers/ai/predict.py {{{payload.temperature}}} {{{payload.smoke}}} {{{payload.gas}}} {{{payload.humidity}}}
```

Puis parser la sortie avec un **`json` node** pour obtenir `ai_status`, `risk_score` et `alert` directement dans `msg.payload`.

---

## Description du dataset

Le dataset contient **120 exemples équilibrés** (40 par classe) avec les colonnes :
- `temperature` (°C)
- `smoke` (indice 0–1000)
- `gas` (indice 0–850)
- `humidity` (%)
- `label` : `normal` | `suspect` | `danger`

### Plages de valeurs par classe

| Classe | Température | Fumée | Gaz | Humidité |
|---|---|---|---|---|
| `normal` | 16–35°C | 30–115 | 60–145 | 45–65% |
| `suspect` | 41–60°C | 230–510 | 250–450 | 31–47% |
| `danger` | 63–100°C | 700–1000 | 580–850 | 10–29% |

Ces plages sont cohérentes avec celles définies dans le contrat commun du projet.

---

## Modèle choisi : Random Forest Classifier

- **Pourquoi ?** Robuste sur données tabulaires, résistant au surapprentissage, interprétable via l'importance des features.
- **Hyperparamètres** : 100 arbres, `class_weight="balanced"`, `random_state=42`
- **Alternative testable** : `DecisionTreeClassifier` pour visualisation graphique de l'arbre

---

## Livrables transmis à la Tâche 4

| Livrable | Utilisé par |
|---|---|
| `predict.py` | Node-RED via `exec` node |
| `model_fire_detection.joblib` | Chargé par `predict.py` |
| `evaluation_results.txt` | Documentation / rapport final |
| `confusion_matrix.png` | Rapport final / soutenance |

---

*Projet encadré par : Pr. M. EL Brak — FST Tanger — Année universitaire 2025/2026*
