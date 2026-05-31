"""
=============================================================
  Tâche 3 - Bourti Ayoub
  Projet IoT - Système intelligent de détection d'incendie
  train_model.py : Entraînement, évaluation et sauvegarde du modèle IA
=============================================================
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.preprocessing import LabelEncoder
import joblib

# ─────────────────────────────────────────────
# 1. Paramètres
# ─────────────────────────────────────────────
DATASET_PATH     = "dataset_fire_detection.csv"
MODEL_PATH       = "model_fire_detection.joblib"
EVAL_PATH        = "evaluation_results.txt"
CM_PATH          = "confusion_matrix.png"
RANDOM_STATE     = 42
TEST_SIZE        = 0.25
LABEL_ORDER      = ["normal", "suspect", "danger"]   # ordre logique

print("=" * 60)
print("  Projet IoT - Détection d'incendie  |  Tâche 3")
print("  Bourti Ayoub — Entraînement du modèle IA")
print("=" * 60)

# ─────────────────────────────────────────────
# 2. Chargement et inspection du dataset
# ─────────────────────────────────────────────
print("\n[1/6] Chargement du dataset ...")
df = pd.read_csv(DATASET_PATH)
print(f"  → {len(df)} échantillons chargés")
print(f"  → Colonnes : {list(df.columns)}")
print(f"  → Distribution des classes :")
for cls in LABEL_ORDER:
    count = (df["label"] == cls).sum()
    print(f"     {cls:<10}: {count} exemples")

# Vérification : pas de valeurs manquantes
assert df.isnull().sum().sum() == 0, "Valeurs manquantes détectées !"
print("  → Aucune valeur manquante détectée ✓")

# ─────────────────────────────────────────────
# 3. Préparation des données
# ─────────────────────────────────────────────
print("\n[2/6] Préparation des données ...")
FEATURES = ["temperature", "smoke", "gas", "humidity"]
X = df[FEATURES].values
y = df["label"].values

# Encodage des étiquettes (ordre logique)
le = LabelEncoder()
le.fit(LABEL_ORDER)
y_enc = le.transform(y)
print(f"  → Classes encodées : {dict(zip(le.classes_, le.transform(le.classes_)))}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_enc
)
print(f"  → Train : {len(X_train)} exemples | Test : {len(X_test)} exemples")

# ─────────────────────────────────────────────
# 4. Entraînement — Random Forest (modèle principal)
# ─────────────────────────────────────────────
print("\n[3/6] Entraînement du Random Forest Classifier ...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    random_state=RANDOM_STATE,
    class_weight="balanced",
)
rf_model.fit(X_train, y_train)
print("  → Entraînement terminé ✓")

# ─────────────────────────────────────────────
# 5. Évaluation complète
# ─────────────────────────────────────────────
print("\n[4/6] Évaluation du modèle ...")

y_pred    = rf_model.predict(X_test)
accuracy  = accuracy_score(y_test, y_pred)
report    = classification_report(
    y_test, y_pred, target_names=le.classes_
)
cm        = confusion_matrix(y_test, y_pred, labels=le.transform(LABEL_ORDER))

# Cross-validation (5-fold stratifié)
cv        = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
cv_scores = cross_val_score(rf_model, X, y_enc, cv=cv, scoring="accuracy")

# Importance des features
feat_imp  = pd.Series(rf_model.feature_importances_, index=FEATURES).sort_values(ascending=False)

print(f"  → Accuracy  : {accuracy * 100:.2f} %")
print(f"  → CV Score  : {cv_scores.mean() * 100:.2f} % ± {cv_scores.std() * 100:.2f} %")

# ─────────────────────────────────────────────
# 6. Sauvegarde des résultats d'évaluation
# ─────────────────────────────────────────────
print("\n[5/6] Sauvegarde des fichiers ...")

# 6a. Texte d'évaluation
eval_text = f"""
================================================================
  EVALUATION DU MODELE IA - Detection d incendie
  Tache 3 - Bourti Ayoub
================================================================

