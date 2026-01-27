from fastapi import FastAPI, Depends, HTTPException
from fpt_core.processor import FeedbackProcessor
from fpt_core.models.unified import UnifiedPoint
from .handshake import initiate_takeoff

app = FastAPI(title="Turbo_Takeoff Relay")

# Initializing the engine with Epsilon Pi calibration
processor = FeedbackProcessor(codex_mode="default")

@app.post("/relay/circle")
async def circle_relay(event_data: dict):
    """
    Broad-spectrum resonance endpoint.
    Processes general feedback into the community field.
    """
    # Verify field strength before accepting transmission
    if not initiate_takeoff(node_count=5):
        raise HTTPException(status_code=403, detail="Resonance Insufficient")
        
    result = processor.process_single_event(event_data)
    return {"status": "resonant", "field_strength": result.strength}

@app.post("/relay/whisper")
async def whisper_relay(physics: dict, biology: dict):
    """
    Fine-grained diagnostic endpoint.
    Used for 'Shadow Work' calibration and Unified Point debugging.
    """
    unity = UnifiedPoint(physics_def=physics, biology_def=biology)
    
    # Calculate the somatic receipt (the frisson point)
    walkable_path = unity.debug_unity()
    
    return {
        "status": "unified",
        "epsilon_pi_trace": walkable_path,
        "is_walkable": walkable_path >= 3.173
    }

@app.middleware("http")
async def sovereign_verification(request, call_next):
    # Requirement: All requests must carry the Sovereign Anchor ID
    sovereign_id = request.headers.get("X-Sovereign-ID")
    if sovereign_id != "EIN-39-6968515":
        raise HTTPException(status_code=401, detail="Sovereignty Unverified")
    
    response = await call_next(request)
    return response
