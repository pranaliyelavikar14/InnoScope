from patent_landscape import build_patent_landscape
from patent_analyzer import analyze_patent


def main():

    idea = (
        "AI system for detecting potholes "
        "using smartphone camera and GPS"
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "ACTUAL PATENT ANALYSIS TEST"
    )

    print(
        "=" * 70
    )

    # Build landscape using the existing local cache
    relevant_patents = build_patent_landscape(
        idea
    )

    print(
        "\n" + "=" * 70
    )

    print(
        f"Relevant patents to analyze: "
        f"{len(relevant_patents)}"
    )

    print(
        "=" * 70
    )

    # Analyze each relevant patent
    for index, patent in enumerate(
        relevant_patents,
        start=1
    ):

        analysis = analyze_patent(
            patent,
            idea
        )

        print(
            "\n" + "-" * 70
        )

        print(
            f"PATENT {index}"
        )

        print(
            "-" * 70
        )

        print(
            f"\nTitle:\n"
            f"{analysis['title']}"
        )

        print(
            f"\nPatent ID:\n"
            f"{analysis['patent_id']}"
        )

        print(
            f"\nWhat it does:\n"
            f"{analysis['what_it_does']}"
        )

        print(
            f"\nKey technologies:\n"
            f"{', '.join(analysis['key_technologies']) or 'None'}"
        )

        print(
            f"\nMatched actions:\n"
            f"{', '.join(analysis['matched_actions']) or 'None'}"
        )

        print(
            f"\nMatched contexts:\n"
            f"{', '.join(analysis['matched_contexts']) or 'None'}"
        )

        print(
            f"\nOverlap:\n"
            f"{analysis['overlap']}"
        )

        print(
            f"\nSimilarity:\n"
            f"{analysis['similarity']}"
        )

        print(
            f"\nPotential differentiation:\n"
            f"{analysis['potential_differentiation']}"
        )


if __name__ == "__main__":

    main()