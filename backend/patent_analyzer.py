from idea_analyzer import analyze_idea


ACTION_FORMS = {
    "detect": [
        "detect",
        "detecting",
        "detection",
        "detected",
    ],
    "identify": [
        "identify",
        "identifying",
        "identification",
        "identified",
    ],
    "classify": [
        "classify",
        "classifying",
        "classification",
        "classified",
    ],
    "predict": [
        "predict",
        "predicting",
        "prediction",
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
        "translating",
        "translation",
        "translated",
    ],
    "analyze": [
        "analyze",
        "analyzing",
        "analysis",
        "analyzed",
    ],
    "recognize": [
        "recognize",
        "recognizing",
        "recognition",
        "recognized",
    ],
    "forecast": [
        "forecast",
        "forecasting",
        "forecasted",
    ],
    "recommend": [
        "recommend",
        "recommending",
        "recommendation",
        "recommended",
    ],
}


ACTION_DESCRIPTIONS = {
    "detect": "detecting",
    "identify": "identifying",
    "classify": "classifying",
    "predict": "predicting",
    "monitor": "monitoring",
    "track": "tracking",
    "translate": "translating",
    "analyze": "analyzing",
    "recognize": "recognizing",
    "forecast": "forecasting",
    "recommend": "recommending",
}


def find_action_match(action, searchable_text):
    """
    Check whether any form of an action appears
    in the patent title or snippet.
    """

    forms = ACTION_FORMS.get(
        action,
        [action]
    )

    for form in forms:

        if form.lower() in searchable_text:

            return True

    return False


def build_what_it_does(
    title,
    snippet,
    core_concept,
    matched_actions,
    matched_technologies,
    matched_contexts
):
    """
    Build a natural-language description of what
    the patent appears to do using the available
    title and snippet.

    No LLM or external API is used.
    """

    if snippet.strip():

        sentence = snippet.strip()

        sentence = " ".join(
            sentence.split()
        )

        if len(sentence) > 250:

            sentence = (
                sentence[:247]
                .rsplit(" ", 1)[0]
                + "..."
            )

        return sentence

    if matched_actions and core_concept:

        action = matched_actions[0]

        action_description = (
            ACTION_DESCRIPTIONS.get(
                action,
                action
            )
        )

        return (
            f"The patent appears to describe "
            f"a system for {action_description} "
            f"{core_concept}."
        )

    if core_concept:

        return (
            f"The patent appears to address "
            f"{core_concept}."
        )

    return (
        "The patent addresses a technology "
        "related to the submitted idea."
    )


def determine_similarity(
    core_concept_matched,
    matched_actions,
    matched_technologies,
    matched_contexts
):
    """
    Determine an initial rule-based similarity level.

    This is only a heuristic based on the available
    title and snippet text. It is not a legal or
    patentability assessment.
    """

    if not core_concept_matched:

        return "Low"

    supporting_elements = (
        len(matched_technologies)
        + len(matched_contexts)
    )

    if matched_actions:

        if supporting_elements >= 2:

            return "High"

        return "Medium"

    if supporting_elements >= 2:

        return "Medium"

    return "Low"


def build_similarity_reason(
    core_concept,
    core_concept_matched,
    matched_actions,
    matched_technologies,
    matched_contexts,
    similarity
):
    """
    Explain why the similarity level was assigned.

    This is a rule-based explanation based only on
    the retrieved patent title and snippet.
    """

    if similarity == "Low":

        if not core_concept_matched:

            return (
                "The retrieved text does not explicitly "
                f"match the core concept '{core_concept}'."
            )

        if not matched_actions:

            return (
                "The patent matches the core concept, "
                "but the analyzed action was not explicitly "
                "observed in the retrieved text."
            )

        return (
            "Only limited supporting elements were "
            "matched in the retrieved text."
        )

    if similarity == "Medium":

        if matched_actions and matched_technologies:

            return (
                "The patent matches the core concept, "
                "the main action, and at least one "
                "supporting technology."
            )

        if matched_actions and matched_contexts:

            return (
                "The patent matches the core concept, "
                "the main action, and at least one "
                "supporting context."
            )

        if matched_actions:

            return (
                "The patent matches the core concept "
                "and the main action, but fewer supporting "
                "elements were explicitly observed."
            )

        return (
            "The patent matches the core concept and "
            "multiple supporting elements, but the "
            "main action was not explicitly observed."
        )

    return (
        "The patent matches the core concept and main "
        "action, along with multiple supporting elements "
        "in the retrieved text."
    )


def build_matched_elements(
    matched_actions,
    matched_technologies,
    matched_contexts
):
    """
    Build a structured representation of elements
    observed in the retrieved patent text.
    """

    return {
        "actions": matched_actions,
        "technologies": matched_technologies,
        "contexts": matched_contexts,
    }


def analyze_patent(patent, idea):
    """
    Analyze one patent against the user's technology idea.

    This is a local deterministic analyzer.
    No external API calls are made.
    """

    idea_analysis = analyze_idea(
        idea
    )

    core_concept = idea_analysis.get(
        "core_concept"
    )

    actions = idea_analysis.get(
        "actions",
        []
    )

    technologies = idea_analysis.get(
        "technologies",
        []
    )

    contexts = idea_analysis.get(
        "contexts",
        []
    )

    title = patent.get(
        "title",
        ""
    )

    snippet = patent.get(
        "snippet",
        ""
    )

    searchable_text = (
        f"{title} {snippet}"
    ).lower()

    # --------------------------------------------------
    # Match technologies
    # --------------------------------------------------

    matched_technologies = []

    for technology in technologies:

        if technology.lower() in searchable_text:

            matched_technologies.append(
                technology
            )

    # --------------------------------------------------
    # Match contexts
    # --------------------------------------------------

    matched_contexts = []

    for context in contexts:

        if context.lower() in searchable_text:

            matched_contexts.append(
                context
            )

    # --------------------------------------------------
    # Match actions
    # --------------------------------------------------

    matched_actions = []

    for action in actions:

        if find_action_match(
            action,
            searchable_text
        ):

            matched_actions.append(
                action
            )

    # --------------------------------------------------
    # Core concept matching
    # --------------------------------------------------

    core_concept_matched = False

    if core_concept:

        if core_concept.lower() in searchable_text:

            core_concept_matched = True

        else:

            core_words = (
                core_concept.lower().split()
            )

            if len(core_words) == 1:

                word = core_words[0]

                if word.endswith("s"):

                    singular = word[:-1]

                    if singular in searchable_text:

                        core_concept_matched = True

                else:

                    plural = word + "s"

                    if plural in searchable_text:

                        core_concept_matched = True

    # --------------------------------------------------
    # Similarity
    # --------------------------------------------------

    similarity = determine_similarity(
        core_concept_matched,
        matched_actions,
        matched_technologies,
        matched_contexts
    )

    similarity_reason = build_similarity_reason(
        core_concept,
        core_concept_matched,
        matched_actions,
        matched_technologies,
        matched_contexts,
        similarity
    )

    # --------------------------------------------------
    # What the patent does
    # --------------------------------------------------

    what_it_does = build_what_it_does(
        title,
        snippet,
        core_concept,
        matched_actions,
        matched_technologies,
        matched_contexts
    )

    # --------------------------------------------------
    # Matched elements
    # --------------------------------------------------

    matched_elements = build_matched_elements(
        matched_actions,
        matched_technologies,
        matched_contexts
    )

    # --------------------------------------------------
    # Overlap analysis
    # --------------------------------------------------

    overlap_parts = []

    if core_concept_matched and core_concept:

        overlap_parts.append(
            f"Both the idea and patent relate to "
            f"{core_concept}."
        )

    if matched_actions:

        overlap_parts.append(
            "Shared actions: "
            + ", ".join(
                matched_actions
            )
            + "."
        )

    if matched_technologies:

        overlap_parts.append(
            "Shared technologies: "
            + ", ".join(
                matched_technologies
            )
            + "."
        )

    if matched_contexts:

        overlap_parts.append(
            "Shared context: "
            + ", ".join(
                matched_contexts
            )
            + "."
        )

    if overlap_parts:

        overlap = " ".join(
            overlap_parts
        )

    else:

        overlap = (
            "Limited overlap was identified "
            "using the available patent text."
        )

    # --------------------------------------------------
    # Potential differentiation
    # --------------------------------------------------

    differentiation_parts = []

    unmatched_technologies = [
        technology
        for technology in technologies
        if technology
        not in matched_technologies
    ]

    unmatched_contexts = [
        context
        for context in contexts
        if context
        not in matched_contexts
    ]

    if unmatched_technologies:

        differentiation_parts.append(
            "Technology elements not explicitly "
            "matched in the retrieved text: "
            + ", ".join(
                unmatched_technologies
            )
            + "."
        )

    if unmatched_contexts:

        differentiation_parts.append(
            "Context elements not explicitly "
            "matched in the retrieved text: "
            + ", ".join(
                unmatched_contexts
            )
            + "."
        )

    if differentiation_parts:

        differentiation = " ".join(
            differentiation_parts
        )

    else:

        differentiation = (
            "The retrieved text contains matches "
            "across the main analyzed elements. "
            "Further detailed comparison would be "
            "needed to identify meaningful differences."
        )

    return {
        "patent_id": patent.get(
            "patent_id"
        ),
        "title": title,
        "link": patent.get(
            "link"
        ),
        "what_it_does": what_it_does,
        "key_technologies": matched_technologies,
        "matched_elements": matched_elements,
        "matched_actions": matched_actions,
        "matched_contexts": matched_contexts,
        "overlap": overlap,
        "similarity": similarity,
        "similarity_reason": similarity_reason,
        "potential_differentiation": differentiation,
    }


if __name__ == "__main__":

    test_idea = (
        "AI system for detecting potholes "
        "using smartphone camera and GPS"
    )

    test_patent = {
        "patent_id": (
            "patent/JP7301138B2/en"
        ),
        "title": "Pothole detection system",
        "snippet": (
            "A system for detecting potholes "
            "using road surface analysis."
        ),
        "link": (
            "https://patents.google.com/"
            "patent/JP7301138B2/en"
        ),
    }

    result = analyze_patent(
        test_patent,
        test_idea
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "PATENT ANALYSIS TEST"
    )

    print(
        "=" * 60
    )

    print(
        f"\nPatent: {result['title']}"
    )

    print(
        f"\nWhat it does:\n"
        f"{result['what_it_does']}"
    )

    print(
        f"\nKey technologies:\n"
        f"{', '.join(result['key_technologies']) or 'None'}"
    )

    print(
        f"\nMatched elements:\n"
        f"{result['matched_elements']}"
    )

    print(
        f"\nMatched actions:\n"
        f"{', '.join(result['matched_actions']) or 'None'}"
    )

    print(
        f"\nMatched contexts:\n"
        f"{', '.join(result['matched_contexts']) or 'None'}"
    )

    print(
        f"\nOverlap:\n"
        f"{result['overlap']}"
    )

    print(
        f"\nSimilarity:\n"
        f"{result['similarity']}"
    )

    print(
        f"\nSimilarity reason:\n"
        f"{result['similarity_reason']}"
    )

    print(
        f"\nPotential differentiation:\n"
        f"{result['potential_differentiation']}"
    )