# Insurance Claim Fraud Detection Dataset Generator & Framework

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Dataset Status](https://img.shields.io/badge/Dataset-100k%20Rows%20%7C%2062%20Cols-success.svg)](#-dataset-overview)
[![Fraud Ratio](https://img.shields.io/badge/Fraud%20Ratio-20.04%25-red.svg)](#-fraud-logic--scoring-engine)

A complete, production-ready framework for generating and validating a realistic, high-dimensional **Insurance Claim Fraud Detection Dataset** (100,000 records, 62 columns).

This project bridges **Finance, Insurance Analytics, Machine Learning Classification, Anomaly Detection, and Explainable AI (XAI)** by simulating complex, non-linear fraud indicators and realistic business logic.

---

## Features & Highlights

* **100,000 Clean Records**: 100% complete, zero missing values, zero duplicate rows, and unique primary keys.
* **62 High-Dimensional Features**: Categorical, numerical, date, dynamic risk flags, and realistic claim financials.
* **Realistic Fraud Engine**: Target positive class (`fraudulent = Yes`) calibrated to **~20%** using a weighted multi-factor scoring algorithm.
* **Reproducible Data Pipeline**: Built using modular Python scripts with seed control, parameter management, and automated integrity validation assertions.
* **ML & XAI Ready**: Out-of-the-box support for LightGBM/XGBoost classification, SHAP/LIME explainability, and cost-sensitive risk evaluation.

---

## Project Structure

```text
Insurance-Claim-Fraud-Detection-Dataset/
│
├── dataset/
│   └── insurance_claim_fraud_dataset.csv  # Output CSV (100k rows x 62 cols)
│
├── scripts/
│   ├── constants.py                       # Schema, categories, ranges & fraud weights
│   ├── utils.py                           # Cost calculations & fraud scoring math
│   ├── generate_dataset.py                # Main synthetic generator (Pandas + Faker)
│   └── validate_dataset.py                # Automated integrity & distribution tests
│
├── docs/                        
│   └── DATA_DICTIONARY.md                 # Complete schema dictionary
│
├── .gitignore                             # Git ignore configuration
├── LICENSE                                # Apache License 2.0
└── requirements.txt                       # Dependencies
├── README.md                              # Documentation
```

## Fraud Logic & Scoring Engine

Instead of random target assignment, fraud probability is calculated through a dynamic risk matrix simulating real-world insurer detection flags:

| **Fraud Risk Indicator**     | **Weight Added** | **Condition / Trigger**                     |
| ---------------------------- | ---------------- | ------------------------------------------- |
| **Suspicious Documents**     | `+25`            | Document flags raised                       |
| **Identity Not Verified**    | `+20`            | Identity verification failure               |
| **GPS Location Mismatch**    | `+15`            | Incident GPS does not match claim telemetry |
| **Inconsistent Statements**  | `+15`            | Conflicting narrative statements logged     |
| **No Police Report**         | `+10`            | Severe accident without a police report     |
| **Delayed Reporting**        | `+10`            | Claim filed > 5 days after incident         |
| **Multiple Previous Claims** | `+10`            | Claimant has > 2 historical claims          |
| **High Claim Amount**        | `+8`             | Claim amount exceeds $35,000                |
| **Night Submission**         | `+8`             | Submitted between 10 PM and 5 AM            |
| **Repair Shop Unverified**   | `+6`             | Facility outside approved network           |

*A stochastic noise parameter ($\mathcal{N}(0, 4)$) is added to ensure soft boundaries before applying the binary decision threshold.*

## Quickstart Guide

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Insurance-Claim-Fraud-Detection-Dataset.git
cd Insurance-Claim-Fraud-Detection-Dataset
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the Dataset

Execute the generator script to create the 100,000-row CSV file:

```bash
python scripts/generate_dataset.py
```

### 4. Validate Dataset Integrity

Run the assertion pipeline to verify row/column dimensions, target distributions, and clean data guarantees:

```bash
python scripts/validate_dataset.py
```

## Python Usage Example

When loading the dataset into Pandas, set `keep_default_na=False` to prevent standard text codes like `"NA"` from being parsed as `NaN` values:

```python
import pandas as pd

# Load dataset cleanly
df = pd.read_csv(
    'dataset/insurance_claim_fraud_dataset.csv',
    keep_default_na=False
)

print(f"Dataset Shape: {df.shape}")
print("\nTarget Class Distribution:")
print(df['fraudulent'].value_counts(normalize=True) * 100)
```

## Use Cases & Applications

1. **Fraud Classification Models**: Train gradient boosted trees such as XGBoost, CatBoost, and LightGBM or use Neural Networks to detect fraudulent activity.
2. **Explainable AI (XAI)**: Compute SHAP values or LIME explanations to identify key indicators driving high-risk predictions.
3. **Imbalanced Learning**: Benchmark cost-sensitive learning, focal loss, SMOTE, or threshold-tuning algorithms.
4. **Interactive Fraud Dashboards**: Build Streamlit, Dash, or Power BI dashboards displaying claim distributions and risk scores.

## Dataset Overview

The dataset contains **100,000 synthetic insurance claim records** with **62 features**, covering claimant information, policy details, incident characteristics, financial information, verification signals, historical claim behavior, fraud indicators, and the final fraud classification target.

The dataset is designed for educational, research, benchmarking, and machine learning experimentation purposes.

## License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome. You can improve the dataset generator, add new fraud indicators, enhance validation logic, introduce additional machine learning benchmarks, or improve documentation.

Please open an issue to discuss significant changes before submitting a pull request.

## Disclaimer

This dataset is **synthetic** and does not represent real insurance customers, claims, policies, companies, or financial records. It should not be used for real-world insurance underwriting, fraud investigations, financial decisions, or automated decisions affecting individuals without appropriate validation and regulatory review.
