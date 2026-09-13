from sklearn.neural_network import MLPClassifier


def build_localizer(seed=0):
    return MLPClassifier(hidden_layer_sizes=(64, 32), early_stopping=True, max_iter=400, random_state=seed)
