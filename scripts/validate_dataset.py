"""
validate_dataset.py
Validation tool to ensure zero nulls, correct column counts, exact duplicate-free
Claim IDs, and distribution compliance.
"""

import os
import pandas as pd

def run_validations():
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "dataset", "insurance_claim_fraud_dataset.csv")

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset missing at {dataset_path}. Run generate_dataset.py first.")

    print(f"Loading dataset from: {dataset_path}")
    
    # Disable automatic NA parsing so text strings like "NA" aren't treated as NaN
    df = pd.read_csv(dataset_path, keep_default_na=False)

    print("\n--- Running Automated Assertions ---")

    # 1. Row and Column Count Validation
    assert len(df) == 100000, f"Expected 100,000 rows, found {len(df)}"
    assert df.shape[1] == 62, f"Expected 62 total columns (61 features + 1 target), found {df.shape[1]}"
    print("✓ Row and Column Count Check Passed (100,000 Rows, 62 Columns)")

    # 2. Missing Value & Duplicate Check
    null_counts = df.isnull().sum().sum()
    assert null_counts == 0, f"Dataset contains {null_counts} unexpected NULL values!"
    assert df.duplicated().sum() == 0, "Dataset contains duplicate records!"
    assert df["claim_id"].nunique() == 100000, "claim_id column contains non-unique keys!"
    print("✓ Zero Missing Values, Zero Duplicates, and Unique IDs Confirmed")

    # 3. Fraud Target Proportion Check
    fraud_counts = df["fraudulent"].value_counts(normalize=True)
    fraud_pct = fraud_counts.get("Yes", 0.0) * 100
    print(f"✓ Fraud Ratio Distribution: No = {(100 - fraud_pct):.2f}%, Yes = {fraud_pct:.2f}%")
    assert 18.0 <= fraud_pct <= 22.0, f"Fraud target ratio ({fraud_pct:.2f}%) outside expected ~20% threshold!"

    # 4. Target Specific Features
    expected_cols = [
        'claim_id', 'policy_id', 'customer_id', 'customer_name', 'claim_date',
        'incident_date', 'claim_status', 'claim_amount', 'approved_amount', 'deductible',
        'claim_duration_days', 'age', 'gender', 'marital_status', 'occupation',
        'annual_income', 'education_level', 'credit_score', 'years_with_company',
        'previous_claims', 'policy_type', 'policy_start_date', 'policy_duration_years',
        'premium_amount', 'coverage_amount', 'deductible_plan', 'payment_method',
        'policy_active', 'incident_type', 'accident_severity', 'incident_location',
        'weather_condition', 'police_report', 'witnesses', 'injuries',
        'hospital_visit', 'property_damage', 'vehicle_damage', 'vehicle_make',
        'vehicle_model', 'vehicle_year', 'vehicle_age', 'mileage', 'vehicle_value',
        'ownership_type', 'suspicious_documents', 'claim_submitted_at_night',
        'multiple_claims_last_year', 'delayed_reporting', 'inconsistent_statements',
        'gps_location_match', 'repair_shop_verified', 'identity_verified',
        'claim_history_risk', 'fraud_risk_score', 'repair_cost', 'medical_cost',
        'towing_cost', 'rental_vehicle_cost', 'total_loss', 'payout_amount', 'fraudulent'
    ]

    missing_cols = set(expected_cols) - set(df.columns)
    assert len(missing_cols) == 0, f"Missing target columns: {missing_cols}"
    print("✓ All 61 specified feature columns and target label are correctly aligned.")

    print("\nSUCCESS: All dataset integrity assertions passed!")

if __name__ == "__main__":
    run_validations()
