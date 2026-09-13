from sklearn.metrics import confusion_matrix


def evaluate_predictions(actual, predicted):
    return {"confusion_matrix": confusion_matrix(actual, predicted).tolist()}
