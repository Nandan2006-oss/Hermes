from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv


# -------------------------
# Configuration
# -------------------------

load_dotenv()
client = genai.Client()

app = FastAPI()


# -------------------------
# Data Models
# -------------------------

class SourceEvidence(BaseModel):
    evidence: str
    source: str


class EvidenceField(BaseModel):
    value: str
    evidence: list[SourceEvidence]
    confidence: float


class Conflict(BaseModel):
    field: str
    values: list[str]
    sources: list[str]


class AnalysisRequest(BaseModel):
    sources: dict[str, str]


class AnalysisResponse(BaseModel):
    part_number: str
    brand: str
    product_type: str
    quantity_value: float
    quantity_uom: str
    width: EvidenceField
    length: EvidenceField
    conflicts: list[Conflict]


schema = AnalysisResponse.model_json_schema()


# -------------------------
# Normalization
# -------------------------

def normalize_dimension(value: str):
    return value.replace('"', ' in')


def normalize_quantity_uom(value: str):
    return value


# -------------------------
# Validation
# -------------------------

def validate_product(result: AnalysisResponse):

    if result.quantity_value <= 0:
        raise ValueError("Quantity must be greater than 0")

    return result


def validate_evidence(evidence: str, original_text: str):
    return evidence in original_text


# -------------------------
# Conflict Detection
# -------------------------

def detect_conflict(value1: str, value2: str):
    if value1 != value2:
        return True

    return False


# -------------------------
# Routes
# -------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(data: AnalysisRequest):

    prompt = f"""
Extract the relevant product information from the following product sources.

For every field that has an EvidenceField:

- value: the normalized extracted value
- evidence: a list of evidence items
- each evidence item must contain:
  - evidence: the exact text supporting the value
  - source: the name of the source where that evidence was found
- confidence: your confidence that the extracted value is correct, from 0 to 1

Do not invent information that is not present in the provided sources.

Product sources:
{data.sources}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": schema
        }
    )

    # LLM output → Pydantic object
    result = AnalysisResponse.model_validate_json(
        interaction.output_text
    )

    # -------------------------
    # Normalization
    # -------------------------

    result.width.value = normalize_dimension(
        result.width.value
    )

    result.length.value = normalize_dimension(
        result.length.value
    )

    result.quantity_uom = normalize_quantity_uom(
        result.quantity_uom
    )

    # -------------------------
    # Evidence Validation
    # -------------------------

    for item in result.width.evidence:
        if not validate_evidence(
            item.evidence,
            data.sources[item.source]
        ):
            result.width.confidence = 0.0

    for item in result.length.evidence:
        if not validate_evidence(
            item.evidence,
            data.sources[item.source]
        ):
            result.length.confidence = 0.0

    # -------------------------
    # Validation
    # -------------------------

    result = validate_product(result)

    return {"output_text": result}