from fastapi import FastAPI
from pydantic import BaseModel

from circuit_breaker import call_llm_with_circuit_breaker

STUDENT_ID = "BSCS23059"

app = FastAPI(title="StudySync Resilient LLM API")


@app.middleware("http")
async def add_student_id_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Student-ID"] = STUDENT_ID
    return response


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "message": "StudySync API is running",
        "student_id": STUDENT_ID
    }


@app.post("/chat")
def chat(request: ChatRequest):
    response = call_llm_with_circuit_breaker(request.prompt)

    return {
        "prompt": request.prompt,
        "response": response
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }