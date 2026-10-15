"""TASK169 — fixed-config nonlinear ML diagnostic (RF vs RBF SVM).

Run ONCE under the locked protocol `169_nonlinear_ml_protocol.md`
(SHA-256 159b84f19d609dbbf29c6474a5461c8ae66f5a05fb121b33944840d44aa72b05).
Exactly two predeclared fits; no tuning, no search, no threshold stats.
"""
import csv
import hashlib
import json

import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (brier_score_loss, average_precision_score,
                             roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

DATA = "output/prototypes/fx_h4inv_adx_prep/_t39_baskets_forensics.jsonl"
DATA_SHA = "e2fa81737f9264798baf0c4964084ccb73c7230751f58e43c1975e34f888dc97"
OUT = "output/prototypes/regression_bot_audit/task169"
FEATS = ["adx_base", "atr_base", "spread_base_pips", "dir"]
BOOT_N, BOOT_SEED = 2000, 20261014
PERM_N, PERM_SEED = 1000, 20261015
LOGISTIC_REF_AUC = 0.5278

print("== TASK169 single run: RF vs RBF SVM on _t39 ==")
print("sklearn", sklearn.__version__)

# ---- integrity gates (stop before fitting on any mismatch) ----
raw = open(DATA, "rb").read()
got = hashlib.sha256(raw).hexdigest()
assert got == DATA_SHA, "data hash mismatch: " + got
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines()]
assert len(rows) == 1031, len(rows)
n1 = sum(1 for r in rows if r["outcome"] == 1)
n0 = sum(1 for r in rows if r["outcome"] == 0)
assert (n1, n0) == (651, 380), (n1, n0)
assert all(r.get(f) is not None for r in rows for f in FEATS), "missing predictor"
tr = [r for r in rows if 2021 <= r["year"] <= 2024]
te = [(i, r) for i, r in enumerate(rows) if 2025 <= r["year"] <= 2026]
assert (len(tr), sum(1 for r in tr if r["outcome"] == 0)) == (700, 241)
assert (len(te), sum(1 for _, r in te if r["outcome"] == 0)) == (331, 139)
assert len(tr) + len(te) == 1031, "split not exhaustive"
print("integrity gates OK: 1031 rows; train 700/241f; test 331/139f")

X_tr = np.array([[r[f] for f in FEATS] for r in tr], dtype=float)
y_tr = np.array([r["outcome"] for r in tr], dtype=int)
X_te = np.array([[r[f] for f in FEATS] for _, r in te], dtype=float)
y_te = np.array([r["outcome"] for _, r in te], dtype=int)

# ---- Model A: Random Forest (frozen config) ----
rf = RandomForestClassifier(n_estimators=500, max_depth=4,
                            min_samples_leaf=25, max_features="sqrt",
                            class_weight=None, random_state=20261015,
                            n_jobs=1)
rf.fit(X_tr, y_tr)
rf_prob = rf.predict_proba(X_te)[:, 1]

# ---- Model B: RBF SVM pipeline (scaler fit on train only) ----
svm = Pipeline([("scaler", StandardScaler()),
                ("svc", SVC(kernel="rbf", C=1.0, gamma="scale",
                            class_weight=None))])
svm.fit(X_tr, y_tr)
svm_dec = svm.decision_function(X_te)

# ---- metrics (test only, evaluated once per model) ----
auc_rf = float(roc_auc_score(y_te, rf_prob))
auc_svm = float(roc_auc_score(y_te, svm_dec))
ap_rf = float(average_precision_score(y_te, rf_prob))
ap_svm = float(average_precision_score(y_te, svm_dec))
brier_rf = float(brier_score_loss(y_te, rf_prob))
prev = float((y_te == 0).mean())


def boot_ci(scores):
    rng = np.random.default_rng(BOOT_SEED)
    n, vals, disc = len(y_te), [], 0
    while len(vals) < BOOT_N:
        idx = rng.integers(0, n, n)
        if len(np.unique(y_te[idx])) < 2:
            disc += 1
            continue
        vals.append(float(roc_auc_score(y_te[idx], scores[idx])))
    return ([float(np.percentile(vals, 2.5)),
             float(np.percentile(vals, 97.5))], disc)


