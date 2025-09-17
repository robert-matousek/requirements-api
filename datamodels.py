from enum import Enum
from pydantic import BaseModel
from typing import List

### REQUIREMENTS

class RequirementType(str, Enum):
    requirement = "requirement"
    recommendation = "recommendation"
    permission = "permission"
    possibility = "possibility"

class RequirementItem(BaseModel):
    text: str
    classification: RequirementType

class RequirementsModel(BaseModel):
    requirements: list[RequirementItem]

### CONCEPTS

class ConceptsModel(BaseModel):
    term: str
    definition: str
    abbreviations: list[str]

class ConceptsListModel(BaseModel):
    concepts: List[ConceptsModel]    

### SECTIONS

class SectionType(str, Enum):
    terminology = "terminology"
    normative = "normative_content"
    other = "other"

class SectionModel(BaseModel):
    section_type: SectionType
