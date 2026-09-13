import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from src.baselines.logistic_regression import build_model as build_logistic
from src.models.classifier import build_classifier


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--input", default="data/raw/phase1"); args=parser.parse_args(); root=Path(args.input)
    x=np.load(root/"detectors.npz")["detectors"]; meta=pd.read_csv(root/"metadata.csv"); y=meta.class_id.to_numpy()
    train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=.25,random_state=0,stratify=y)
    for name, model in (("logistic",build_logistic()),("mlp",build_classifier())):
        model.fit(train_x,train_y); pred=model.predict(test_x); print(name, "accuracy", round(accuracy_score(test_y,pred),4)); print(classification_report(test_y,pred,zero_division=0))


if __name__ == "__main__": main()
