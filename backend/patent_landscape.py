import json
import os

from query_generator import generate_patent_queries
from patent_search import search_patents
from result_filter import filter_relevant_patents


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PATENT_FILE = os.path.join(DATA_DIR, "patent_results.json")


def save_patents(patents):
    """Save patent results locally as JSON."""

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(PATENT_FILE, "w", encoding="utf-8") as file:
        json.dump(patents, file, indent=4, ensure_ascii=False)


def load_patents():
    """Load previously saved patent results."""

    if not os.path.exists(PATENT_FILE):
        return None

    with open(PATENT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_patent_landscape(idea):
    """
    Build patent landscape.

    If local patent data already exists, use it.
    Otherwise, perform SerpApi searches once and save the results.
    """

    # Check local cache first
    cached_patents = load_patents()

    if cached_patents is not None:
        print("📂 Loading patents from local JSON...")
        return cached_patents

    print("🌐 No local patent data found.")
    print("🔎 Searching SerpApi for patents...")

    queries = generate_patent_queries(idea)

    all_patents = []

    for query in queries:

        print(f"\nSearching: {query}")

        patents = search_patents(query, limit=10)

        for patent in patents:
            patent["search_query"] = query

        all_patents.extend(patents)

    # Deduplicate using patent ID
    unique_patents = {}

    for patent in all_patents:

        patent_id = patent.get("patent_id")

        if patent_id:
            unique_patents[patent_id] = patent

    patents = list(unique_patents.values())

    # Save raw patent data locally
    save_patents(patents)

    print(f"\n💾 Saved {len(patents)} unique patents to:")
    print(PATENT_FILE)

    return patents


if __name__ == "__main__":

    idea = "pothole detection using smartphone camera and GPS"

    patents = build_patent_landscape(idea)

    print("\n" + "=" * 60)
    print("PATENT LANDSCAPE")
    print("=" * 60)

    relevant_patents = filter_relevant_patents(patents)

    print(f"\nRelevant patents found: {len(relevant_patents)}")
    print("Showing top 10 most relevant patents:\n")

    for i, patent in enumerate(relevant_patents[:10], start=1):

        print(f"{i}. {patent['title']}")
        print(f"   Patent ID: {patent['patent_id']}")
        print(f"   Relevance Score: {patent['relevance_score']}")
        print(f"   Matched Keywords: {', '.join(patent['matched_keywords'])}")
        print(f"   Link: {patent['link']}")
        print()