from llm.llm_client import client, model
from datamodels import SectionModel, SectionType

def classify_section(text: str, title: str | None = None) -> SectionType:
    """
    Classifies a document section into exactly one of three categories:
    - terminology: Sections that define terms, acronyms, and abbreviations.
    - normative_content: Sections that set rules, requirements, or recommendations.
    - other: Everything else (e.g., front matter, back matter, references).
    
    Args:
        text (str): Section content.
        title (str, optional): Section title.
    
    Returns:
        SectionType: Enum value representing the classification.
    """
    combined_text = f"Title: {title or 'Unknown'}\n\n{text}"

    prompt = f"""
    Classify the following section into one of exactly three categories:
    - "terminology": Sections that provide clear and precise definitions of key terms, acronyms, and abbreviations used throughout the document.
    - "normative_content": Sections or elements that establish standards, guidelines, rules, or requirements that need to be followed.
    - "other": Any other type of section, including front matter (title page, authors, publisher, publication date, ISBN, copyright,
      preface, foreword, table of contents) and back matter (bibliography, index, appendices, acknowledgements, annexes, non-normative notes).

    Classification rules:
    - If the section defines terms, words, or concepts, classify as terminology.
    - If the section states rules, requirements, obligations, prohibitions, or recommendations, classify as normative_content.
    - Everything else is other.

    Respond with a valid JSON object: {{ "section_type": "<category>" }}.
    Section:
    \"\"\"{combined_text}\"\"\"
    """

    try:
        response = client.responses.parse(
            model= model,
            input=[
                {
                    "role": "system",
                    "content": "You classify document sections into terminology, normative_content, or other."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            text_format=SectionModel,
            temperature=0,   # Fully deterministic
            top_p=1,         # (Optional) makes selection fully greedy
            #seed=42          # (Optional) locks in randomness if model supports it            
        )
        # Drill down to the parsed Pydantic model
        category_model = response.output[0].content[0].parsed
        print(category_model)
        # Access the enum value
        category = category_model.section_type

    except Exception as e:
        print(f"Error during classification: {e}")
        category = SectionType.other  # default fallback

    return category
