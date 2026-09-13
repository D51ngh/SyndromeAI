# SyndromeAI / QEC Fault Forensics

Phase 1 asks whether detector patterns from a Stim surface-code memory can
distinguish a known measurement fault from a known CNOT fault. Each sample
stores detector events and the ground-truth fault metadata.

## Run

```bash
python -m pip install stim numpy pandas scikit-learn pymatching
python src/generate_dataset.py --output data/raw/phase1 --samples-per-class 100
python src/inspect_detector_patterns.py --input data/raw/phase1
python src/baseline_classifier.py --input data/raw/phase1
```

The first experiment uses one controlled fault in an otherwise noiseless
distance-3 circuit. It is a diagnostic baseline, not a claim that microscopic
hardware causes are uniquely identifiable from syndrome data.
