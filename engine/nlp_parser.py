
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
            r"\s+(?:i am|i'm|my age is)\b",
            match.group(1),
            maxsplit=1,
            flags=re.IGNORECASE
        )[0]
        profile["name"] = name.strip()

    # Age: "20 years old", "20 years", "age 20"
    match = re.search(
        r"\b(?:i am|i'm|age is|aged)?\s*(\d{1,3})"
        r"\s*(?:years?\s*old|yrs?\s*old|years?|yrs?)\b",
        lower
    )

    if not match:
        match = re.search(r"\b(?:age is|aged|age)\s*(\d{1,3})\b", lower)

    if match:
        age = int(match.group(1))
        if 0 <= age <= 120:
            profile["age"] = age

    # Annual income
    number_pattern = r"(\d+(?:,\d{3})*(?:\.\d+)?)"

    income_patterns = [
        rf"(?:annual\s+)?(?:income|earnings?|salary)"
        rf"\s*(?:is|of|:|=)?\s*(?:rs\.?|inr|₹)?\s*"
        rf"{number_pattern}\s*"
        rf"(lakh|lakhs|lac|lacs|crore|crores|thousand|thousands|k)?",

        rf"\b(?:rs\.?|inr|₹)\s*{number_pattern}\s*"
        rf"(lakh|lakhs|lac|lacs|crore|crores|thousand|thousands|k)?",

        rf"\b{number_pattern}\s*"
        rf"(lakh|lakhs|lac|lacs|crore|crores|thousand|thousands)"
        rf"(?:\s+rupees?)?\b"
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
        ("student", "student"),
        ("employee", "employee"),
        ("farmer", "farmer"),
        ("homemaker", "homemaker")
    ]

    for keyword, value in occupation_options:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lower):
            profile["occupation"] = value
            break

    # Education: longer terms first to prevent partial matches
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

    # Social category: use word boundaries so "sc" doesn't
    # accidentally match letters inside unrelated words.
    for keyword, value in [
        ("general", "General"),
        ("obc", "OBC"),
        ("ews", "EWS"),
        ("sc", "SC"),
        ("st", "ST")
    ]:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lower):
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
        ("employment", "job"),
        ("job", "job"),
        ("welfare", "welfare"),
        ("examination", "exam"),
        ("competitive exam", "exam"),
        ("exam", "exam"),
        ("skill development", "skill"),
        ("skill", "skill")
    ]

    for keyword, value in service_options:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lower):
            profile["service_type"] = value
            break

    return profile
