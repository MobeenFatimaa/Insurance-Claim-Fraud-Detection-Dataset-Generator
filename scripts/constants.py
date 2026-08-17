"""
constants.py
Defines configuration constants, feature domain options, generation parameters,
and fraud weighting metrics for synthetic dataset generation.
"""

NUM_SAMPLES = 100_000
RANDOM_SEED = 42

# Target Class Imbalance Target (Approximate)
TARGET_FRAUD_RATIO = 0.20
FRAUD_SCORE_THRESHOLD = 22  # Calibrated to achieve ~20% fraud rate

# Date Ranges
START_DATE = "2021-01-01"
END_DATE = "2025-12-31"

# Feature Categorical Mappings
CATEGORIES = {
    "claim_status": ["Pending", "Under Review", "Approved", "Denied", "Closed"],
    "gender": ["Male", "Female", "Non-Binary", "Prefer Not to Say"],
    "marital_status": ["Single", "Married", "Divorced", "Widowed"],
    "occupation": [
        "Software Engineer", "Doctor", "Teacher", "Mechanic", "Accountant",
        "Manager", "Sales Representative", "Nurse", "Lawyer", "Self-Employed",
        "Construction Worker", "Retired", "Student", "Other"
    ],
    "education_level": ["High School", "Associate", "Bachelor", "Master", "Doctorate"],
    "policy_type": ["Comprehensive", "Collision", "Liability Only", "Personal Injury Protection", "Uninsured Motorist"],
    "deductible_plan": ["Low ($250)", "Standard ($500)", "High ($1,000)", "Premium ($2,500)"],
    "payment_method": ["Credit Card", "Debit Card", "Bank Transfer", "Auto-Debit", "Check"],
    "incident_type": ["Single Vehicle Collision", "Multi-Vehicle Collision", "Parked Vehicle", "Theft", "Vandalism", "Animal Impact"],
    "accident_severity": ["Minor", "Moderate", "Major", "Total Loss"],
    "incident_location": ["Urban", "Suburban", "Rural", "Highway", "Parking Lot"],
    "weather_condition": ["Clear", "Rainy", "Snowy", "Foggy", "Icy", "Windy"],
    "vehicle_damage": ["None", "Front Bump", "Rear Bump", "Side Impact", "Rollover", "Severe Structural"],
    "vehicle_make_models": {
        "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma"],
        "Honda": ["Civic", "CR-V", "Accord", "Pilot", "Odyssey"],
        "Ford": ["F-150", "Escape", "Explorer", "Mustang", "Focus"],
        "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe", "Cruze"],
        "BMW": ["3 Series", "5 Series", "X3", "X5", "M4"],
        "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "S-Class"],
        "Hyundai": ["Elantra", "Tucson", "Sonata", "Santa Fe"],
        "Tesla": ["Model 3", "Model Y", "Model S", "Model X"]
    },
    "ownership_type": ["Owned", "Financed", "Leased"],
    "claim_history_risk": ["Low", "Medium", "High"]
}

# Numerical Distributions Setup
RANGES = {
    "age": (18, 85),
    "annual_income": (25000, 250000),
    "credit_score": (300, 850),
    "years_with_company": (0, 30),
    "previous_claims": (0, 8),
    "policy_duration_years": (1, 10),
    "premium_amount": (500, 4500),
    "coverage_amount": (10000, 250000),
    "mileage": (5000, 250000),
    "vehicle_year": (2005, 2025),
    "witnesses": (0, 5),
    "injuries": (0, 6)
}

# Weighted logic for realistic Fraud Classification
FRAUD_WEIGHTS = {
    "suspicious_documents": 25,
    "identity_verified": 20,         # Applies if 'No'
    "gps_location_match": 15,        # Applies if 'No'
    "inconsistent_statements": 15,
    "delayed_reporting": 10,
    "no_police_report": 10,           # Applies if 'No'
    "multiple_previous_claims": 10,   # Applies if previous_claims > 2
    "claim_submitted_at_night": 8,
    "high_claim_amount": 8,           # Applies if claim_amount > $35,000
    "repair_shop_verified": 6         # Applies if 'No'
}
