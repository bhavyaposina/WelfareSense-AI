def calculate_gap(criterion_results):
    """
    Calculate the eligibility gap.

    Gap = unmet criteria / total criteria
    """

    total = len(criterion_results)

    if total == 0:
        return 0

    unmet = sum(
        1
        for result in criterion_results
        if not result["matched"]
    )

    return round((unmet / total) * 100, 2)


def determine_status(gap):
    """
    Convert the gap percentage into an understandable status.
    """

    if gap == 0:
        return "Eligible"

    if gap <= 20:
        return "Near Eligible"

    if gap <= 50:
        return "Partially Eligible"

    return "Not Currently Eligible"


def generate_gap_analysis(criterion_results):
    """
    Produce the complete eligibility-gap analysis.
    """

    gap = calculate_gap(criterion_results)

    status = determine_status(gap)

    matched = [
        result
        for result in criterion_results
        if result["matched"]
    ]

    unmet = [
        result
        for result in criterion_results
        if not result["matched"]
    ]

    return {
        "gap_score": gap,
        "status": status,
        "total_criteria": len(criterion_results),
        "matched_criteria": len(matched),
        "unmet_criteria": len(unmet),
        "matched": matched,
        "unmet": unmet
    }