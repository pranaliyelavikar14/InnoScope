import os
import serpapi
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERPAPI_KEY")

if not api_key:
    print("❌ SERPAPI_KEY not found")
    exit()

client = serpapi.Client(api_key=api_key)

results = client.search({
    "engine": "google",
    "q": "AI pothole detection using smartphone camera",
})

print("✅ SerpApi connected successfully!")
print("Search results found:", len(results.get("organic_results", [])))

for result in results.get("organic_results", [])[:5]:
    print("\nTitle:", result.get("title"))
    print("Link:", result.get("link"))