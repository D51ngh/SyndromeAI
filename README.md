# SyndromeAI: QEC Fault Forensics

This repository studies whether surface-code detector histories can identify
and localize circuit-level faults. Phase I compares three controlled classes:
`none`, measurement faults, and CNOT faults.

The model input is detector data only. The injected fault metadata is kept as
ground truth for training and evaluation. The first pipeline is intentionally
small and reproducible before adding persistent noise, overlapping faults,
unknown-fault detection, or decoder adaptation.

## Quick start

```bash
python -m pip install -r requirements.txt
python -m src.simulation.generate_samples --output data/raw/phase1 --samples-per-class 100
python -m src.baselines.correlation_analysis --input data/raw/phase1
python -m src.training.train_classifier --input data/raw/phase1
```

Run tests with `pytest`. See `paper/` and `configs/` for the research plan.
