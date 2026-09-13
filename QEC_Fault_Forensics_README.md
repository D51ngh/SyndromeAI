# QEC Fault Forensics

## Overview

QEC Fault Forensics is a research project that studies whether different circuit-level errors in a surface-code quantum error correction circuit can be identified from syndrome and detector-event patterns.

The first phase asks:

> Can we distinguish a measurement error from a CNOT error using only detector-event data?

The long-term goal is to use syndrome data not only for decoding, but also for diagnosing what type of error occurred, where it occurred, how long it persisted, and whether it contributed to a logical failure.

## Phase 1 Goal

Phase 1 studies two fault classes:

1. Measurement errors
2. CNOT errors

The experiment uses simulation so the true injected fault is known, while the analysis method only sees the detector-event data.

## Phase 1 Workflow

```text
Build surface-code circuit
        ↓
Choose a fault type
        ↓
Measurement OR CNOT
        ↓
Inject the fault
        ↓
Run Stim simulation
        ↓
Collect detector events
        ↓
Extract spatial and temporal features
        ↓
Compare error fingerprints
        ↓
Train a simple classifier
        ↓
Measurement or CNOT?
```

## Why Use Simulation First?

Stim allows us to generate detector data while keeping exact ground-truth information about:

- fault type,
- fault location,
- fault round,
- error probability,
- logical outcome.

This gives us labeled data for training and evaluation.

Example:

```text
Detector history → CNOT error
Detector history → Measurement error
```

The classifier receives only the detector history. The true fault label is kept separately as the answer key.

## Syndrome Fingerprint

A syndrome fingerprint is the spatial and temporal pattern of detector events left by an error.

Example:

```text
             QEC Round
Detector    1  2  3  4  5

D10         .  .  .  .  .
D11         .  X  X  .  .
D12         .  .  .  .  .
D13         .  .  .  .  .
```

The project investigates whether measurement and CNOT faults leave distinguishable fingerprints.

## Initial Variables

### 1. Detector Count
Total number of detector events.

### 2. Spatial Spread
How far apart the activated detectors are on the surface-code lattice.

### 3. Temporal Spread
How many QEC rounds separate the first and last detector events.

### 4. Persistence
Whether abnormal detector activity continues across consecutive rounds.

### 5. Same-Detector Repetition
Whether the same detector fires repeatedly over time.

### 6. Simultaneous Detector Events
How many detectors fire in the same QEC round.

These variables are the starting point for understanding how the two fault classes differ.

## Project Structure

```text
qec-fault-forensics/
│
├── README.md
│
├── configs/
│   └── phase1.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── build_surface_code.py
│   ├── inject_measurement_error.py
│   ├── inject_cnot_error.py
│   ├── generate_dataset.py
│   ├── inspect_detector_patterns.py
│   └── baseline_classifier.py
│
├── results/
│   ├── figures/
│   └── tables/
│
└── notebooks/
    └── phase1_analysis.ipynb
```

## File Descriptions

### `build_surface_code.py`

Creates the clean surface-code circuit.

Initial setup:

```text
distance = 3
rounds = 10
```

Responsibilities:

- generate the Stim circuit,
- obtain detector coordinates,
- obtain logical observables,
- store circuit metadata.

### `inject_measurement_error.py`

Introduces a controlled measurement fault.

Should allow control over:

```text
measurement location
QEC round
error probability
```

Example:

```text
fault_type = measurement
stabilizer = S4
round = 5
probability = 0.01
```

### `inject_cnot_error.py`

Introduces a controlled fault at a CNOT gate.

Should record:

```text
ancilla qubit
data qubit
QEC round
circuit tick
error probability
```

Example:

```text
fault_type = CNOT
ancilla = S4
data = D7
round = 5
probability = 0.01
```

### `generate_dataset.py`

Main data-generation script.

Responsibilities:

1. Build the surface-code circuit.
2. Randomly choose a fault class.
3. Randomly choose a location.
4. Randomly choose a round.
5. Inject the fault.
6. Run Stim.
7. Collect detector events.
8. Save detector data.
9. Save ground-truth labels separately.

## Dataset Format

Each sample should contain detector information and ground truth.

Example:

