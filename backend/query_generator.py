from idea_analyzer import analyze_idea


# --------------------------------------------------
# Convert detected actions into natural search terms
# --------------------------------------------------

ACTION_QUERY_FORMS = {
    "detect": "detection",
    "identify": "identification",
    "classify": "classification",
    "predict": "prediction",
    "monitor": "monitoring",
    "track": "tracking",
    "translate": "translation",
    "analyze": "analysis",
    "recognize": "recognition",
    "forecast": "forecasting",
    "recommend": "recommendation",
}


def normalize_query(query):
    """
    Normalize a generated query for consistency.
    """

    query = " ".join(
        query.lower().split()
    ).strip()

    return query


def add_query(queries, query):
    """
    Add a query only if it is non-empty
    and not already present.
    """

    if not query:
        return

    query = " ".join(
        query.split()
    ).strip()

    if not query:
        return

    normalized = normalize_query(
        query
    )

    existing = {
        normalize_query(item)
        for item in queries
    }

    if normalized not in existing:
        queries.append(query)


def generate_patent_queries(idea):
    """
    Generate natural and generic patent-search
    queries from the analyzed technology idea.

    Query strategy:

    1. Core concept
    2. Core concept + action
    3. Core concept + action + technology
    4. Core concept + action + context
    5. Original idea

    This avoids weak queries such as:

        potholes smartphone
        battery degradation electric vehicles

    and prefers more informative combinations such as:

        potholes detection smartphone
        battery degradation prediction electric vehicles
    """

    analysis = analyze_idea(
        idea
    )

    core_concept = analysis.get(
        "core_concept"
    )

    actions = analysis.get(
        "actions",
        []
    )

    contexts = analysis.get(
        "contexts",
        []
    )

    technologies = analysis.get(
        "technologies",
        []
    )

    queries = []

    # --------------------------------------------------
    # 1. Core concept
    # --------------------------------------------------

    if core_concept:

        add_query(
            queries,
            core_concept
        )

    # --------------------------------------------------
    # 2. Core concept + action
    # --------------------------------------------------

    action_forms = []

    for action in actions:

        action_form = ACTION_QUERY_FORMS.get(
            action,
            action
        )

        action_forms.append(
            action_form
        )

        if core_concept:

            add_query(
                queries,
                f"{core_concept} {action_form}"
            )

    # --------------------------------------------------
    # 3. Core concept + action + technology
    # --------------------------------------------------

    if core_concept:

        for action_form in action_forms:

            for technology in technologies:

                add_query(
                    queries,
                    f"{core_concept} "
                    f"{action_form} "
                    f"{technology}"
                )

    # --------------------------------------------------
    # 4. Core concept + action + context
    # --------------------------------------------------

    if core_concept:

        for action_form in action_forms:

            for context in contexts:

                add_query(
                    queries,
                    f"{core_concept} "
                    f"{action_form} "
                    f"{context}"
                )

    # --------------------------------------------------
    # 5. If no action exists, use core + technology
    # --------------------------------------------------

    if core_concept and not actions:

        for technology in technologies:

            add_query(
                queries,
                f"{core_concept} {technology}"
            )

        for context in contexts:

            add_query(
                queries,
                f"{core_concept} {context}"
            )

    # --------------------------------------------------
    # 6. Original idea
    #
    # Keep one broad query representing the
    # user's original wording.
    # --------------------------------------------------

    add_query(
        queries,
        idea.strip()
    )

    return queries


# --------------------------------------------------
# Local testing
# --------------------------------------------------

if __name__ == "__main__":

    test_ideas = [
        "AI system for detecting potholes using smartphone camera and GPS",

        "AI system for detecting crop diseases from leaf images",

        "Smartphone application for translating Indian Sign Language",

        "AI system that predicts battery degradation in electric vehicles",
    ]

    for idea in test_ideas:

        print(
            "\n" + "=" * 70
        )

        print(
            "IDEA:"
        )

        print(
            idea
        )

        print(
            "=" * 70
        )

        queries = generate_patent_queries(
            idea
        )

        print(
            "\nGenerated Patent Search Queries:"
        )

        for i, query in enumerate(
            queries,
            start=1
        ):

            print(
                f"{i}. {query}"
            )