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

@app.get("/health")
def health():
    return {"status": "ok"}

# 2. Add the model as a parameter to your endpoint
@app.post("/analyze")
def analyze(data: AnalysisRequest):
    # You can access the text using data.text
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=data.text
    )
    return {
        "message": "Analyze endpoint works",
        "processed_text": data.text,
        "output_text": interaction.output_text
    }
