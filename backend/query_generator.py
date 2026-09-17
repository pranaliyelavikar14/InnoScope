def generate_patent_queries(idea):
    """
    Generate multiple focused patent search queries
    from a user's technology idea.
    """

    queries = [
        f'"{idea}"',
        f'{idea} computer vision',
        f'{idea} machine learning',
        f'{idea} smartphone',
        f'{idea} detection system',
    ]

    return queries


if __name__ == "__main__":

    idea = "pothole detection using smartphone camera and GPS"

    queries = generate_patent_queries(idea)

    print("Generated patent queries:\n")

    for i, query in enumerate(queries, start=1):
        print(f"{i}. {query}")