import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from features import extract_features

df = pd.read_csv('data/urls.csv')       # columns: url, label (1 = phishing)
X = pd.DataFrame([extract_features(u) for u in df['url']])
y = df['label']

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                          stratify=y, random_state=42)
model = RandomForestClassifier(n_estimators=300, max_depth=None,
                               random_state=42, n_jobs=-1)
model.fit(X_tr, y_tr)

print(classification_report(y_te, model.predict(X_te)))
print('ROC-AUC:', roc_auc_score(y_te, model.predict_proba(X_te)[:, 1]))
joblib.dump((model, list(X.columns)), 'phish_model.pkl')
print('Model saved to phish_model.pkl')
