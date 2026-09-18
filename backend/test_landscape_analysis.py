import json

from patent_landscape import build_patent_landscape
from patent_analyzer import analyze_patent
from landscape_analyzer import analyze_landscape


IDEA = (
    "AI system for detecting potholes "
    "using smartphone camera and GPS"
)

OUTPUT_FILE = "../data/landscape_result.json"


def main():
    print("=" * 70)
    print("INNOSCOPE - ACTUAL LANDSCAPE ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------
    # Step 1: Load relevant patents
    # --------------------------------------------------

    print("\n[1] Loading relevant patents...")

    relevant_patents = build_patent_landscape(
        IDEA
    )

    print(
        f"\nRelevant patents found: "
        f"{len(relevant_patents)}"
    )

    # --------------------------------------------------
    # Step 2: Analyze each patent individually
    # --------------------------------------------------

    print("\n[2] Analyzing individual patents...")

    patent_analyses = []

    for index, patent in enumerate(
        relevant_patents,
        start=1
    ):
        analysis = analyze_patent(
            patent,
            IDEA
        )

        patent_analyses.append(
            analysis
        )

        print(
            f"{index}. "
            f"{analysis['title']}"
        )

        print(
            f"   Similarity: "
            f"{analysis['similarity']}"
        )

    # --------------------------------------------------
    # Step 3: Build overall landscape
    # --------------------------------------------------

    print("\n[3] Building overall landscape...")

    landscape = analyze_landscape(
        patent_analyses
    )

    # --------------------------------------------------
    # Step 4: Save landscape result
    # --------------------------------------------------

    print("\n[4] Saving landscape result...")

    result = {
        "idea": IDEA,
        "patent_analyses": patent_analyses,
        "landscape": landscape,
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"✅ Landscape result saved to: "
        f"{OUTPUT_FILE}"
    )

    # --------------------------------------------------
    # Step 5: Display summary
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("LANDSCAPE SUMMARY")
    print("=" * 70)

    print(
        f"\nTotal patents analyzed: "
        f"{landscape['total_patents']}"
    )

    print(
        "\nSimilarity distribution:"
    )

    print(
        landscape[
            "similarity_distribution"
        ]
    )

    print(
        "\nCommon technologies:"
    )

    for technology in landscape[
        "common_technologies"
    ]:
        print(
            f"- {technology}"
        )

    print(
        "\nCommon actions:"
    )

    for action in landscape[
        "common_actions"
    ]:
        print(
            f"- {action}"
        )

    print(
        "\nPotential differentiation:"
    )

    for item in landscape[
        "potential_differentiation"
    ]:
        print(
            f"- {item}"
        )


if __name__ == "__main__":
    main()