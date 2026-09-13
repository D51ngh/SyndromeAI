from sklearn.ensemble import RandomForestClassifier


def build_model(seed=0):
    return RandomForestClassifier(n_estimators=200, random_state=seed, n_jobs=-1)
