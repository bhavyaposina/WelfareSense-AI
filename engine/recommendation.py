def calculate_recommendation_score(gap_analysis):
    """
    Calculate a recommendation score from the
    percentage of satisfied criteria.

    100 = all criteria satisfied
    0   = no criteria satisfied
    """

    total = gap_analysis["total_criteria"]

    if total == 0:
        return 0

    matched = gap_analysis["matched_criteria"]

    return round((matched / total) * 100, 2)


def generate_guidance(scheme, gap_analysis):
    """
    Generate actionable guidance for a scheme.
    """

    score = calculate_recommendation_score(
        gap_analysis
    )

    if gap_analysis["status"] == "Eligible":

        return {
            "message": (
                f"You currently satisfy the evaluated criteria "
                f"for {scheme['name']}."
            ),
            "action": scheme["guidance"],
            "recommendation_score": score
        }

    unmet_names = [
        item["criterion"]
        for item in gap_analysis["unmet"]
    ]

    return {
        "message": (
            "The following eligibility gaps were identified: "
            + ", ".join(unmet_names)
            + "."
        ),
        "action": scheme["guidance"],
        "recommendation_score": score
    }


def rank_recommendations(results):
    """
    Rank opportunities according to their
    eligibility match score.

    Eligible opportunities appear first.
    """

    for result in results:

        result["recommendation_score"] = (
            calculate_recommendation_score(
                result["gap_analysis"]
            )
        )

    results.sort(
        key=lambda item: (
            item["recommendation_score"],
            -item["gap_analysis"]["gap_score"]
        ),
        reverse=True
    )

    return results