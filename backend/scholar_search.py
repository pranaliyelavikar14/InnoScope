import os
import serpapi
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv("SERPAPI_KEY")

if not api_key:
    raise ValueError("SERPAPI_KEY not found in .env file")

client = serpapi.Client(api_key=api_key)


def search_scholar(query, limit=10):
    """
    Search Google Scholar using SerpApi.
    """

    results = client.search({
        "engine": "google_scholar",
        "q": query,
    })

    papers = results.get("organic_results", [])

    structured_papers = []

    for paper in papers[:limit]:

        structured_papers.append({
            "title": paper.get("title"),
            "publication_info": paper.get("publication_info"),
            "snippet": paper.get("snippet"),
            "link": paper.get("link"),
            "result_id": paper.get("result_id"),
        })

    return structured_papers


if __name__ == "__main__":

    query = "pothole detection smartphone camera GPS"

    papers = search_scholar(query)
with open("../data/scholar_results.json", "w", encoding="utf-8") as file:
    json.dump(papers, file, indent=4, ensure_ascii=False)
    print("💾 Scholar results saved to data/scholar_results.json")
    print("✅ Google Scholar search successful!")
    print(f"Found {len(papers)} papers\n")

    for i, paper in enumerate(papers, start=1):

        print(f"{i}. {paper['title']}")
        print(f"   Link: {paper['link']}")
        print(f"   Info: {paper['publication_info']}")
        print(f"   Snippet: {paper['snippet']}")
        print("-" * 60)