```text
sample_id: 1024

detector_events:
D7 @ round 4
D7 @ round 5
D13 @ round 5

ground_truth:
fault_type: CNOT
location: S4-D7
round: 4
```

### `inspect_detector_patterns.py`

Performs the initial physics and statistical analysis.

It should calculate:

- detector count,
- spatial spread,
- temporal spread,
- persistence,
- same-detector repetition,
- simultaneous event count.

It should also generate:

- detector-count histograms,
- spatial-spread plots,
- temporal-spread plots,
- space-time detector maps,
- detector correlation matrices.

### `baseline_classifier.py`

Tests whether simple machine-learning models can distinguish the two fault classes.

Start with:

- Logistic Regression
- Random Forest

Input:

```text
detector count
spatial spread
temporal spread
persistence
same-detector repetition
simultaneous detector count
```

Output:

```text
Measurement Error
or
CNOT Error
```

The goal is to establish a baseline before using a neural network.

## Phase 1 Evaluation

Use:

- accuracy,
- precision,
- recall,
- F1 score,
- confusion matrix.

Example confusion matrix:

| True Error | Predicted Measurement | Predicted CNOT |
|---|---:|---:|
| Measurement | 89% | 11% |
| CNOT | 15% | 85% |

A key research question is:

> Under what conditions does a CNOT error produce a detector pattern that looks like a measurement error?

## Train / Validation / Test Split

Suggested split:

```text
70% training
15% validation
15% testing
```

Later, test generalization by training and testing on different error probabilities or different fault locations.

## Phase 1 Success Criterion

Phase 1 succeeds if detector-derived features can distinguish measurement and CNOT errors significantly better than random guessing.

For two balanced classes:

```text
Random baseline ≈ 50%
```

The experiment should determine how distinguishable the two mechanisms actually are.

## Neural Network Stage

The neural network comes after the baseline analysis.

Add:

```text
src/
├── models/
│   └── classifier.py
│
└── training/
    ├── train_classifier.py
    └── evaluate.py
```

The neural network will receive raw detector histories instead of only hand-designed features.

Example input:

```text
              Detector
          D1 D2 D3 D4 D5

Round 1    0  0  0  0  0
Round 2    0  1  0  0  0
Round 3    0  1  1  0  0
Round 4    0  0  0  0  0
```

## Connection to Temporal-Correlation Research

The previous research direction studies:

```text
Known correlated noise
        ↓
Surface code
        ↓
Detector events
        ↓
MWPM
        ↓
Logical performance
```

The fault-forensics project begins solving the reverse problem:

```text
Detector events
        ↓
Infer hidden fault
        ↓
Infer temporal behavior
        ↓
Determine logical significance
```

This directly connects the new project to correlated and non-Markovian noise research.

## Future Phases

### Phase 2 — Fault Localization
Predict where the error occurred.

### Phase 3 — Persistent and Correlated Errors
Estimate fault duration and temporal correlation.

### Phase 4 — Overlapping Errors
Handle multiple simultaneous fault mechanisms.

### Phase 5 — Unknown Error Detection
Detect patterns that do not match known training classes.

### Phase 6 — Logical Failure Attribution
Measure which detected fault patterns are most strongly associated with logical failure.

### Phase 7 — Physical Root Cause
Combine syndrome data with hardware information such as:

- T1/T2,
- calibration history,
- qubit frequency,
- leakage metrics,
- temperature,
- control telemetry.

The long-term objective is:

```text
Detector pattern
      ↓
Circuit-level fault
      ↓
Possible physical mechanism
```

## Tools

Initial software stack:

- Python
- Stim
- PyMatching
- NumPy
- Pandas
- Matplotlib
- scikit-learn

Later:

- PyTorch
- Graph Neural Networks
- Temporal neural networks

## Current Status

```text
[x] Research question defined
[x] Phase 1 architecture defined
[ ] Surface-code circuit generation
[ ] Measurement-error injection
[ ] CNOT-error injection
[ ] Dataset generation
[ ] Detector fingerprint analysis
[ ] Baseline classification
[ ] Neural-network classifier
```

## Immediate Next Milestone

> Generate a distance-3 surface-code dataset containing controlled measurement and CNOT faults and visualize the detector-event fingerprint of each fault class.

The neural network should be introduced only after the detector patterns are understood statistically and physically.
