from sklearn.metrics import confusion_matrix


def summarize(actual, predicted):
    return confusion_matrix(actual, predicted)
