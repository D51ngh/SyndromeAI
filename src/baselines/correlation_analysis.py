import argparse
import numpy as np
import pandas as pd


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--input", default="data/raw/phase1"); args=parser.parse_args()
    meta=pd.read_csv(f"{args.input}/metadata.csv"); x=np.load(f"{args.input}/detectors.npz")["detectors"]; meta["detector_count"]=x.sum(axis=1)
    print(meta.groupby("fault_type")["detector_count"].agg(["mean", "std", "count"]).round(4))


if __name__ == "__main__": main()
