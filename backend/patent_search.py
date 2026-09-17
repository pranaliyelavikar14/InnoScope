import os
import serpapi
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERPAPI_KEY")

if not api_key:
    raise ValueError("SERPAPI_KEY not found in .env file")

client = serpapi.Client(api_key=api_key)


def search_patents(query, limit=10):
    """
    Search Google Patents using SerpApi.

    Args:
        query: Search query string.
        limit: Maximum number of results to return.

    Returns:
        List of structured patent results.
    """

    results = client.search({
        "engine": "google_patents",
        "q": query,
    })

    patents = results.get("organic_results", [])

    structured_patents = []

    for patent in patents[:limit]:
        patent_id = patent.get("patent_id")

        structured_patents.append({
            "title": patent.get("title"),
            "patent_id": patent_id,
            "link": (
                f"https://patents.google.com/{patent_id}"
                if patent_id
                else None
            ),
            "snippet": patent.get("snippet"),
        })

    return structured_patents


if __name__ == "__main__":

    query = "pothole detection computer vision"

    patents = search_patents(query)

    print(f"✅ Patent search successful!")
    print(f"Found {len(patents)} patent results\n")

    for patent in patents:
        print("Title:", patent["title"])
        print("Patent ID:", patent["patent_id"])
        print("Link:", patent["link"])
        print("Snippet:", patent["snippet"])
        print("-" * 60)