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
    product_name: str
    brand: str
    ram: str
    storage: str

schema=AnalysisResponse.model_json_schema()

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
    return {
        "output_text": AnalysisResponse.model_validate_json(interaction.output_text)
    }
