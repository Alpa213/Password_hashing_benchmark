# Performance and Resource Consumption Analysis of Password Hashing Algorithms Under Different Configuration Parameters

## Author

**Alpamys Ospanov**  
**Student ID:** 77481

**University:** Vistula University  
**Course:** Architecture of Computers

## Research Question

How do different settings of Argon2id, bcrypt, and PBKDF2 affect their speed and resource consumption when hashing and verifying passwords?

## Project Overview

This project investigates the performance and resource consumption of three password-hashing algorithms: Argon2id, bcrypt, and PBKDF2-HMAC-SHA256.

The experiment evaluates nine configurations in total, measuring hashing time, verification time, CPU utilization, and observed process memory changes. Each configuration is tested 30 times after a warm-up cycle.

The project contains the Python source code, experimental measurements, summary CSV files, and visualization graphs.

## Experimental Environment

| Component | Specification |
|---|---|
| Operating System | Windows 11 |
| Python | 3.14.0 |
| CPU | AMD Ryzen 7 8845HS |
| Physical cores | 8 |
| Logical processors | 16 |
| RAM | 64 GB, 5600 MHz |

## Tested Algorithms and Configurations

### Argon2id

- Memory cost: 19,456 KiB, 32,768 KiB, and 65,536 KiB
- Time cost: 2
- Parallelism: 1

### bcrypt

- Cost factors: 10, 11, and 12

### PBKDF2-HMAC-SHA256

- Iterations: 300,000, 600,000, and 900,000
- Derived key length: 32 bytes
- Salt length: 16 bytes

## Experimental Procedure

1. One warm-up hashing and verification cycle is performed for each configuration.
2. Each configuration is measured 30 times.
3. Hashing and verification are timed separately.
4. Execution time is measured using Python's `time.perf_counter()`.
5. CPU utilization and process RSS memory are monitored using `psutil`.
6. Resource samples are collected in a separate thread at approximately 10 ms intervals.
7. Configurations are executed sequentially in ascending parameter order within each algorithm.

The experiment includes:

- 3 algorithms;
- 3 configurations per algorithm;
- 9 configurations in total;
- 270 measurement repetitions;
- 540 measured operations, including hashing and verification.

A synthetic test password is used. No real user passwords are included.

## Project Structure

```text
password-hashing-benchmark/
│
├── code/
│   ├── argon2_test.py
│   ├── bcrypt_test.py
│   ├── compare_results.py
│   ├── full_parameter_experiment.py
│   ├── pbkdf2_test.py
│   └── resource_monitor.py
│
├── data/
│   ├── argon2_results.csv
│   ├── bcrypt_results.csv
│   ├── comparison_summary.csv
│   ├── parameter_sweep_results.csv
│   ├── parameter_sweep_summary.csv
│   └── pbkdf2_results.csv
│
├── graphs/
│   ├── comparison_cpu.png
│   ├── comparison_ram_argon2id.png
│   ├── comparison_ram_other.png
│   └── comparison_time.png
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

Python 3.14.0 is used for the experiment.

Clone the repository:

```bash
git clone https://github.com/Alpa213/Password_hashing_benchmark.git
cd Password_hashing_benchmark
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Experiment

Run the main parameter sweep from the project root:

```bash
python code/full_parameter_experiment.py
```

The script generates or replaces:

- `data/parameter_sweep_results.csv` — individual experimental measurements;
- `data/parameter_sweep_summary.csv` — aggregated statistical results.

**Important:** The raw parameter sweep results file is cleared at the beginning of a new experiment run. Preserve or rename existing results before running the experiment again if they need to be retained.

## Data and Measurements

The summary CSV file includes:

- Average hashing time;
- Standard deviation of hashing time;
- Minimum and maximum hashing time;
- Average verification time;
- Standard deviation of verification time;
- Minimum and maximum verification time;
- Average CPU measurements;
- Average and maximum observed RSS memory increases.

The `data/` directory contains the raw measurements and summary files produced by the experiments.

## Graphs

The `graphs/` directory contains visualizations from the comparison experiments:

- `comparison_time.png` — baseline execution time comparison;
- `comparison_cpu.png` — baseline CPU utilization comparison;
- `comparison_ram_argon2id.png` — Argon2id memory comparison;
- `comparison_ram_other.png` — bcrypt and PBKDF2 memory comparison.

## Methodological Limitations

The experiment has several limitations:

- Measurements represent one hardware and software environment.
- Configuration execution order is fixed and not randomized.
- System load and thermal conditions may influence measurements.
- Periodic resource sampling may miss short-lived changes.
- CPU measurements contain unusually high observations and should be interpreted cautiously.
- Very small RSS changes may be below the practical resolution of the monitoring method.
- Argon2id salt generation is included in the timed hashing operation, whereas bcrypt and PBKDF2 salts are generated before timing. This limits direct comparison of absolute hashing times between algorithms.

For these reasons, results should be interpreted within the scope of the tested environment and measurement procedure.

## Reproducibility

This repository provides:

- Python experiment source code;
- Resource-monitoring implementation;
- Dependency list;
- Raw experimental CSV measurements;
- Aggregated summary CSV files;
- Comparison graphs;
- Instructions for running the experiment.

The experiment can be repeated using the installation and execution commands described above.

## Data and Code Availability

The source code, experimental data, and supporting materials are publicly available at:

https://github.com/Alpa213/Password_hashing_benchmark

## Academic Use

This repository supports the research project submitted for the Student Research Challenge in the Architecture of Computers course at Vistula University.