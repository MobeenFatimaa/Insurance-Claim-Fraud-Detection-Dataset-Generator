"""
utils.py
Helper functions to maintain logical dependencies between variables
(e.g., deductible correlation, cost alignment, policy active windows).
"""

import datetime
import numpy as np

def calculate_vehicle_age(vehicle_year: int, reference_year: int = 2026) -> int:
    """Calculates vehicle age relative to dataset baseline."""
    return max(0, reference_year - vehicle_year)

def calculate_deductible_value(deductible_plan: str) -> float:
    """Extracts numeric deductible from categorical selection."""
    mapping = {
        "Low ($250)": 250.0,
        "Standard ($500)": 500.0,
        "High ($1,000)": 1000.0,
        "Premium ($2,500)": 2500.0
    }
    return mapping.get(deductible_plan, 500.0)

def generate_financials(accident_severity: str, vehicle_value: float):
    """
    Generates interconnected cost figures that logically align
    with incident severity and vehicle value.
    """
    severity_multipliers = {
        "Minor": (0.02, 0.10, 0.0, 0.20),
        "Moderate": (0.10, 0.30, 0.2, 0.50),
        "Major": (0.30, 0.70, 0.6, 0.80),
        "Total Loss": (0.85, 1.10, 0.9, 1.0)
    }

    low_m, high_m, med_prob, tow_prob = severity_multipliers.get(
        accident_severity, (0.1, 0.3, 0.2, 0.3)
    )

    # Base repair cost scaled to vehicle value
    repair_cost = round(float(np.random.uniform(low_m, high_m) * vehicle_value), 2)

    # Medical cost probability and generation
    medical_cost = 0.0
    if np.random.rand() < med_prob:
        medical_cost = round(float(np.random.exponential(scale=3500) + 500), 2)

    # Towing and Rental Costs
    towing_cost = round(float(np.random.uniform(75, 450)), 2) if np.random.rand() < tow_prob else 0.0
    rental_vehicle_cost = round(float(np.random.uniform(150, 1200)), 2) if repair_cost > 1500 else 0.0

    total_claim_raw = repair_cost + medical_cost + towing_cost + rental_vehicle_cost
    total_loss = "Yes" if accident_severity == "Total Loss" or repair_cost >= 0.8 * vehicle_value else "No"

    return repair_cost, medical_cost, towing_cost, rental_vehicle_cost, total_loss, total_claim_raw

def compute_fraud_metrics(row_dict: dict) -> tuple[int, str]:
    """
    Calculates dynamic fraud risk score (0-100) based on weighted risk indicators
    and determines final target label ('Yes'/'No').
    """
    score = 0
    from constants import FRAUD_WEIGHTS, FRAUD_SCORE_THRESHOLD

    if row_dict["suspicious_documents"] == "Yes":
        score += FRAUD_WEIGHTS["suspicious_documents"]
    if row_dict["identity_verified"] == "No":
        score += FRAUD_WEIGHTS["identity_verified"]
    if row_dict["gps_location_match"] == "No":
        score += FRAUD_WEIGHTS["gps_location_match"]
    if row_dict["inconsistent_statements"] == "Yes":
        score += FRAUD_WEIGHTS["inconsistent_statements"]
    if row_dict["delayed_reporting"] == "Yes":
        score += FRAUD_WEIGHTS["delayed_reporting"]
    if row_dict["police_report"] == "No" and row_dict["accident_severity"] in ["Major", "Total Loss"]:
        score += FRAUD_WEIGHTS["no_police_report"]
    if row_dict["previous_claims"] > 2:
        score += FRAUD_WEIGHTS["multiple_previous_claims"]
    if row_dict["claim_submitted_at_night"] == "Yes":
        score += FRAUD_WEIGHTS["claim_submitted_at_night"]
    if row_dict["claim_amount"] > 35000:
        score += FRAUD_WEIGHTS["high_claim_amount"]
    if row_dict["repair_shop_verified"] == "No":
        score += FRAUD_WEIGHTS["repair_shop_verified"]

    # Stochastic noise factor to prevent rigid decision boundaries
    noise = int(np.random.normal(0, 4))
    final_score = int(np.clip(score + noise, 0, 100))

    fraud_label = "Yes" if final_score >= FRAUD_SCORE_THRESHOLD else "No"
    return final_score, fraud_label
