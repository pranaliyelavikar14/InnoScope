import re


# --------------------------------------------------
# Common words that do not carry useful meaning
# --------------------------------------------------

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "based",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "through",
    "to",
    "using",
    "via",
    "with",
}


# --------------------------------------------------
# Generic system/product words
# --------------------------------------------------

GENERIC_TERMS = {
    "ai",
    "artificial intelligence",
    "system",
    "application",
    "app",
    "platform",
    "solution",
    "method",
    "device",
    "tool",
    "model",
    "software",
}


# --------------------------------------------------
# Explicit technology terms
# --------------------------------------------------

TECHNOLOGY_TERMS = [
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


# --------------------------------------------------
# Action patterns
# --------------------------------------------------

ACTION_PATTERNS = {
    "detect": r"\bdetect(?:s|ed|ing)?\b",
    "identify": r"\bidentif(?:y|ies|ied|ying)\b",
    "classify": r"\bclassif(?:y|ies|ied|ying)\b",
    "predict": r"\bpredict(?:s|ed|ing)?\b",
    "monitor": r"\bmonitor(?:s|ed|ing)?\b",
    "track": r"\btrack(?:s|ed|ing)?\b",
    "translate": r"\btranslat(?:e|es|ed|ing)\b",
    "analyze": r"\banaly[sz](?:e|es|ed|ing)\b",
    "recognize": r"\brecogni[sz](?:e|es|ied|ying)\b",
    "forecast": r"\bforecast(?:s|ed|ing)?\b",
    "recommend": r"\brecommend(?:s|ed|ing)?\b",
}


# --------------------------------------------------
# All grammatical forms of actions
# --------------------------------------------------

ACTION_VARIANTS = {
    "detect": [
        "detect",
        "detects",
        "detected",
        "detecting",
    ],
    "identify": [
        "identify",
        "identifies",
        "identified",
        "identifying",
    ],
    "classify": [
        "classify",
        "classifies",
        "classified",
        "classifying",
    ],
    "predict": [
        "predict",
        "predicts",
        "predicted",
        "predicting",
    ],
    "monitor": [
        "monitor",
        "monitors",
        "monitored",
        "monitoring",
    ],
    "track": [
        "track",
        "tracks",
        "tracked",
        "tracking",
    ],
    "translate": [
        "translate",
        "translates",
        "translated",
        "translating",
    ],
    "analyze": [
        "analyze",
        "analyzes",
        "analyzed",
        "analyzing",
    ],
    "recognize": [
        "recognize",
        "recognizes",
        "recognized",
        "recognizing",
    ],
    "forecast": [
        "forecast",
        "forecasts",
        "forecasted",
        "forecasting",
    ],
    "recommend": [
        "recommend",
        "recommends",
        "recommended",
        "recommending",
    ],
}


def clean_text(text):
    """
    Normalize input text.
    """

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


def detect_actions(idea):
    """
    Detect the main technological actions
    present in the idea.
    """

    idea_lower = clean_text(idea)

    actions = []

    for action, pattern in ACTION_PATTERNS.items():

        if re.search(pattern, idea_lower):
            actions.append(action)

    return actions


def extract_object(idea):
    """
    Extract the main object/problem associated
    with a technological action.
    """

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

        match = re.search(
            pattern,
            idea_lower
        )

        if match:

            result = match.group(1).strip()

            if result:
                return result

    return None


def detect_technology_terms(idea):
    """
    Detect explicitly mentioned technologies.

    Longer technology phrases are checked first
    to avoid partial/overlapping matches.
    """

    idea_lower = clean_text(idea)

    matches = []

    sorted_terms = sorted(
        TECHNOLOGY_TERMS,
        key=len,
        reverse=True
    )

    for technology in sorted_terms:

        if technology in GENERIC_TERMS:
            continue

        match = re.search(
            rf"\b{re.escape(technology)}\b",
            idea_lower
        )

        if match:

            matches.append(
                (
                    match.start(),
                    technology
                )
            )

    # Sort technologies by their position
    # in the original idea.
    matches.sort(
        key=lambda item: item[0]
    )

    detected = []

    for _, technology in matches:

        if technology not in detected:
            detected.append(technology)

    return detected


def remove_action_variants(
    text,
    actions
):
    """
    Remove all grammatical forms of
    detected actions from a phrase.
    """

    cleaned = text

    for action in actions:

        variants = ACTION_VARIANTS.get(
            action,
            [action]
        )

        for variant in variants:

            cleaned = re.sub(
                rf"\b{re.escape(variant)}\b",
                " ",
                cleaned
            )

    return cleaned


def clean_context(
    context,
    core_concept,
    actions,
    technologies
):
    """
    Clean a raw context phrase by removing
    actions, core concepts, technologies,
    and generic words.
    """

    context = clean_text(
        context
    )

    # Remove all action variants.
    context = remove_action_variants(
        context,
        actions
    )

    # Remove core concept.
    if core_concept:

        context = re.sub(
            rf"\b{re.escape(core_concept)}\b",
            " ",
            context
        )

    # Remove technology terms.
    for technology in technologies:

        context = re.sub(
            rf"\b{re.escape(technology)}\b",
            " ",
            context
        )

    # Remove generic multi-word terms.
    for generic_term in GENERIC_TERMS:

        context = re.sub(
            rf"\b{re.escape(generic_term)}\b",
            " ",
            context
        )

    # Normalize spaces.
    context = re.sub(
        r"\s+",
        " ",
        context
    ).strip()

    # Remove individual stopwords.
    words = context.split()

    useful_words = []

    for word in words:

        word = word.strip(
            ".,!?;:"
        )

        if not word:
            continue

        if word in STOPWORDS:
            continue

        useful_words.append(
            word
        )

    return " ".join(
        useful_words
    ).strip()


def extract_context(
    idea,
    core_concept,
    actions,
    technologies
):
    """
    Extract meaningful contextual information.

    Supported context patterns include:

    - in <context>
    - within <context>
    - from <context>

    Important:
    'for detecting ...' is NOT treated as context,
    because it represents the action/object part
    of the idea.
    """

    idea_lower = clean_text(
        idea
    )

    contexts = []

    # --------------------------------------------------
    # "in" context
    #
    # Example:
    # predicts battery degradation in electric vehicles
    # -> electric vehicles
    # --------------------------------------------------

    in_pattern = (
        r"\bin\s+(.+?)"
        r"(?=\s+using\s+|\s+with\s+|\s+from\s+"
        r"|\s+through\s+|\s+via\s+|$)"
    )

    for match in re.findall(
        in_pattern,
        idea_lower
    ):

        contexts.append(
            match
        )

    # --------------------------------------------------
    # "within" context
    #
    # Example:
    # operates within industrial environments
    # -> industrial environments
    # --------------------------------------------------

    within_pattern = (
        r"\bwithin\s+(.+?)"
        r"(?=\s+using\s+|\s+with\s+|\s+from\s+"
        r"|\s+through\s+|\s+via\s+|$)"
    )

    for match in re.findall(
        within_pattern,
        idea_lower
    ):

        contexts.append(
            match
        )

    # --------------------------------------------------
    # "from" input/source context
    #
    # Example:
    # detects crop diseases from leaf images
    # -> leaf images
    # --------------------------------------------------

    from_pattern = (
        r"\bfrom\s+(.+?)"
        r"(?=\s+using\s+|\s+with\s+|\s+through\s+"
        r"|\s+via\s+|$)"
    )

    for match in re.findall(
        from_pattern,
        idea_lower
    ):

        contexts.append(
            match
        )

    # --------------------------------------------------
    # Clean and deduplicate
    # --------------------------------------------------

    cleaned_contexts = []

    for context in contexts:

        cleaned = clean_context(
            context,
            core_concept,
            actions,
            technologies
        )

        if not cleaned:
            continue

        if cleaned == core_concept:
            continue

        if cleaned not in cleaned_contexts:

            cleaned_contexts.append(
                cleaned
            )

    return cleaned_contexts


def analyze_idea(idea):
    """
    Main idea-analysis pipeline.

    Returns:
        original_idea
        core_concept
        actions
        contexts
        technologies
    """

    if not idea or not idea.strip():

        raise ValueError(
            "Idea cannot be empty."
        )

    idea = idea.strip()

    actions = detect_actions(
        idea
    )

    core_concept = extract_object(
        idea
    )

    technologies = detect_technology_terms(
        idea
    )

    contexts = extract_context(
        idea,
        core_concept,
        actions,
        technologies
    )

    return {
        "original_idea": idea,
        "core_concept": core_concept,
        "actions": actions,
        "contexts": contexts,
        "technologies": technologies,
    }


# --------------------------------------------------
# Local testing
# --------------------------------------------------

if __name__ == "__main__":

    test_ideas = [
        "AI system for detecting potholes using smartphone camera and GPS",

        "AI system for detecting crop diseases from leaf images",

        "Smartphone application for translating Indian Sign Language",

        "AI system that predicts battery degradation in electric vehicles",
    ]

    for idea in test_ideas:

        result = analyze_idea(
            idea
        )

        print(
            "\n" + "=" * 70
        )

        print(
            "IDEA ANALYSIS"
        )

        print(
            "=" * 70
        )

        print(
            "\nOriginal Idea:"
        )

        print(
            result["original_idea"]
        )

        print(
            "\nCore Concept:"
        )

        print(
            result["core_concept"]
        )

        print(
            "\nActions:"
        )

        if result["actions"]:

            for action in result["actions"]:
                print(
                    "-",
                    action
                )

        else:
            print(
                "- None"
            )

        print(
            "\nTechnologies:"
        )

        if result["technologies"]:

            for technology in result["technologies"]:
                print(
                    "-",
                    technology
                )

        else:
            print(
                "- None"
            )

        print(
            "\nContext:"
        )

        if result["contexts"]:

            for context in result["contexts"]:
                print(
                    "-",
                    context
                )

        else:
            print(
                "- None"
            )