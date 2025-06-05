from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import random

app = FastAPI(title="Synergy API (Private Beta)")

API_KEYS = {"demo-key-123"}   # replace with Supabase lookup later


def verify_key(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")


class GenRequest(BaseModel):
    prompt: str
    max_tokens: int = 64


class GenResponse(BaseModel):
    completion: str
    bsq_score: float


@app.post("/generate", response_model=GenResponse, dependencies=[Depends(verify_key)])
async def generate(req: GenRequest):
    # TODO: call your model here; placeholder below
    completion = f"(Echo) {req.prompt}"
    bsq_score = round(random.uniform(0.4, 0.9), 3)  # placeholder
    return {"completion": completion, "bsq_score": bsq_score}


@app.get("/healthz")
async def health():
    return {"status": "ok"}
