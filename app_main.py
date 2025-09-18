import re
import time

from datamodels import SectionType
from llm.section_classification import classify_section
from llm.terminology_extraction import extract_terms
from llm.requirement_extraction import extract_requirements
from lxml import etree

"""
Description:
    This script reads an XML file containing structured documentation (e.g. technical specifications),
    extracts text content from specific <section> elements, and uses the OpenAI Chat API to identify
    and extract blocks of text that represent requirements.

    Each requirement is extracted based on semantic cues and returned as a list of strings (JSON array).
    The script is designed to support processing and analysis of regulatory, standards-based,
    or technical specification documents.

Main Features:
    - Parses XML using lxml for full XPath support.
    - Locates <section> elements and extracts all contained text.
    - Sends the full section text to an LLM.
    - Prompts the LLM to classify each section as normative content, terminology or other.
    - Prompts the LLM to return all requirement-like blocks of text as a JSON array.
    - Calculates character offsets of each requirement relative to its section.    
    - (Calculates character offsets of each concept relative to its section)

Functions:
    - `extract_requirements(text)`: Sends text to OpenAI Chat API and parses the JSON result.
    - `find_requirements_in_section_llm(text)`: Wrapper that calls `extract_requirements`.

Setup:
    - Set your OpenAI API key via environment variable: `OPENAI_API_KEY=your-key`

Usage:
    python extract_requirements_from_xml.py path/to/file.
    
Todo: Make generic (not just sections). 
"""

def find_requirements_in_section_llm(section_node, tree):
    """
    Extracts requirement blocks from a given <section> element in an XML tree using a Large Language Model (LLM).

    Args:
        section_node (lxml.etree._Element): The <section> element to process.
        tree (lxml.etree._ElementTree): The entire parsed XML tree, used for XPath generation.

    Returns:
        List[dict]: A list of dictionaries with the following keys:
            - 'requirement': The extracted requirement block (string).
            - 'section_xpath': The XPath of the <section> in the XML.
            - 'xml_start': The start character offset of the requirement in the section text.
            - 'xml_end': The end character offset of the requirement in the section text.
    """    
    section_text = ''.join(section_node.itertext()).strip()
    section_xpath = tree.getpath(section_node)

    extracted_requirements = extract_requirements(section_text)
    time.sleep(5)

    results = []

    for req in extracted_requirements:
        # req is a RequirementItem object
        req_text = req.text
        classification = req.classification

        start = section_text.find(req_text)
        if start != -1:
            end = start + len(req_text)
            results.append({
                'requirement_text': req_text,
                'classification': classification.value,  # store as string
                'section_relative_start': start,
                'section_relative_end': end,
                'section_xpath': section_xpath
            })
        else:
            print(f"Requirement not found in section {section_xpath}: '{req_text}'")
            results.append({
                'requirement_text': req_text,
                'classification': classification.value,  # store as string
                'section_relative_start': None,
                'section_relative_end': None,
                'section_xpath': section_xpath                
            })

    return results

def extract_requirements_from_xml(xml_file_path):
    """
    Parses an XML document, identifies relevant sections, and extracts requirements using an LLM.

    Args:
        xml_file_path (str): The path to the XML file to be processed.

    Returns:
        None
    """    
    parser = etree.XMLParser(recover=True, encoding='utf-8')
    with open(xml_file_path, 'r', encoding='utf-8') as f:
        xml_data = f.read()
    root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
    tree = root.getroottree()

    sections = tree.xpath('//section')
    if not sections:
        print("No <section> elements found.")
        return

    all_requirements = []
    all_definitions = []

    for section in sections:
        # Get section title (if present)
        title_node = section.find('.//title')
        title = ""
        if title_node is not None:
            if title_node.text:
                title = title_node.text.strip()

        # Get section text
        section_text = " ".join(section.itertext()).strip()

        # Classify section type
        category = classify_section(section_text, title=title)
        print(f"Section XPath: '{tree.getpath(section)}'")
        print(f"Section classified as: {category}")
        time.sleep(3)

        if category == SectionType.normative:
            # Find requirements
            requirements = find_requirements_in_section_llm(section, tree)
            all_requirements.extend(requirements)
        elif category ==  SectionType.terminology:
            # Find concepts
            definitions = extract_terms(section_text)
            all_definitions.extend(definitions)
            # for item in definitions_list:
            #     concept_list = item[0]  # take the first element of the tuple
            #     all_definitions.extend(concept_list.concepts)
        else:
            print(f"Skipping section '{title}' ({category})")

    for req in all_requirements:
        print(f"Requirement text: {req['requirement_text']}\n")
        print(f"Requirement class: {req['classification']}\n")
        print(f"Document section (XPath): {req['section_xpath']}")
        print(f"Start: {req['section_relative_start']}, End: {req['section_relative_end']}")
        print("-" * 50)
    print(all_definitions)

def normalize_text(text):
    """Normalize whitespace for consistent matching."""
    return re.sub(r'\s+', ' ', text.strip())
