import pandas as pd, joblib, shap
from features import extract_features

model, FEATURE_COLUMNS = joblib.load('phish_model.pkl')

WARNINGS = {
    'has_ip':         'The link uses a numeric IP address instead of a website name.',
    'has_at':         "The '@' symbol can hide the real destination of the link.",
    'num_subdomains': 'The address has an unusually large number of subdomains.',
    'keyword_count':  'The URL contains words often used to trick users (login, verify, update).',
    'url_length':     'The URL is unusually long, possibly hiding its true domain.',
    'is_shortener':   'A shortened link hides the final destination.',
    'domain_entropy': 'The domain name looks randomly generated.',
    'bad_tld':        'The domain ending is frequently abused in scams.',
    'is_https':       'The site does not use a secure HTTPS connection.',
}

explainer = shap.TreeExplainer(model)

def explain(url, top_k=4):
    feats = pd.DataFrame([extract_features(url)])
    prob = model.predict_proba(feats)[0][1]
    sv = explainer.shap_values(feats)
    sv = sv[1][0] if isinstance(sv, list) else sv[0, :, 1] if sv.ndim == 3 else sv[0]
    ranked = sorted(zip(feats.columns, sv), key=lambda t: t[1], reverse=True)
    reasons = [WARNINGS[f] for f, v in ranked if v > 0 and f in WARNINGS][:top_k]
    level = 'High' if prob >= .7 else 'Medium' if prob >= .4 else 'Low'
    return {'verdict': 'Phishing' if prob >= .5 else 'Legitimate',
            'risk_score': round(prob*100, 1), 'level': level, 'reasons': reasons}
