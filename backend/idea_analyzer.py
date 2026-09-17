def analyze_idea(idea):
    """
    Analyze a technology idea and extract
    useful concepts for technology landscape search.
    """

    idea_lower = idea.lower()

    technologies = []
    components = []
    domains = []

    # Technology detection
    technology_keywords = {
        "computer vision": ["computer vision", "image", "camera", "vision"],
        "machine learning": ["machine learning", "ml"],
        "deep learning": ["deep learning", "neural network", "cnn", "yolo"],
        "gps": ["gps", "geolocation", "location"],
        "smartphone": ["smartphone", "mobile", "android"],
        "artificial intelligence": ["ai", "artificial intelligence"],
    }

    for technology, keywords in technology_keywords.items():

        if any(keyword in idea_lower for keyword in keywords):
            technologies.append(technology)

    # Component detection
    component_keywords = {
        "camera": ["camera", "cameras"],
        "gps": ["gps", "location"],
        "mobile application": ["app", "application", "smartphone", "mobile"],
        "detection system": ["detection", "detect"],
        "mapping": ["mapping", "map"],
    }

    for component, keywords in component_keywords.items():

        if any(keyword in idea_lower for keyword in keywords):
            components.append(component)

    # Domain detection
    domain_keywords = {
        "transportation": ["road", "vehicle", "traffic", "transport"],
        "infrastructure": ["pothole", "road damage", "road condition"],
        "healthcare": ["health", "medical", "disease", "patient"],
        "agriculture": ["crop", "farm", "agriculture", "plant"],
        "education": ["student", "education", "learning"],
    }

    for domain, keywords in domain_keywords.items():

        if any(keyword in idea_lower for keyword in keywords):
            domains.append(domain)

    return {
        "original_idea": idea,
        "technologies": technologies,
        "components": components,
        "domains": domains,
    }


if __name__ == "__main__":

    idea = "AI system for detecting potholes using smartphone camera and GPS"

    result = analyze_idea(idea)

    print("\n" + "=" * 60)
    print("IDEA ANALYSIS")
    print("=" * 60)

    print("\nOriginal Idea:")
    print(result["original_idea"])

    print("\nTechnologies:")
    for technology in result["technologies"]:
        print("-", technology)

    print("\nComponents:")
    for component in result["components"]:
        print("-", component)

    print("\nDomains:")
    for domain in result["domains"]:
        print("-", domain)