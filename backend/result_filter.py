import json
import os
import re

from idea_analyzer import analyze_idea


# --------------------------------------------------
# Common words that should not influence relevance
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
# Action synonyms
# --------------------------------------------------

ACTION_SYNONYMS = {
    "detect": [
        "detect",
        "detection",
        "detecting",
        "detected",
    ],
    "identify": [
        "identify",
        "identification",
        "identifying",
        "identified",
    ],
    "classify": [
        "classify",
        "classification",
        "classifying",
        "classified",
    ],
    "predict": [
        "predict",
        "prediction",
        "predicting",
        "predicted",
    ],
    "monitor": [
        "monitor",
        "monitoring",
        "monitored",
    ],
    "track": [
        "track",
        "tracking",
        "tracked",
    ],
    "translate": [
        "translate",
        "translation",
        "translating",
        "translated",
    ],
    "analyze": [
        "analyze",
        "analysis",
        "analyzing",
        "analyzed",
    ],
    "recognize": [
        "recognize",
        "recognition",
        "recognizing",
        "recognized",
    ],
    "forecast": [
        "forecast",
        "forecasting",
        "forecasted",
    ],
    "recommend": [
        "recommend",
        "recommendation",
        "recommending",
        "recommended",
    ],
}


def normalize_text(text):
    """
    Normalize text for reliable matching.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def generate_term_variants(term):
    """
    Generate simple lexical variants of a concept.

    Examples:

        potholes
        -> potholes
        -> pothole
        -> pot hole

        crop diseases
        -> crop diseases
        -> crop disease

    This is intentionally conservative.
    """

    term = normalize_text(
        term
    )

    if not term:
        return []

    variants = [
        term
    ]

    words = term.split()

    # --------------------------------------------------
    # Singularize a simple final plural.
    # --------------------------------------------------

    if len(words) >= 1:

        last_word = words[-1]

        if last_word.endswith("ies") and len(last_word) > 3:

            singular_word = (
                last_word[:-3] + "y"
            )

            singular_words = words[:-1] + [
                singular_word
            ]

            variants.append(
                " ".join(singular_words)
            )

        elif last_word.endswith("s") and not last_word.endswith("ss"):

            singular_word = last_word[:-1]

            singular_words = words[:-1] + [
                singular_word
            ]

            variants.append(
                " ".join(singular_words)
            )

    # --------------------------------------------------
    # Handle compound words such as:
    #
    # pothole -> pot hole
    # --------------------------------------------------

    if "pothole" in term:

        variants.append(
            term.replace(
                "pothole",
                "pot hole"
            )
        )

    if "potholes" in term:

        variants.append(
            term.replace(
                "potholes",
                "pot hole"
            )
        )

        variants.append(
            term.replace(
                "potholes",
                "pothole"
            )
        )

    return list(
        dict.fromkeys(
            variants
        )
    )


def contains_term(text, term):
    """
    Check whether a complete word or phrase
    exists in the text.
    """

    text = normalize_text(
        text
    )

    term = normalize_text(
        term
    )

    if not text or not term:
        return False

    pattern = (
        rf"(?<!\w)"
        rf"{re.escape(term)}"
        rf"(?!\w)"
    )

    return re.search(
        pattern,
        text
    ) is not None


def find_term_match(text, term):
    """
    Check all safe lexical variants of a term.
    """

    variants = generate_term_variants(
        term
    )

    for variant in variants:

        if contains_term(
            text,
            variant
        ):
            return variant

    return None


def build_search_terms(analysis):
    """
    Build structured relevance terms from
    the analyzed idea.
    """

    return {
        "core": analysis.get(
            "core_concept"
        ),

        "actions": analysis.get(
            "actions",
            []
        ),

        "technologies": analysis.get(
            "technologies",
            []
        ),

        "contexts": analysis.get(
            "contexts",
            []
        ),
    }


def get_action_terms(actions):
    """
    Expand canonical actions into common
    search-language variants.
    """

    action_terms = []

    for action in actions:

        variants = ACTION_SYNONYMS.get(
            action,
            [action]
        )

        for variant in variants:

            if variant not in action_terms:

                action_terms.append(
                    variant
                )

    return action_terms


def calculate_relevance_score(
    title,
    snippet,
    search_terms
):
    """
    Calculate relevance score for one patent.

    Core concept is mandatory.

    Generic technologies such as camera,
    GPS, smartphone, etc. cannot make a patent
    relevant by themselves.
    """

    title_text = normalize_text(
        title
    )

    snippet_text = normalize_text(
        snippet
    )

    core = search_terms.get(
        "core"
    )

    actions = search_terms.get(
        "actions",
        []
    )

    technologies = search_terms.get(
        "technologies",
        []
    )

    contexts = search_terms.get(
        "contexts",
        []
    )

    score = 0

    matched_keywords = []

    # --------------------------------------------------
    # 1. CORE CONCEPT
    # --------------------------------------------------

    core_title_match = None
    core_snippet_match = None

    if core:

        core_title_match = find_term_match(
            title_text,
            core
        )

        core_snippet_match = find_term_match(
            snippet_text,
            core
        )

    # --------------------------------------------------
    # Core concept is mandatory.
    #
    # If it does not occur anywhere, the patent
    # is not considered relevant by this baseline.
    # --------------------------------------------------

    if not core_title_match and not core_snippet_match:

        return 0, []

    # --------------------------------------------------
    # Strong core score
    # --------------------------------------------------

    if core_title_match:

        score += 15

        matched_keywords.append(
            core_title_match
        )

    elif core_snippet_match:

        score += 8

        matched_keywords.append(
            core_snippet_match
        )

    # --------------------------------------------------
    # 2. ACTION
    # --------------------------------------------------

    action_match = False

    action_terms = get_action_terms(
        actions
    )

    for action_term in action_terms:

        if contains_term(
            title_text,
            action_term
        ):

            score += 5

            action_match = True

            matched_keywords.append(
                action_term
            )

        elif contains_term(
            snippet_text,
            action_term
        ):

            score += 2

            action_match = True

            matched_keywords.append(
                action_term
            )

    # --------------------------------------------------
    # 3. CORE + ACTION COMBINATION
    # --------------------------------------------------

    if action_match:

        if core_title_match:

            score += 10

        elif core_snippet_match:

            score += 5

    # --------------------------------------------------
    # 4. TECHNOLOGIES
    # --------------------------------------------------

    technology_matches = 0

    for technology in technologies:

        if contains_term(
            title_text,
            technology
        ):

            score += 3

            technology_matches += 1

            matched_keywords.append(
                technology
            )

        elif contains_term(
            snippet_text,
            technology
        ):

            score += 1

            technology_matches += 1

            matched_keywords.append(
                technology
            )

    # --------------------------------------------------
    # 5. CONTEXT
    # --------------------------------------------------

    context_matches = 0

    for context in contexts:

        context_match_title = find_term_match(
            title_text,
            context
        )

        context_match_snippet = find_term_match(
            snippet_text,
            context
        )

        if context_match_title:

            score += 4

            context_matches += 1

            matched_keywords.append(
                context_match_title
            )

        elif context_match_snippet:

            score += 2

            context_matches += 1

            matched_keywords.append(
                context_match_snippet
            )

    # --------------------------------------------------
    # 6. Core + technology bonus
    # --------------------------------------------------

    if technology_matches:

        score += 3

    # --------------------------------------------------
    # 7. Core + context bonus
    # --------------------------------------------------

    if context_matches:

        score += 3

    # --------------------------------------------------
    # Remove duplicate matched keywords
    # --------------------------------------------------

    matched_keywords = list(
        dict.fromkeys(
            matched_keywords
        )
    )

    return score, matched_keywords


def filter_relevant_patents(
    patents,
    idea,
    minimum_score=8
):
    """
    Rank patents according to relevance
    to the current technology idea.

    A patent must contain the core concept
    to enter the relevant-results list.
    """

    analysis = analyze_idea(
        idea
    )

    search_terms = build_search_terms(
        analysis
    )

    relevant_patents = []

    for patent in patents:

        title = patent.get(
            "title"
        ) or ""

        snippet = patent.get(
            "snippet"
        ) or ""

        score, matched_keywords = (
            calculate_relevance_score(
                title,
                snippet,
                search_terms
            )
        )

        if score >= minimum_score:

            patent_copy = patent.copy()

            patent_copy[
                "relevance_score"
            ] = score

            patent_copy[
                "matched_keywords"
            ] = matched_keywords

            relevant_patents.append(
                patent_copy
            )

    # --------------------------------------------------
    # Sort by score first.
    # Title provides deterministic ordering
    # when scores are equal.
    # --------------------------------------------------

    relevant_patents.sort(
        key=lambda patent: (
            patent[
                "relevance_score"
            ],
            patent.get(
                "title",
                ""
            ).lower()
        ),
        reverse=True
    )

    return relevant_patents


# --------------------------------------------------
# Local testing
# --------------------------------------------------

if __name__ == "__main__":

    data_dir = os.path.join(
        os.path.dirname(
            os.path.dirname(
                __file__
            )
        ),
        "data"
    )

    patent_file = os.path.join(
        data_dir,
        "patent_results.json"
    )

    if not os.path.exists(
        patent_file
    ):

        print(
            "❌ patent_results.json not found."
        )

        raise SystemExit(1)

    # --------------------------------------------------
    # Load existing local patent data.
    #
    # NO SerpApi call.
    # --------------------------------------------------

    with open(
        patent_file,
        "r",
        encoding="utf-8"
    ) as file:

        patents = json.load(
            file
        )

    # --------------------------------------------------
    # Test idea
    # --------------------------------------------------

    test_idea = (
        "AI system for detecting potholes "
        "using smartphone camera and GPS"
    )

    analysis = analyze_idea(
        test_idea
    )

    search_terms = build_search_terms(
        analysis
    )

    relevant_patents = (
        filter_relevant_patents(
            patents,
            test_idea
        )
    )

    # --------------------------------------------------
    # Display analysis
    # --------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "LOCAL PATENT FILTER TEST"
    )

    print(
        "=" * 70
    )

    print(
        "\nTest Idea:"
    )

    print(
        test_idea
    )

    print(
        "\nCore Concept:"
    )

    print(
        search_terms["core"]
    )

    print(
        "\nActions:"
    )

    if search_terms["actions"]:

        for action in search_terms["actions"]:

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

    if search_terms["technologies"]:

        for technology in search_terms["technologies"]:

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

    if search_terms["contexts"]:

        for context in search_terms["contexts"]:

            print(
                "-",
                context
            )

    else:

        print(
            "- None"
        )

    # --------------------------------------------------
    # Display ranked results
    # --------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "RANKED PATENT RESULTS"
    )

    print(
        "=" * 70
    )

    print(
        f"\nRelevant Patents Found: "
        f"{len(relevant_patents)}"
    )

    print(
        "\nTop 10 Results:\n"
    )

    for i, patent in enumerate(
        relevant_patents[:10],
        start=1
    ):

        print(
            f"{i}. "
            f"{patent.get('title', 'No title')}"
        )

        print(
            f"   Score: "
            f"{patent.get('relevance_score', 0)}"
        )

        matched = patent.get(
            "matched_keywords",
            []
        )

        print(
            "   Matched: "
            + (
                ", ".join(matched)
                if matched
                else "None"
            )
        )

        print(
            f"   Patent ID: "
            f"{patent.get('patent_id', 'N/A')}"
        )

        print(
            "-" * 70
        )