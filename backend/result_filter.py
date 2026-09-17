def filter_relevant_patents(patents):
    """
    Rank patents based on technology-specific relevance.
    """

    keyword_weights = {
        "pothole": 5,
        "road anomaly": 5,
        "road condition": 4,
        "road surface": 4,
        "road damage": 4,
        "infrastructure damage": 4,
        "gps": 3,
        "smartphone": 3,
        "computer vision": 3,
        "machine learning": 3,
        "deep learning": 3,
        "vehicle": 2,
        "camera": 2,
        "image": 1,
        "detection": 1,
    }

    relevant_patents = []

    for patent in patents:

        title = (patent.get("title") or "").lower()
        snippet = (patent.get("snippet") or "").lower()

        text = title + " " + snippet

        score = 0
        matched_keywords = []

        for keyword, weight in keyword_weights.items():

            if keyword in text:
                score += weight
                matched_keywords.append(keyword)

        if score > 0:
            patent["relevance_score"] = score
            patent["matched_keywords"] = matched_keywords

            relevant_patents.append(patent)

    relevant_patents.sort(
        key=lambda patent: patent["relevance_score"],
        reverse=True
    )

    return relevant_patents