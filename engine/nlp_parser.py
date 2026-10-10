
import re


def parse_profile(text):
    text = (text or "").strip()
    lower = text.lower()

    profile = {
        "name": "",
        "age": 0,
        "income": 0,
        "occupation": "",
        "education": "",
        "state": "",
        "category": "",
        "area": "",
        "service_type": ""
    }

    # Name
    match = re.search(
        r"\bmy name is\s+([a-zA-Z]+(?:\s+[a-zA-Z]+){0,3})",
        text,
        re.IGNORECASE
    )
    if match:
        name = re.split(
            r"\s+(?:i am|i'm|and|my age is|age is)\b",
            match.group(1),
            maxsplit=1,
            flags=re.IGNORECASE
        )[0]
        profile["name"] = name.strip()

    # Age: 20 years old, 20 years, age 20, I am 20
    match = re.search(
        r"\b(?:(?:i am|i'm|age is|aged)\s*)?"
        r"(\d{1,3})\s*(?:years?\s*old|yrs?\s*old|years?|yrs?)\b",
        lower
    )

    if not match:
        match = re.search(
            r"\b(?:age(?:\s+is)?|aged)\s*[:=]?\s*(\d{1,3})\b",
            lower
        )

    if not match:
        match = re.search(
            r"\bi am\s+(\d{1,3})\b",
            lower
        )

    if match:
        age = int(match.group(1))
        if 0 <= age <= 120:
            profile["age"] = age

    # Annual income
    number_pattern = r"(\d+(?:,\d{3})*(?:\.\d+)?)"
    unit_pattern = (
        r"(lakh|lakhs|lac|lacs|crore|crores|"
        r"thousand|thousands|k)?"
    )

    income_patterns = [
        rf"\b(?:annual\s+(?:family\s+)?income|family\s+income|"
        rf"income|earnings?|salary)\s*"
        rf"(?:is|of|:|=)?\s*(?:rs\.?|inr|₹)?\s*"
        rf"{number_pattern}\s*{unit_pattern}\b",

        rf"(?:rs\.?|inr|₹)\s*"
        rf"{number_pattern}\s*{unit_pattern}\b",

        rf"\b{number_pattern}\s*"
        rf"(lakh|lakhs|lac|lacs|crore|crores|"
        rf"thousand|thousands|k)\b"
    ]

    for pattern in income_patterns:
        match = re.search(pattern, lower, re.IGNORECASE)
        if not match:
            continue

        amount = float(match.group(1).replace(",", ""))
        unit = (match.group(2) or "").lower()

        if unit in ("lakh", "lakhs", "lac", "lacs"):
            amount *= 100000
        elif unit in ("crore", "crores"):
            amount *= 10000000
        elif unit in ("thousand", "thousands", "k"):
            amount *= 1000

        profile["income"] = int(amount)
        break

    # Occupation
    occupation_options = [
        ("business owner", "business owner"),
        ("self-employed", "self-employed"),
        ("self employed", "self-employed"),
        ("daily wage worker", "daily wage worker"),
        ("unemployed", "unemployed"),
        ("job seeker", "job seeker"),
        ("homemaker", "homemaker"),
        ("student", "student"),
        ("employee", "employee"),
        ("farmer", "farmer")
    ]

    for keyword, value in occupation_options:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lower):
            profile["occupation"] = value
            break

    # Education
    education_options = [
        ("postgraduate", "postgraduate"),
        ("post graduate", "postgraduate"),
        ("undergraduate", "undergraduate"),
        ("under graduate", "undergraduate"),
        ("school student", "school student"),
        ("intermediate", "intermediate"),
        ("graduate", "graduate"),
        ("diploma", "diploma"),
        ("illiterate", "illiterate"),
        ("12th", "12th"),
        ("10th", "10th")
    ]

    for keyword, value in education_options:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lower):
            profile["education"] = value
            break

    # State
    states = [
        "andhra pradesh", "telangana", "karnataka",
        "tamil nadu", "uttar pradesh", "madhya pradesh",
        "west bengal", "himachal pradesh", "uttarakhand",
        "maharashtra", "kerala", "delhi", "rajasthan",
        "gujarat", "bihar", "odisha", "punjab", "haryana",
        "assam", "jharkhand", "chhattisgarh", "goa"
    ]

    for state in states:
        if re.search(r"\b" + re.escape(state) + r"\b", lower):
            profile["state"] = state.title()
            break

    # Social category
    category_patterns = [
        (r"\bobc\b", "OBC"),
        (r"\bsc\b", "SC"),
        (r"\bst\b", "ST"),
        (r"\bews\b", "EWS"),
        (r"\bgeneral\s+category\b", "General"),
        (r"\bgeneral\b", "General")
    ]

    for pattern, value in category_patterns:
        if re.search(pattern, lower):
            profile["category"] = value
            break

    # Area
    if re.search(r"\burban\b|\bcity\b", lower):
        profile["area"] = "Urban"
    elif re.search(r"\brural\b|\bvillage\b", lower):
        profile["area"] = "Rural"

    # Service type
    service_options = [
        ("scholarship", "scholarship"),
        ("competitive exam", "exam"),
        ("competitive examination", "exam"),
        ("examination", "exam"),
        ("employment", "job"),
        ("government job", "job"),
        ("job", "job"),
        ("welfare", "welfare"),
        ("skill development", "skill"),
        ("skill", "skill"),
        ("exam", "exam")
    ]

    for keyword, value in service_options:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lower):
            profile["service_type"] = value
            break

    return profile
