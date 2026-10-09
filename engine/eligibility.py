import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMES_FILE = os.path.join(BASE_DIR, "data", "schemes.json")


def load_schemes():
    """Load scheme information from schemes.json."""
    with open(SCHEMES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def check_criterion(user, criteria, criterion_name):
    """
    Check one eligibility criterion.

    Returns:
        matched: True/False
        reason: explanation
    """

    if criterion_name == "age_min":
        if user["age"] >= criteria["age_min"]:
            return True, f"Age {user['age']} meets the minimum requirement."
        return False, (
            f"Minimum age required is {criteria['age_min']}, "
            f"but the applicant is {user['age']}."
        )

    if criterion_name == "age_max":
        if user["age"] <= criteria["age_max"]:
            return True, f"Age {user['age']} is within the permitted age limit."
        return False, (
            f"Maximum age allowed is {criteria['age_max']}, "
            f"but the applicant is {user['age']}."
        )

    if criterion_name == "income_max":
        if user["income"] <= criteria["income_max"]:
            return True, (
                f"Annual income ₹{user['income']:,} is within "
                f"the permitted limit of ₹{criteria['income_max']:,}."
            )
        return False, (
            f"Income limit is ₹{criteria['income_max']:,}, "
            f"but the applicant's income is ₹{user['income']:,}."
        )

    if criterion_name == "education":
        if user["education"] in criteria["education"]:
            return True, (
                f"Education level '{user['education']}' "
                "matches the requirement."
            )
        return False, (
            f"Required education levels include: "
            f"{', '.join(criteria['education'])}."
        )

    if criterion_name == "occupation":
        if user["occupation"] in criteria["occupation"]:
            return True, (
                f"Occupation '{user['occupation']}' "
                "matches the requirement."
            )
        return False, (
            f"Eligible occupations include: "
            f"{', '.join(criteria['occupation'])}."
        )

    if criterion_name == "category":
        if user["category"] in criteria["category"]:
            return True, "Social category satisfies the requirement."
        return False, "The applicant's social category does not match."

    if criterion_name == "area":
        if user["area"] in criteria["area"]:
            return True, f"Area '{user['area']}' matches the requirement."
        return False, (
            f"This opportunity is intended for: "
            f"{', '.join(criteria['area'])} areas."
        )

    return True, "Criterion was not evaluated."


def analyze_scheme(user, scheme):
    """
    Analyze a user's profile against one scheme.

    Returns criterion-level results.
    """

    criteria = scheme["criteria"]

    results = []

    # Age minimum
    if "age_min" in criteria:
        matched, reason = check_criterion(
            user, criteria, "age_min"
        )

        results.append({
            "criterion": "Minimum Age",
            "matched": matched,
            "reason": reason
        })

    # Age maximum
    if "age_max" in criteria:
        matched, reason = check_criterion(
            user, criteria, "age_max"
        )

        results.append({
            "criterion": "Maximum Age",
            "matched": matched,
            "reason": reason
        })

    # Income
    if "income_max" in criteria:
        matched, reason = check_criterion(
            user, criteria, "income_max"
        )

        results.append({
            "criterion": "Income",
            "matched": matched,
            "reason": reason
        })

    # Education
    if "education" in criteria:
        matched, reason = check_criterion(
            user, criteria, "education"
        )

        results.append({
            "criterion": "Education",
            "matched": matched,
            "reason": reason
        })

    # Occupation
    if "occupation" in criteria:
        matched, reason = check_criterion(
            user, criteria, "occupation"
        )

        results.append({
            "criterion": "Occupation",
            "matched": matched,
            "reason": reason
        })

    # Category
    if "category" in criteria:
        matched, reason = check_criterion(
            user, criteria, "category"
        )

        results.append({
            "criterion": "Social Category",
            "matched": matched,
            "reason": reason
        })

    # Area
    if "area" in criteria:
        matched, reason = check_criterion(
            user, criteria, "area"
        )

        results.append({
            "criterion": "Area",
            "matched": matched,
            "reason": reason
        })

    return results