def perm_p(scores, obs):
    rng = np.random.default_rng(PERM_SEED)
    ge = 0
    for _ in range(PERM_N):
        if float(roc_auc_score(rng.permutation(y_te), scores)) >= obs:
            ge += 1
    return ge / PERM_N


ci_rf, disc_rf = boot_ci(rf_prob)
ci_svm, disc_svm = boot_ci(svm_dec)
p_rf = perm_p(rf_prob, auc_rf)
p_svm = perm_p(svm_dec, auc_svm)

# predeclared interpretation rule (protocol §5)
def classify(auc, ci, p):
    credible = (ci[0] > 0.5) and (min(1.0, 2 * p) < 0.05)
    material = abs(auc - LOGISTIC_REF_AUC) >= 0.05
    return {"credible": bool(credible), "materially_different": bool(material),
            "pattern_observed": bool(credible and material)}

cls_rf = classify(auc_rf, ci_rf, p_rf)
cls_svm = classify(auc_svm, ci_svm, p_svm)

# ---- artifacts ----
with open(OUT + "/169_test_predictions.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["row_index", "basket_id", "year", "outcome",
                "rf_prob", "svm_decision"])
    for i, (line_idx, r) in enumerate(te):
        w.writerow([line_idx, r["basket_id"], int(r["year"]),
                    int(r["outcome"]), repr(float(rf_prob[i])),
                    repr(float(svm_dec[i]))])

results = {
    "protocol_sha256": "159b84f19d609dbbf29c6474a5461c8ae66f5a05fb121b33944840d44aa72b05",
    "data_sha256": DATA_SHA,
    "environment": {"sklearn": sklearn.__version__,
                    "numpy": np.__version__},
    "features": FEATS,
    "config": {
        "rf": {"n_estimators": 500, "max_depth": 4, "min_samples_leaf": 25,
               "max_features": "sqrt", "class_weight": None,
               "random_state": 20261015, "n_jobs": 1},
        "svm": {"pipeline": "StandardScaler(train)->SVC", "kernel": "rbf",
                "C": 1.0, "gamma": "scale", "class_weight": None,
                "probability": False, "score": "decision_function"},
    },
    "samples": {"total": 1031, "train_n": 700, "train_fails": 241,
                "test_n": 331, "test_fails": 139,
                "test_failure_prevalence": prev,
                "excluded": 0},
    "metrics": {
        "rf": {"test_auc": auc_rf, "ci95": ci_rf, "perm_p": p_rf,
               "avg_precision": ap_rf, "brier": brier_rf,
               "bootstrap_discarded_redraws": disc_rf,
               "bonferroni_p": min(1.0, 2 * p_rf), **cls_rf},
        "svm": {"test_auc": auc_svm, "ci95": ci_svm, "perm_p": p_svm,
                "avg_precision": ap_svm, "brier": None,
                "brier_omitted_reason": "decision scores are not probabilities",
                "bootstrap_discarded_redraws": disc_svm,
                "bonferroni_p": min(1.0, 2 * p_svm), **cls_svm},
    },
    "logistic_reference": {"test_auc": 0.5278, "ci95": [0.466, 0.594],
                           "perm_p": 0.204, "source": "TASK152 report",
                           "formal_difference_test": None,
                           "reason": "no saved TASK152 predictions"},
    "inference": {"bootstrap": {"n": BOOT_N, "seed": BOOT_SEED},
                  "permutation": {"n": PERM_N, "seed": PERM_SEED},
                  "multiplicity": "two predeclared comparisons; bonferroni alpha 0.025",
                  "exploratory_nonconfirmatory": True,
                  "dependence_caveat": "within-month basket correlation; row bootstrap precision may be overstated"},
}
with open(OUT + "/169_model_results.json", "w") as fh:
    json.dump(results, fh, indent=2, sort_keys=True)

print("prevalence(fail) test:", round(prev, 4))
print("RF   AUC", round(auc_rf, 4), "CI", [round(x, 4) for x in ci_rf],
      "p", round(p_rf, 4), "AP", round(ap_rf, 4), "Brier", round(brier_rf, 4))
print("SVM  AUC", round(auc_svm, 4), "CI", [round(x, 4) for x in ci_svm],
      "p", round(p_svm, 4), "AP", round(ap_svm, 4))
print("pattern RF:", cls_rf, "| pattern SVM:", cls_svm)
print("done — single run complete")
