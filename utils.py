import csv
import pickle
from typing import List, Dict
from datamodels import ConceptsModel

def write_requirements_to_csv(all_requirements: List[Dict], csv_file_name: str = "requirements.csv"):
    """
    Write a list of requirement dictionaries to a CSV file.

    Args:
        all_requirements (List[Dict]): List of requirement dictionaries.
        csv_file_name (str, optional): Name of the CSV file. Defaults to "requirements.csv".
    """
    headers = [
        'requirement_text',
        'classification',
        'section_xpath',
        'section_relative_start',
        'section_relative_end'
    ]

    try:
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for req in all_requirements:
                writer.writerow(req)

        print(f"Successfully wrote {len(all_requirements)} records to {csv_file_name}")

    except IOError as e:
        print(f"Error writing to file {csv_file_name}: {e}")
    except KeyError as e:
        print(f"Error: A result dictionary is missing the key: {e}. Please check your data.")

def write_definitions_to_csv(all_definitions: List[ConceptsModel], csv_file_name: str = "definitions.csv"):
    """
    Write a list of ConceptsModel objects to a CSV file.

    Args:
        all_definitions (List[ConceptsModel]): List of concepts to write.
        csv_file_name (str, optional): Name of the CSV file. Defaults to "definitions.csv".
    """
    headers = ["term", "definition", "abbreviations"]

    try:
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for term in all_definitions:
                writer.writerow({
                    "term": term.term,
                    "definition": term.definition,
                    "abbreviations": ", ".join(term.abbreviations) if term.abbreviations else ""
                })

        print(f"Definitions written to {csv_file_name}")

    except Exception as e:
        print(f"Error writing definitions to CSV: {e}")

def save_definitions_as_pickle(all_definitions, pickle_file_name="definitions.pkl"):
    """
    Save a list of ConceptsModel objects to a pickle file.

    Args:
        all_definitions (list): List of ConceptsModel objects.
        pickle_file_name (str, optional): Name of the pickle file. Defaults to "definitions.pkl".
    """
    try:
        with open(pickle_file_name, 'wb') as f:
            pickle.dump(all_definitions, f)
        print(f"Definitions saved to {pickle_file_name}")
    except Exception as e:
        print(f"Error saving definitions to pickle: {e}")

# Example usage:
import os
if __name__ == "__main__":
    # xml_path = os.path.join("data", "publication_595.xml")
    # extract_requirements_from_xml(xml_path)


    # Load the pickle file
    pickle_file = "definitions.pkl"  # replace with your filename
    with open(pickle_file, "rb") as f:
        data = pickle.load(f)

    # Extract the ConceptsModel list
    concepts_list = data[1]  # the second item in your list

    # Write to CSV
    csv_file = "definitions.csv"
    headers = ["term", "definition", "abbreviations"]

    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for concept in concepts_list:
                writer.writerow({
                    "term": concept.term,
                    "definition": concept.definition,
                    "abbreviations": ", ".join(concept.abbreviations) if concept.abbreviations else ""
                })

        print(f"Definitions written to {csv_file}")

    except Exception as e:
        print(f"Error writing CSV: {e}")    
