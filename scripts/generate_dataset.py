"""
generate_dataset.py
Main generation script utilizing Pandas, Numpy, and Faker to assemble
100,000 structured claims with 60 features and correlated logic.
"""

import os
import pandas as pd
import numpy as np
from faker import Faker
from tqdm import tqdm
from datetime import datetime, timedelta

from constants import (
    NUM_SAMPLES, RANDOM_SEED, CATEGORIES, RANGES,
    START_DATE, END_DATE
)
from utils import (
    calculate_vehicle_age, calculate_deductible_value,
    generate_financials, compute_fraud_metrics
)

# Seed Initialization for Reproducibility
np.random.seed(RANDOM_SEED)
fake = Faker()
Faker.seed(RANDOM_SEED)

def build_dataset() -> pd.DataFrame:
    print(f"Generating {NUM_SAMPLES:,} primary synthetic records...")

    start_dt = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_dt = datetime.strptime(END_DATE, "%Y-%m-%d")
    date_delta_days = (end_dt - start_dt).days

    records = []

    for i in tqdm(range(1, NUM_SAMPLES + 1), desc="Building Data"):
        # 1. Primary Identifiers
        claim_id = f"CLM-{i:07d}"
        policy_id = f"POL-{np.random.randint(10000000, 99999999)}"
        customer_id = f"CUST-{np.random.randint(100000, 999999)}"

        # 2. Customer Information
        customer_name = fake.name().replace("NA", "N.A.")
        age = int(np.random.randint(RANGES["age"][0], RANGES["age"][1]))
        gender = np.random.choice(CATEGORIES["gender"], p=[0.48, 0.48, 0.02, 0.02])
        marital_status = np.random.choice(CATEGORIES["marital_status"])
        occupation = np.random.choice(CATEGORIES["occupation"])
        annual_income = round(float(np.random.uniform(RANGES["annual_income"][0], RANGES["annual_income"][1])), 2)
        education_level = np.random.choice(CATEGORIES["education_level"])
        credit_score = int(np.random.randint(RANGES["credit_score"][0], RANGES["credit_score"][1]))
        years_with_company = int(np.random.randint(0, min(30, max(1, age - 18))))
        previous_claims = int(np.random.poisson(lam=0.8))

        # 3. Insurance Policy Details
        policy_type = np.random.choice(CATEGORIES["policy_type"])
        pol_start_offset = np.random.randint(30, 1800)
        inc_offset = np.random.randint(0, date_delta_days)

        incident_dt = start_dt + timedelta(days=inc_offset)
        policy_start_dt = incident_dt - timedelta(days=pol_start_offset)

        # Reporting Delay
        reporting_delay = int(np.random.exponential(scale=2))
        claim_dt = incident_dt + timedelta(days=reporting_delay)

        policy_duration_years = int(np.random.randint(RANGES["policy_duration_years"][0], RANGES["policy_duration_years"][1]))
        premium_amount = round(float(np.random.uniform(RANGES["premium_amount"][0], RANGES["premium_amount"][1])), 2)
        coverage_amount = round(float(np.random.uniform(RANGES["coverage_amount"][0], RANGES["coverage_amount"][1])), 2)
        deductible_plan = np.random.choice(CATEGORIES["deductible_plan"])
        deductible = calculate_deductible_value(deductible_plan)
        payment_method = np.random.choice(CATEGORIES["payment_method"])

        policy_end_dt = policy_start_dt + timedelta(days=365 * policy_duration_years)
        policy_active = "Yes" if policy_start_dt <= incident_dt <= policy_end_dt else "No"

        # 4. Incident Details
        incident_type = np.random.choice(CATEGORIES["incident_type"])
        accident_severity = np.random.choice(CATEGORIES["accident_severity"], p=[0.4, 0.3, 0.2, 0.1])
        incident_location = np.random.choice(CATEGORIES["incident_location"])
        weather_condition = np.random.choice(CATEGORIES["weather_condition"])
        police_report = np.random.choice(["Yes", "No"], p=[0.65, 0.35])
        witnesses = int(np.random.randint(RANGES["witnesses"][0], RANGES["witnesses"][1]))
        injuries = int(np.random.poisson(lam=0.4)) if accident_severity in ["Moderate", "Major", "Total Loss"] else 0
        hospital_visit = "Yes" if injuries > 0 and np.random.rand() < 0.75 else "No"
        property_damage = np.random.choice(["Yes", "No"], p=[0.4, 0.6])
        vehicle_damage = np.random.choice(CATEGORIES["vehicle_damage"])

        # 5. Vehicle Information
        vehicle_make = np.random.choice(list(CATEGORIES["vehicle_make_models"].keys()))
        vehicle_model = np.random.choice(CATEGORIES["vehicle_make_models"][vehicle_make])
        vehicle_year = int(np.random.randint(RANGES["vehicle_year"][0], RANGES["vehicle_year"][1]))
        vehicle_age = calculate_vehicle_age(vehicle_year, reference_year=incident_dt.year)
        mileage = int(np.random.uniform(5000, 20000) * max(1, vehicle_age))
        vehicle_value = round(max(2000.0, 45000.0 * (0.88 ** vehicle_age)), 2)
        ownership_type = np.random.choice(CATEGORIES["ownership_type"])

        # 6. Financial Costs Calculations
        repair_cost, medical_cost, towing_cost, rental_vehicle_cost, total_loss, claim_amount = generate_financials(
            accident_severity, vehicle_value
        )

        claim_duration_days = int(np.random.randint(1, 45))

        # 7. Fraud Risk Indicator Mechanics
        suspicious_documents = np.random.choice(["Yes", "No"], p=[0.08, 0.92])
        claim_submitted_at_night = np.random.choice(["Yes", "No"], p=[0.15, 0.85])
        multiple_claims_last_year = "Yes" if previous_claims >= 2 else "No"
        delayed_reporting = "Yes" if reporting_delay > 5 else "No"
        inconsistent_statements = np.random.choice(["Yes", "No"], p=[0.09, 0.91])
        gps_location_match = np.random.choice(["Yes", "No"], p=[0.88, 0.12])
        repair_shop_verified = np.random.choice(["Yes", "No"], p=[0.85, 0.15])
        identity_verified = np.random.choice(["Yes", "No"], p=[0.92, 0.08])

        if previous_claims == 0:
            claim_history_risk = "Low"
        elif previous_claims in [1, 2]:
            claim_history_risk = "Medium"
        else:
            claim_history_risk = "High"

        # Temporary dictionary build to evaluate target state
        record = {
            "claim_id": claim_id, "policy_id": policy_id, "customer_id": customer_id,
            "customer_name": customer_name, "claim_date": claim_dt.strftime("%Y-%m-%d"),
            "incident_date": incident_dt.strftime("%Y-%m-%d"), "claim_status": np.random.choice(CATEGORIES["claim_status"]),
            "claim_amount": claim_amount, "approved_amount": 0.0, "deductible": deductible,
            "claim_duration_days": claim_duration_days, "age": age, "gender": gender,
            "marital_status": marital_status, "occupation": occupation, "annual_income": annual_income,
            "education_level": education_level, "credit_score": credit_score,
            "years_with_company": years_with_company, "previous_claims": previous_claims,
            "policy_type": policy_type, "policy_start_date": policy_start_dt.strftime("%Y-%m-%d"),
            "policy_duration_years": policy_duration_years, "premium_amount": premium_amount,
            "coverage_amount": coverage_amount, "deductible_plan": deductible_plan,
            "payment_method": payment_method, "policy_active": policy_active,
            "incident_type": incident_type, "accident_severity": accident_severity,
            "incident_location": incident_location, "weather_condition": weather_condition,
            "police_report": police_report, "witnesses": witnesses, "injuries": injuries,
            "hospital_visit": hospital_visit, "property_damage": property_damage,
            "vehicle_damage": vehicle_damage, "vehicle_make": vehicle_make,
            "vehicle_model": vehicle_model, "vehicle_year": vehicle_year,
            "vehicle_age": vehicle_age, "mileage": mileage, "vehicle_value": vehicle_value,
            "ownership_type": ownership_type, "suspicious_documents": suspicious_documents,
            "claim_submitted_at_night": claim_submitted_at_night,
            "multiple_claims_last_year": multiple_claims_last_year,
            "delayed_reporting": delayed_reporting, "inconsistent_statements": inconsistent_statements,
            "gps_location_match": gps_location_match, "repair_shop_verified": repair_shop_verified,
            "identity_verified": identity_verified, "claim_history_risk": claim_history_risk,
            "repair_cost": repair_cost, "medical_cost": medical_cost, "towing_cost": towing_cost,
            "rental_vehicle_cost": rental_vehicle_cost, "total_loss": total_loss
        }

        # 8. Compute Fraud Risk Score & Binary Target Label
        fraud_risk_score, fraudulent = compute_fraud_metrics(record)

        # Align approved amount and payout amount according to outcome
        if fraudulent == "Yes":
            payout_amount = 0.0
            approved_amount = 0.0
            record["claim_status"] = "Denied"
        else:
            payout_amount = round(max(0.0, claim_amount - deductible), 2)
            approved_amount = claim_amount if record["claim_status"] == "Approved" else round(claim_amount * 0.9, 2)

        record["fraud_risk_score"] = fraud_risk_score
        record["payout_amount"] = payout_amount
        record["approved_amount"] = approved_amount
        record["fraudulent"] = fraudulent

        records.append(record)

    df = pd.DataFrame(records)

    # Validate exact column ordering (60 total)
    expected_order = [
        "claim_id", "policy_id", "customer_id", "customer_name", "claim_date",
        "incident_date", "claim_status", "claim_amount", "approved_amount", "deductible",
        "claim_duration_days", "age", "gender", "marital_status", "occupation",
        "annual_income", "education_level", "credit_score", "years_with_company", "previous_claims",
        "policy_type", "policy_start_date", "policy_duration_years", "premium_amount", "coverage_amount",
        "deductible_plan", "payment_method", "policy_active", "incident_type", "accident_severity",
        "incident_location", "weather_condition", "police_report", "witnesses", "injuries",
        "hospital_visit", "property_damage", "vehicle_damage", "vehicle_make", "vehicle_model",
        "vehicle_year", "vehicle_age", "mileage", "vehicle_value", "ownership_type",
        "suspicious_documents", "claim_submitted_at_night", "multiple_claims_last_year",
        "delayed_reporting", "inconsistent_statements", "gps_location_match", "repair_shop_verified",
        "identity_verified", "claim_history_risk", "fraud_risk_score", "repair_cost",
        "medical_cost", "towing_cost", "rental_vehicle_cost", "total_loss", "payout_amount",
        "fraudulent"
    ]

    return df[expected_order]

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), "..", "dataset")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "insurance_claim_fraud_dataset.csv")

    df_generated = build_dataset()
    df_generated.to_csv(file_path, index=False)
    print(f"\nDataset saved successfully at: {file_path}")