Modele         : Random Forest Classifier
Dataset        : {DATASET_PATH}
Echantillons   : {len(df)} total | {len(X_train)} train | {len(X_test)} test
Features       : {', '.join(FEATURES)}
Classes        : {', '.join(LABEL_ORDER)}

----------------------------------------------------------------
ACCURACY SUR LE JEU DE TEST
----------------------------------------------------------------
  Accuracy     : {accuracy * 100:.2f} %

----------------------------------------------------------------
CROSS-VALIDATION (5-Fold Stratifie)
----------------------------------------------------------------
  Scores       : {[f"{s*100:.2f}%" for s in cv_scores]}
  Moyenne      : {cv_scores.mean() * 100:.2f} %
  Ecart-type   : {cv_scores.std() * 100:.2f} %

----------------------------------------------------------------
RAPPORT DE CLASSIFICATION
----------------------------------------------------------------
{report}

----------------------------------------------------------------
MATRICE DE CONFUSION (lignes=reel, colonnes=predit)
----------------------------------------------------------------
  Classes      : {', '.join(LABEL_ORDER)}
{cm}

----------------------------------------------------------------
IMPORTANCE DES FEATURES
----------------------------------------------------------------
{feat_imp.to_string()}

----------------------------------------------------------------
TESTS SUR LES 3 SCENARIOS DU PROJET
----------------------------------------------------------------
  Scenario 1 - Normal  : temp=24 smoke=80  gas=120 humid=55
    Prediction = {le.inverse_transform(rf_model.predict([[24,  80,  120, 55]]))[0]}  (attendu: normal)

  Scenario 2 - Suspect : temp=48 smoke=340 gas=300 humid=40
    Prediction = {le.inverse_transform(rf_model.predict([[48, 340,  300, 40]]))[0]}  (attendu: suspect)

  Scenario 3 - Danger  : temp=78 smoke=850 gas=720 humid=22
    Prediction = {le.inverse_transform(rf_model.predict([[78, 850,  720, 22]]))[0]}  (attendu: danger)

================================================================
"""
with open(EVAL_PATH, "w", encoding="utf-8") as f:
    f.write(eval_text)
print(f"  → {EVAL_PATH} sauvegardé ✓")

# 6b. Confusion matrix PNG
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="YlOrRd",
    xticklabels=LABEL_ORDER,
    yticklabels=LABEL_ORDER,
    linewidths=0.5,
    ax=ax,
)
ax.set_xlabel("Classe prédite", fontsize=12)
ax.set_ylabel("Classe réelle",   fontsize=12)
ax.set_title(
    "Matrice de Confusion — Détection d'incendie\n"
    "Random Forest Classifier | Tâche 3 - Bourti Ayoub",
    fontsize=11,
    fontweight="bold",
)
plt.tight_layout()
plt.savefig(CM_PATH, dpi=150)
plt.close()
print(f"  → {CM_PATH} sauvegardé ✓")

# 6c. Modèle joblib
joblib.dump({"model": rf_model, "label_encoder": le, "features": FEATURES}, MODEL_PATH)
print(f"  → {MODEL_PATH} sauvegardé ✓")

# ─────────────────────────────────────────────
# 7. Résumé final
# ─────────────────────────────────────────────
print("\n[6/6] Résumé final")
print(f"  Accuracy   : {accuracy * 100:.2f} %")
print(f"  CV Moyenne : {cv_scores.mean() * 100:.2f} %")
print("\nScénarios de validation :")
scenarios = [
    ("Normal",  [24,  80,  120, 55], "normal"),
    ("Suspect", [48, 340,  300, 40], "suspect"),
    ("Danger",  [78, 850,  720, 22], "danger"),
]
for name, values, expected in scenarios:
    pred = le.inverse_transform(rf_model.predict([values]))[0]
    ok   = "✓" if pred == expected else "✗"
    print(f"  [{ok}] {name:<8} → {pred}")

print("\n" + "=" * 60)
print("  Entraînement terminé avec succès. Livrables générés :")
for f in [DATASET_PATH, MODEL_PATH, EVAL_PATH, CM_PATH, "predict.py"]:
    print(f"  - {f}")
print("=" * 60)
