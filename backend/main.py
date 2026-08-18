from unittest import result

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

app = FastAPI()

# 1. Define the Pydantic model for the request body
class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    part_number: str
    brand: str
    product_type: str
    quantity_value: float
    quantity_uom: str
    width: str
    length: str

schema=AnalysisResponse.model_json_schema()

def normalize_dimension(value: str):
    return value.replace('"', ' in')

@app.get("/health")
def health():
    return {"status": "ok"}

# 2. Add the model as a parameter to your endpoint
@app.post("/analyze")
def analyze(data: AnalysisRequest):
    # You can access the text using data.text
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=data.text,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": schema
        }
    )
    result = AnalysisResponse.model_validate_json(interaction.output_text)

    result.width = normalize_dimension(result.width)
    result.length = normalize_dimension(result.length)

    return {"output_text": result}
