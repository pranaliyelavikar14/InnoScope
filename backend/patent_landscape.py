import json
import os

from query_generator import generate_patent_queries
from patent_search import search_patents
from result_filter import filter_relevant_patents


DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data"
)

PATENT_FILE = os.path.join(
    DATA_DIR,
    "patent_results.json"
)


def save_patents(patents):
    """Save patent results locally as JSON."""

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(PATENT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            patents,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_patents():
    """Load previously saved patent results."""

    if not os.path.exists(PATENT_FILE):
        return None

    with open(PATENT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_and_cache_patents(idea):
    """
    Search patents using SerpApi and save the results locally.

    This function makes actual API calls.
    """

    queries = generate_patent_queries(idea)

    all_patents = []

    for query in queries:

        print(f"\n🔎 Searching SerpApi: {query}")

        patents = search_patents(
            query,
            limit=10
        )

        for patent in patents:
            patent["search_query"] = query

        all_patents.extend(patents)

    # Remove duplicate patents using patent ID
    unique_patents = {}

    for patent in all_patents:

        patent_id = patent.get("patent_id")

        if patent_id:
            unique_patents[patent_id] = patent

    patents = list(unique_patents.values())

    save_patents(patents)

    print(
        f"\n💾 Saved {len(patents)} unique patents to:"
    )
    print(PATENT_FILE)

    return patents


def get_patent_data(idea):
    """
    Get patent data.

    Use cached data if available.
    Otherwise perform a SerpApi search.
    """

    cached_patents = load_patents()

    if cached_patents is not None:

        print("📂 Loading patents from local JSON...")

        return cached_patents

    print("🌐 No local patent data found.")

    return search_and_cache_patents(idea)


def build_patent_landscape(idea):
    """
    Build a ranked patent landscape
    using locally available patent data.
    """

    # Get patent data
    patents = get_patent_data(idea)

    # Generate queries for transparency/debugging
    queries = generate_patent_queries(idea)

    print("\n" + "=" * 60)
    print("GENERATED SEARCH QUERIES")
    print("=" * 60)

    for i, query in enumerate(queries, start=1):
        print(f"{i}. {query}")

    # Filter and rank patents
    relevant_patents = filter_relevant_patents(patents)

    return relevant_patents


if __name__ == "__main__":

    idea = "AI system for detecting potholes using smartphone camera and GPS"

    relevant_patents = build_patent_landscape(idea)

    print("\n" + "=" * 60)
    print("PATENT LANDSCAPE")
    print("=" * 60)

    print(
        f"\nRelevant patents found: "
        f"{len(relevant_patents)}"
    )

    print("\nShowing top 10 most relevant patents:\n")

    for i, patent in enumerate(
        relevant_patents[:10],
        start=1
    ):

        print(f"{i}. {patent['title']}")
        print(f"   Patent ID: {patent['patent_id']}")
        print(
            f"   Relevance Score: "
            f"{patent['relevance_score']}"
        )
        print(
            f"   Matched Keywords: "
            f"{', '.join(patent['matched_keywords'])}"
        )
        print(f"   Link: {patent['link']}")
        print("-" * 60)