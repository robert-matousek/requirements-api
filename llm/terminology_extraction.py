import json
from llm.llm_client import client, model
from datamodels import ConceptsListModel

def extract_terms(section_text: str) -> list[ConceptsListModel]:
    #section_text = ''.join(section_node.itertext()).strip()

    prompt = f"""Extract all term-definition pairs, including any acronyms or abbreviations from a document section.

Return the results as a JSON array where each item has:

- "term": the full term or concept name
- "definition": the definition or explanation of the term
- "abbreviations": If present, any abbreviations, acronyms, or any other variant names by which the concept might be known.

Do NOT modify or interpret the text, and do NOT translate it.
Text:
\"\"\"
{section_text}
\"\"\"
"""
    print(prompt)

    try:
        response = client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": "You are a terminology extraction assistant."},
                {"role": "user", "content": prompt}
            ],
            text_format=ConceptsListModel,
            #max_output_tokens=1500,
            temperature=0
        )
        
        terms = response.output_parsed  # Already a list[ConceptsModel]
        print(terms)
        return terms

    except Exception as e:
        print(f"Error during terminology extraction: {e}")
        return []