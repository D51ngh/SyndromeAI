from sklearn.linear_model import LogisticRegression


def build_model(seed=0):
    return LogisticRegression(max_iter=1000, random_state=seed)
