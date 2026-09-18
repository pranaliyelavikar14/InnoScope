from collections import Counter


def analyze_landscape(patent_analyses):
    """
    Build an overall technology landscape from
    individual patent analyses.

    This module is fully local.
    It does NOT make any SerpApi or LLM/API calls.
    """

    total_patents = len(patent_analyses)

    # --------------------------------------------------
    # 1. Similarity distribution
    # --------------------------------------------------

    similarity_counter = Counter()

    for patent in patent_analyses:
        similarity = patent.get("similarity", "Low")

        if similarity:
            similarity_counter[
                similarity.lower()
            ] += 1

    similarity_distribution = {
        "high": similarity_counter.get("high", 0),
        "medium": similarity_counter.get("medium", 0),
        "low": similarity_counter.get("low", 0),
    }

    # --------------------------------------------------
    # 2. Common technologies
    # --------------------------------------------------

    technology_counter = Counter()

    for patent in patent_analyses:
        technologies = patent.get(
            "key_technologies",
            []
        )

        for technology in technologies:
            if technology:
                cleaned_technology = (
                    technology
                    .strip()
                    .strip(".,;:")
                    .lower()
                )

                if cleaned_technology:
                    technology_counter[
                        cleaned_technology
                    ] += 1

    common_technologies = [
        technology
        for technology, count
        in technology_counter.most_common()
    ]

    # --------------------------------------------------
    # 3. Common actions
    # --------------------------------------------------

    action_counter = Counter()

    for patent in patent_analyses:
        actions = patent.get(
            "matched_actions",
            []
        )

        for action in actions:
            if action:
                cleaned_action = (
                    action
                    .strip()
                    .strip(".,;:")
                    .lower()
                )

                if cleaned_action:
                    action_counter[
                        cleaned_action
                    ] += 1

    common_actions = [
        action
        for action, count
        in action_counter.most_common()
    ]

    # --------------------------------------------------
    # 4. Common contexts
    # --------------------------------------------------

    context_counter = Counter()

    for patent in patent_analyses:
        contexts = patent.get(
            "matched_contexts",
            []
        )

        for context in contexts:
            if context:
                cleaned_context = (
                    context
                    .strip()
                    .strip(".,;:")
                    .lower()
                )

                if cleaned_context:
                    context_counter[
                        cleaned_context
                    ] += 1

    common_contexts = [
        context
        for context, count
        in context_counter.most_common()
    ]

    # --------------------------------------------------
    # 5. Overlap summary
    # --------------------------------------------------

    overlap_summary = build_overlap_summary(
        total_patents=total_patents,
        similarity_distribution=similarity_distribution,
        common_technologies=common_technologies,
        common_actions=common_actions,
        common_contexts=common_contexts,
    )

    # --------------------------------------------------
    # 6. Potential differentiation
    # --------------------------------------------------

    potential_differentiation = (
        build_potential_differentiation(
            patent_analyses
        )
    )

    # --------------------------------------------------
    # 7. Final landscape
    # --------------------------------------------------

    return {
        "total_patents": total_patents,
        "similarity_distribution": (
            similarity_distribution
        ),
        "common_technologies": (
            common_technologies
        ),
        "common_actions": (
            common_actions
        ),
        "common_contexts": (
            common_contexts
        ),
        "overlap_summary": overlap_summary,
        "potential_differentiation": (
            potential_differentiation
        ),
        "disclaimer": (
            "This landscape is based on publicly "
            "retrieved patent titles and snippets "
            "and is intended for technology research "
            "and exploration only. It is not legal "
            "advice or a patentability assessment."
        ),
    }


def build_overlap_summary(
    total_patents,
    similarity_distribution,
    common_technologies,
    common_actions,
    common_contexts,
):
    """
    Create a deterministic summary of observed overlap.
    """

    if total_patents == 0:
        return (
            "No relevant patents were identified "
            "for landscape analysis."
        )

    high = similarity_distribution["high"]
    medium = similarity_distribution["medium"]
    low = similarity_distribution["low"]

    parts = []

    parts.append(
        f"{total_patents} relevant patents were "
        f"analyzed."
    )

    if high > 0:
        parts.append(
            f"{high} showed high heuristic similarity."
        )

    if medium > 0:
        parts.append(
            f"{medium} showed medium heuristic similarity."
        )

    if low > 0:
        parts.append(
            f"{low} showed low heuristic similarity."
        )

    if common_actions:
        action_text = ", ".join(
            common_actions[:3]
        )

        parts.append(
            f"Commonly observed actions include "
            f"{action_text}."
        )

    if common_technologies:
        technology_text = ", ".join(
            common_technologies[:3]
        )

        parts.append(
            f"Commonly observed technologies include "
            f"{technology_text}."
        )

    if common_contexts:
        context_text = ", ".join(
            common_contexts[:3]
        )

        parts.append(
            f"Commonly observed contexts include "
            f"{context_text}."
        )

    return " ".join(parts)


def build_potential_differentiation(
    patent_analyses
):
    """
    Aggregate technology elements that were observed
    as missing from individual patent matches.

    This is not a claim that these elements are novel.
    """

    differentiation_counter = Counter()

    for patent in patent_analyses:
        differentiation_text = patent.get(
            "potential_differentiation",
            ""
        )

        if not differentiation_text:
            continue

        marker = (
            "Technology elements not explicitly "
            "matched in the retrieved text:"
        )

        if marker not in differentiation_text:
            continue

        missing_part = differentiation_text.split(
            marker,
            1
        )[1].strip()

        if not missing_part:
            continue

        elements = missing_part.split(",")

        for element in elements:
            cleaned_element = (
                element
                .strip()
                .strip(".,;:")
                .lower()
            )

            if cleaned_element:
                differentiation_counter[
                    cleaned_element
                ] += 1

    return [
        element
        for element, count
        in differentiation_counter.most_common()
    ]


if __name__ == "__main__":
    # Small local test

    sample_patents = [
        {
            "similarity": "High",
            "key_technologies": ["camera"],
            "matched_actions": ["detect"],
            "matched_contexts": ["roads"],
            "potential_differentiation": (
                "Technology elements not explicitly "
                "matched in the retrieved text: "
                "smartphone, gps."
            ),
        },
        {
            "similarity": "Medium",
            "key_technologies": ["smartphone"],
            "matched_actions": ["detect"],
            "matched_contexts": [],
            "potential_differentiation": (
                "Technology elements not explicitly "
                "matched in the retrieved text: "
                "camera, gps."
            ),
        },
    ]

    landscape = analyze_landscape(
        sample_patents
    )

    print("\nLandscape Analysis")
    print("=" * 60)

    for key, value in landscape.items():
        print(f"\n{key}:")
        print(value)