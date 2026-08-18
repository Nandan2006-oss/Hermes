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

class EvidenceField(BaseModel):
    value: str
    evidence: str
    source: str
    confidence: float


class Conflict(BaseModel):
    field: str
    values: list[str]
    sources: list[str]


class AnalysisRequest(BaseModel):
    text: str


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
Extract the relevant product information from the following product description.

For every field that has an EvidenceField:

- value: the extracted value
- evidence: the exact text from the product description that supports the value
- source: where the evidence came from. Since the only source currently provided is the product description, use "Part_Desc"
- confidence: your confidence that the extracted value is correct, from 0 to 1

Do not invent information that is not present in the product description.

Product description:
{data.text}
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
    # Validation
    # -------------------------

    result = validate_product(result)

    return {"output_text": result}