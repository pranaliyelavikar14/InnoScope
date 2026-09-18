import hashlib
import json
import os

from query_generator import generate_patent_queries
from patent_search import search_patents
from result_filter import filter_relevant_patents


DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data"
)

CACHE_DIR = os.path.join(
    DATA_DIR,
    "patent_cache"
)


def get_cache_path(idea):
    """
    Generate a unique cache file path for each idea.

    A SHA-256 hash is used so that the cache filename
    remains safe even when the idea contains spaces
    or special characters.
    """

    normalized_idea = " ".join(
        idea.lower().split()
    ).strip()

    idea_hash = hashlib.sha256(
        normalized_idea.encode("utf-8")
    ).hexdigest()[:16]

    os.makedirs(
        CACHE_DIR,
        exist_ok=True
    )

    return os.path.join(
        CACHE_DIR,
        f"{idea_hash}.json"
    )


def save_patents(idea, patents):
    """
    Save patent results to an idea-specific cache file.
    """

    cache_path = get_cache_path(
        idea
    )

    cache_data = {
        "idea": idea,
        "patents": patents
    }

    with open(
        cache_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cache_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    return cache_path


def load_patents(idea):
    """
    Load patent results from the cache for the
    specific technology idea.

    Returns None if no cache exists.
    """

    cache_path = get_cache_path(
        idea
    )

    if not os.path.exists(
        cache_path
    ):
        return None

    with open(
        cache_path,
        "r",
        encoding="utf-8"
    ) as file:

        cache_data = json.load(
            file
        )

    return cache_data.get(
        "patents",
        []
    )


def search_and_cache_patents(idea):
    """
    Search patents using SerpApi and save the
    results in an idea-specific cache.

    IMPORTANT:
    This function makes actual SerpApi API calls.
    """

    queries = generate_patent_queries(
        idea
    )

    all_patents = []

    for query in queries:

        print(
            f"\n🔎 Searching SerpApi: {query}"
        )

        patents = search_patents(
            query,
            limit=10
        )

        for patent in patents:

            patent["search_query"] = query

        all_patents.extend(
            patents
        )

    # Remove duplicate patents using patent ID
    unique_patents = {}

    for patent in all_patents:

        patent_id = patent.get(
            "patent_id"
        )

        if patent_id:

            unique_patents[
                patent_id
            ] = patent

    patents = list(
        unique_patents.values()
    )

    cache_path = save_patents(
        idea,
        patents
    )

    print(
        f"\n💾 Saved {len(patents)} "
        f"unique patents to:"
    )

    print(cache_path)

    return patents


def get_patent_data(idea):
    """
    Get patent data for a specific idea.

    Uses the idea-specific local cache if available.
    Otherwise, performs a SerpApi search.
    """

    cached_patents = load_patents(
        idea
    )

    if cached_patents is not None:

        print(
            "📂 Loading patents from "
            "local cache..."
        )

        return cached_patents

    print(
        "🌐 No local cache found for this idea."
    )

    return search_and_cache_patents(
        idea
    )


def build_patent_landscape(idea):
    """
    Build a ranked patent landscape for
    the given technology idea.
    """

    # Get idea-specific patent data
    patents = get_patent_data(
        idea
    )

    # Generate queries for transparency/debugging
    queries = generate_patent_queries(
        idea
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "GENERATED SEARCH QUERIES"
    )

    print(
        "=" * 60
    )

    for i, query in enumerate(
        queries,
        start=1
    ):

        print(
            f"{i}. {query}"
        )

    # Filter and rank patents dynamically
    # based on the current idea
    relevant_patents = (
        filter_relevant_patents(
            patents,
            idea
        )
    )

    return relevant_patents


if __name__ == "__main__":

    idea = (
        "AI system for detecting potholes "
        "using smartphone camera and GPS"
    )

    relevant_patents = (
        build_patent_landscape(
            idea
        )
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "PATENT LANDSCAPE"
    )

    print(
        "=" * 60
    )

    print(
        f"\nRelevant patents found: "
        f"{len(relevant_patents)}"
    )

    print(
        "\nShowing top 10 most relevant "
        "patents:\n"
    )

    for i, patent in enumerate(
        relevant_patents[:10],
        start=1
    ):

        print(
            f"{i}. {patent['title']}"
        )

        print(
            f"   Patent ID: "
            f"{patent['patent_id']}"
        )

        print(
            f"   Relevance Score: "
            f"{patent['relevance_score']}"
        )

        print(
            f"   Matched Keywords: "
            f"{', '.join(patent['matched_keywords'])}"
        )

        print(
            f"   Link: {patent['link']}"
        )

        print(
            "-" * 60
        )