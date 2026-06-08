from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from engine import VeriTrustEngine

# 1. Instantiate the API Gateway and the security engine we just built
app = FastAPI(
    title="VeriTrust AI Enterprise Gateway", 
    description="Zero-Trust Proxy for secure LLM prompts", 
    version="1.0.0"
)
security_engine = VeriTrustEngine()

# 2. Define what incoming data must look like (User ID + Prompt Text)
class PromptRequest(BaseModel):
    user_id: str
    prompt: str

# 3. Create the active security endpoint
@app.post("/api/v1/proxy/sanitize")
async def sanitize_endpoint(request: PromptRequest):
    try:
        # Basic validation check
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt context cannot be empty.")
        
        # Pass data through our AI analyzer rules
        metrics = security_engine.analyze_and_sanitize(request.prompt)
        
        return {
            "status": "SECURED",
            "user_id": request.user_id,
            "data": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))