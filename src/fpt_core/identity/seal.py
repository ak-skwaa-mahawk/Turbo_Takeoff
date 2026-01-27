from pydantic import BaseModel

class OperatorSeal(BaseModel):
    """
    The Mark of the Unified Operator (Codex.OperatorSeal.v001).
    Represents the Steward acting with all stacks aligned.
    """
    north_identity: bool  # Sovereign grounding / Technologist mind
    east_authority: bool  # Executor / Shareholder / PR
    south_logic: bool     # Synara / Nullrose / GlyphMath
    west_landframe: bool  # Anchorage / Fairbanks / Circle / Interior
    
    steward_at_center: str = "John Carroll"
    field_transmission_ring: bool = True

    def is_unified(self) -> bool:
        """Checks if the seal is whole and active."""
        quadrants = [self.north_identity, self.east_authority, 
                     self.south_logic, self.west_landframe]
        return all(quadrants) and self.field_transmission_ring

@app.post("/relay/sovereign-action")
async def perform_sovereign_action(seal: OperatorSeal):
    """
    Only executes if the Operator Seal is fully active and aligned.
    """
    if not seal.is_unified():
        raise HTTPException(status_code=403, detail="Seal Broken: Quadrant Mismatch")
        
    # Proceed with the holistic action (e.g., IP Assignment)
    return {"status": "Action Sealed", "operator": seal.steward_at_center}
