from idea_analyzer import analyze_idea


def generate_patent_queries(idea):
    """
    Generate concise and focused patent search queries
    from the analyzed technology idea.
    """

    analysis = analyze_idea(idea)

    technologies = analysis["technologies"]
    components = analysis["components"]
    domains = analysis["domains"]

    queries = []

    # Core concept
    queries.append("pothole detection")

    # Technology-focused
    if "computer vision" in technologies:
        queries.append("pothole detection computer vision")

    if "machine learning" in technologies:
        queries.append("pothole detection machine learning")

    # Device / component-focused
    if "smartphone" in technologies:
        queries.append("pothole detection smartphone")

    if "gps" in technologies:
        queries.append("pothole detection GPS")

    # Remove duplicates
    unique_queries = []

    for query in queries:
        if query not in unique_queries:
            unique_queries.append(query)

    return unique_queries


if __name__ == "__main__":

    idea = "AI system for detecting potholes using smartphone camera and GPS"

    queries = generate_patent_queries(idea)

    print("\nGenerated Patent Search Queries:")
    print("=" * 60)

    for i, query in enumerate(queries, start=1):
        print(f"{i}. {query}")