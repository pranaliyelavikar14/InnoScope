import re


def clean_text(text):
    """Normalize text for analysis."""

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


def detect_actions(idea):
    """Detect common technology actions from the idea."""

    idea_lower = clean_text(idea)

    action_patterns = {
        "detect": r"\bdetect(?:s|ed|ing)?\b",
        "identify": r"\bidentif(?:y|ies|ied|ying)\b",
        "classify": r"\bclassif(?:y|ies|ied|ying)\b",
        "predict": r"\bpredict(?:s|ed|ing)?\b",
        "monitor": r"\bmonitor(?:s|ed|ing)?\b",
        "track": r"\btrack(?:s|ed|ing)?\b",
        "translate": r"\btranslat(?:e|es|ed|ing)\b",
        "analyze": r"\banaly[sz](?:e|es|ed|ing)\b",
        "recognize": r"\brecogni[sz](?:e|es|ed|ing)\b",
        "forecast": r"\bforecast(?:s|ed|ing)?\b",
        "recommend": r"\brecommend(?:s|ed|ing)?\b",
    }

    actions = []

    for action, pattern in action_patterns.items():
        if re.search(pattern, idea_lower):
            actions.append(action)

    return actions


def extract_object(idea):
    """Extract the main object/problem associated with the action."""

    idea_lower = clean_text(idea)

    patterns = [
        r"\b(?:detect|detecting|detects|detected)\s+(.+?)(?:\s+using\s+|\s+with\s+|\s+from\s+|\s+through\s+|\s+via\s+|\s+based\s+on\s+|$)",

        r"\b(?:identify|identifying|identifies|identified)\s+(.+?)(?:\s+using\s+|\s+with\s+|\s+from\s+|\s+through\s+|\s+via\s+|\s+based\s+on\s+|$)",

        r"\b(?:predict|predicting|predicts|predicted)\s+(.+?)(?:\s+in\s+|\s+using\s+|\s+with\s+|\s+from\s+|\s+through\s+|\s+via\s+|\s+based\s+on\s+|$)",

        r"\b(?:classify|classifying|classifies|classified)\s+(.+?)(?:\s+using\s+|\s+with\s+|\s+from\s+|\s+through\s+|\s+via\s+|\s+based\s+on\s+|$)",

        r"\b(?:translate|translating|translates|translated)\s+(.+?)(?:\s+using\s+|\s+with\s+|\s+from\s+|\s+through\s+|\s+via\s+|\s+based\s+on\s+|$)",

        r"\b(?:monitor|monitoring|monitors|monitored)\s+(.+?)(?:\s+using\s+|\s+with\s+|\s+from\s+|\s+through\s+|\s+via\s+|\s+based\s+on\s+|$)",
    ]

    for pattern in patterns:

        match = re.search(pattern, idea_lower)

        if match:
            result = match.group(1).strip()

            if result:
                return result

    return None


def extract_context(idea, object_text):
    """
    Extract contextual information from the idea.
    """

    idea_lower = clean_text(idea)

    if not object_text:
        return []

    contexts = []

    context_patterns = [
        r"\b(?:in|within)\s+(.+)$",
        r"\b(?:using|with|through|via)\s+(.+)$",
    ]

    for pattern in context_patterns:

        matches = re.findall(pattern, idea_lower)

        for match in matches:

            context = match.strip()

            if context:
                contexts.append(context)

    return list(dict.fromkeys(contexts))


def detect_technology_terms(idea):
    """
    Detect explicitly mentioned technology terms.
    """

    idea_lower = clean_text(idea)

    technology_terms = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "computer vision",
        "natural language processing",
        "generative ai",
        "large language model",
        "llm",
        "neural network",
        "cnn",
        "yolo",
        "gps",
        "camera",
        "smartphone",
        "mobile",
        "android",
        "ios",
        "sensor",
        "drone",
        "robot",
        "iot",
        "blockchain",
        "cloud",
        "edge computing",
    ]

    detected = []

    for technology in technology_terms:

        if technology in idea_lower:
            detected.append(technology)

    return detected


def analyze_idea(idea):
    """
    Analyze a technology idea and return structured information.
    """

    if not idea or not idea.strip():
        raise ValueError("Idea cannot be empty.")

    idea = idea.strip()

    actions = detect_actions(idea)

    object_text = extract_object(idea)

    contexts = extract_context(
        idea,
        object_text
    )

    technologies = detect_technology_terms(idea)

    return {
        "original_idea": idea,
        "core_concept": object_text,
        "actions": actions,
        "contexts": contexts,
        "technologies": technologies,
    }


if __name__ == "__main__":

    test_ideas = [
        "AI system for detecting potholes using smartphone camera and GPS",
        "AI system for detecting crop diseases from leaf images",
        "Smartphone application for translating Indian Sign Language",
        "AI system that predicts battery degradation in electric vehicles",
    ]

    for idea in test_ideas:

        result = analyze_idea(idea)

        print("\n" + "=" * 70)
        print("IDEA ANALYSIS")
        print("=" * 70)

        print("\nOriginal Idea:")
        print(result["original_idea"])

        print("\nCore Concept:")
        print(result["core_concept"])

        print("\nActions:")
        for action in result["actions"]:
            print("-", action)

        print("\nContexts:")
        for context in result["contexts"]:
            print("-", context)

        print("\nTechnologies:")
        for technology in result["technologies"]:
            print("-", technology)