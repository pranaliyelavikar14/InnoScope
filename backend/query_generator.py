from idea_analyzer import analyze_idea


def generate_patent_queries(idea):
    """
    Generate generic patent search queries from the
    structured idea analysis.
    """

    analysis = analyze_idea(idea)

    core_concept = analysis["core_concept"]
    actions = analysis["actions"]
    contexts = analysis["contexts"]
    technologies = analysis["technologies"]

    queries = []

    # 1. Core concept
    if core_concept:
        queries.append(core_concept)

    # 2. Core concept + action
    if core_concept:
        for action in actions:
            queries.append(
                f"{core_concept} {action}"
            )

    # 3. Core concept + technology
    if core_concept:
        for technology in technologies:
            queries.append(
                f"{core_concept} {technology}"
            )

    # 4. Core concept + context
    if core_concept:
        for context in contexts:
            queries.append(
                f"{core_concept} {context}"
            )

    # 5. Core concept + action + technology
    if core_concept:
        for action in actions:
            for technology in technologies:
                queries.append(
                    f"{core_concept} {action} {technology}"
                )

    # 6. Original idea
    queries.append(idea)

    # Remove duplicates
    unique_queries = []

    for query in queries:

        query = query.strip()

        if query and query not in unique_queries:
            unique_queries.append(query)

    return unique_queries


if __name__ == "__main__":

    test_ideas = [

        "AI system for detecting potholes using smartphone camera and GPS",

        "AI system for detecting crop diseases from leaf images",

        "Smartphone application for translating Indian Sign Language",

        "AI system that predicts battery degradation in electric vehicles",

    ]

    for idea in test_ideas:

        print("\n" + "=" * 70)
        print("IDEA:")
        print(idea)
        print("=" * 70)

        queries = generate_patent_queries(idea)

        print("\nGenerated Patent Search Queries:")

        for i, query in enumerate(
            queries,
            start=1
        ):
            print(f"{i}. {query}")