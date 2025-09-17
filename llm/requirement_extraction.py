from llm.llm_client import client, model
from typing import List
from datamodels import RequirementsModel

def extract_requirements(text: str) -> List[str]:
    """
    Uses OpenAI's ChatGPT to extract blocks of text that represent requirements from the provided input text.

    Args:
        text (str): The full input text from which to extract requirement blocks.

    Returns:
        List[str]: A list of requirement blocks as strings. If the model cannot parse or no requirements are found,
                   an empty list is returned.
    
    Notes:
        - Requires a valid OpenAI API key set via the OPENAI_API_KEY environment variable.
        - Includes a sleep delay to avoid hitting API rate limits during batch processing.
    """    
#     prompt = f"""Extract all blocks of text from the following content that express a requirement. A "block" can be a sentence, a group of sentences, or a paragraph, as long as it expresses a complete requirement.
# Words that signify a requirement include terms such as "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL".
# Do not translate, rewrite, or interpret the text — just extract it as-is.

# Text: "{text}"

# Return the output as a valid JSON array of strings. If there are no requirements, return an **empty JSON array** (`[]`).
# """

    prompt = f"""Extract all blocks of text from the following content that express a rule. 
A "block" can be a sentence, a group of sentences, or a paragraph, as long as it expresses a complete rule.

Words that signify a rule include terms such as "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", 
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL".

Do not translate, rewrite, or interpret the text — just extract it as-is.

Then, for each extracted rule, classify it into exactly one of these categories:
1. "requirement" – Mandatory rules or obligations (e.g., "MUST", "REQUIRED", "SHALL").
2. "recommendation" – Advice, suggestions, or non-mandatory good practices (e.g., "SHOULD", "RECOMMENDED").
3. "permission" – Things allowed but not required (e.g., "MAY", "OPTIONAL", "PERMITTED").
4. "possibility" – Statements about what could happen, ability, or potential (e.g., "CAN", "MIGHT").

Text:
\"\"\"
{text}
\"\"\"

Return the result as a valid JSON array of objects, where each object contains:
- "text": the exact block of text as-is
- "classification": one of ["requirement", "recommendation", "permission", "possibility"]

If there are no rules, return an **empty JSON array** (`[]`).
"""
    try:
        response = client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You are an assistant who extracts requirements from technical specifications."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            text_format=RequirementsModel
        )

        # Direct parsed output
        requirements = response.output_parsed.requirements
        print("Extracted requirements:", requirements)

        return requirements

    except Exception as e:
        print("Error:", e)
        return []