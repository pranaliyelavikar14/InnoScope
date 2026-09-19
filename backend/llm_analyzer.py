from dotenv import load_dotenv
import json
import os
from google import genai


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANDSCAPE_PATH = os.path.join(BASE_DIR, "data", "landscape_result.json")


def load_landscape_result():
    """Load the locally generated InnoScope landscape result."""
    with open(LANDSCAPE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def prepare_llm_input(landscape_result):
    """
    Prepare a clean, grounded input for Gemini.

    The source JSON contains:
    - 'landscape' for the overall landscape summary
    - 'patent_analyses' for individual patent-level analysis
    """

    landscape = landscape_result.get("landscape", {})
    patent_analyses = landscape_result.get("patent_analyses", [])

    cleaned_patents = []

    for patent in patent_analyses:
        cleaned_patent = {
            "patent_id": patent.get("patent_id"),
            "title": patent.get("title"),
            "link": patent.get("link"),
            "what_it_does": patent.get("what_it_does"),
            "key_technologies": patent.get("key_technologies", []),
            "matched_elements": patent.get("matched_elements", []),
            "matched_actions": patent.get("matched_actions", []),
            "matched_contexts": patent.get("matched_contexts", []),
            "overlap": patent.get("overlap"),
            "similarity": patent.get("similarity"),
            "similarity_reason": patent.get("similarity_reason"),
            "potential_differentiation": patent.get(
                "potential_differentiation"
            ),
        }

        cleaned_patents.append(cleaned_patent)

    llm_input = {
        "idea": landscape_result.get("idea"),
        "total_patents": landscape.get("total_patents", 0),
        "similarity_distribution": landscape.get(
            "similarity_distribution", {}
        ),
        "common_technologies": landscape.get(
            "common_technologies", []
        ),
        "common_actions": landscape.get(
            "common_actions", []
        ),
        "common_contexts": landscape.get(
            "common_contexts", []
        ),
        "overlap_summary": landscape.get(
            "overlap_summary", ""
        ),
        "potential_differentiation": landscape.get(
            "potential_differentiation", []
        ),
        "patent_analyses": cleaned_patents,
    }

    return llm_input


def build_landscape_prompt(llm_input):
    """Build a grounded prompt for the InnoScope landscape report."""

    landscape_summary = {
        "total_patents": llm_input.get("total_patents"),
        "similarity_distribution": llm_input.get(
            "similarity_distribution"
        ),
        "common_technologies": llm_input.get(
            "common_technologies"
        ),
        "common_actions": llm_input.get(
            "common_actions"
        ),
        "common_contexts": llm_input.get(
            "common_contexts"
        ),
        "overlap_summary": llm_input.get(
            "overlap_summary"
        ),
        "potential_differentiation": llm_input.get(
            "potential_differentiation"
        ),
    }

    patent_analyses = llm_input.get("patent_analyses", [])

    return f"""
You are the analysis engine for InnoScope.

InnoScope is an AI-powered technology and prior-art
landscape explorer. It helps users understand publicly
discoverable technology overlap around an idea.

Your task is to summarize and explain ONLY the retrieved
information supplied below.

USER IDEA:
{llm_input.get("idea")}

OVERALL LANDSCAPE SUMMARY:
{json.dumps(landscape_summary, indent=2)}

PATENT-LEVEL ANALYSIS:
{json.dumps(patent_analyses, indent=2)}

IMPORTANT DATA INTERPRETATION RULES:

1. The OVERALL LANDSCAPE SUMMARY is a precomputed summary
   from the local InnoScope analysis pipeline.

2. The PATENT-LEVEL ANALYSIS contains the evidence for
   individual retrieved patents.

3. "common_technologies" means technologies identified as
   recurring in the analyzed landscape. It does NOT mean
   that every patent contains every listed technology.

4. "common_actions" means actions recurring in the analyzed
   landscape. Do not invent counts for individual actions
   unless those counts are explicitly supported by the
   supplied data.

5. "similarity_distribution" contains the exact precomputed
   counts for High, Medium, and Low heuristic similarity.
   Use these counts directly rather than recalculating them.

6. A patent's "similarity" is a heuristic classification
   based on the local InnoScope analysis. It is NOT a legal
   similarity determination.

7. "potential_differentiation" describes elements that were
   not explicitly matched by the local retrieval/analysis.
   This does NOT prove that those elements are novel or
   absent from all existing technology.

8. Do not infer that an element is present in a patent merely
   because it appears elsewhere in the overall summary.
   Use the individual patent record when making a
   patent-specific statement.

9. Do not create new patent IDs, technologies, companies,
   statistics, or factual claims.

Generate a concise but useful technology landscape report
with exactly these sections:

1. Executive Summary

Explain what the retrieved technology landscape shows
about the user's idea.

Include the exact similarity distribution from the supplied
overall landscape data.

2. Major Technology Patterns

Describe recurring technologies, actions, and contexts
that are explicitly present in the supplied landscape data.

Do not imply that recurring technologies occur in every
retrieved patent.

3. Areas of Overlap

Explain the main areas where the user's idea overlaps with
the retrieved patent information.

Use patent-level evidence when giving examples.

When mentioning individual patents, use their supplied
patent ID and title.

4. Potential Differentiation

Describe technology elements or combinations that were
not explicitly matched in the retrieved information.

Use cautious wording such as:
"was not explicitly matched in the retrieved snippets"
or
"was not identified in the analyzed records."

Do not describe these elements as legally novel,
patentable, or guaranteed to be unique.

5. Key Takeaways

Give 3-5 concise factual points that summarize:
- the observed technology landscape
- the main overlap patterns
- the supplied heuristic similarity distribution
- potential differentiation areas
- important limitations of the retrieval

IMPORTANT RULES:

- Use ONLY the information provided above.
- Do not invent facts.
- Do not invent statistics.
- Do not recalculate or reinterpret the supplied
  similarity distribution.
- Do not claim that an idea is patentable or not patentable.
- Do not claim that no one has built something similar.
- Do not provide legal advice.
- Do not speculate about patents that are not in the supplied
  records.
- Do not treat potential differentiation as proof of novelty.
- Clearly distinguish observed overlap from potential
  differentiation.
- Treat similarity levels as heuristic signals based on
  retrieved titles, snippets, and local analysis.
- If the retrieved information is insufficient for a
  conclusion, explicitly say so.
- Keep the report factual and technology-focused.
"""


def generate_gemini_report(prompt):
    """
    Send the prepared landscape prompt to Gemini.

    This function makes the external Gemini API call.
    """

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found in the environment."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text


if __name__ == "__main__":
    print("=" * 70)
    print("INNOSCOPE - GEMINI LANDSCAPE REPORT")
    print("=" * 70)

    print("\n[1] Loading landscape result...")
    landscape_result = load_landscape_result()
    print("✅ Landscape result loaded.")

    print("\n[2] Preparing grounded LLM input...")
    llm_input = prepare_llm_input(landscape_result)
    print("✅ LLM input prepared.")

    print(f"Idea: {llm_input.get('idea')}")
    print(
        f"Patents: {len(llm_input.get('patent_analyses', []))}"
    )

    print("\n[3] Building grounded Gemini prompt...")
    prompt = build_landscape_prompt(llm_input)
    print("✅ Gemini prompt generated.")

    print("\n[4] Calling Gemini...")
    print("⚠️ THIS USES ONE GEMINI API CALL.")
    print("⚠️ No additional Gemini calls will be made in this run.")

    report = generate_gemini_report(prompt)

REPORT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "gemini_report.txt"
)

with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write(report)

print("\n" + "=" * 70)
print("GENERATED INNOSCOPE REPORT")
print("=" * 70)

print(report)

print("\n" + "=" * 70)
print("REPORT SAVED")
print("=" * 70)
print(f"✅ Report saved to: {REPORT_PATH}")