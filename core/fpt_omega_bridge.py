# ====================== TRINITY VIZ ENDPOINT ======================
from core.trinity_harmonics import describe_trinity_state, plot_trinity_harmonics
import base64
from io import BytesIO

@app.get("/trinity-viz")
async def trinity_viz(preset: str = "Balanced", custom_damp: float = None):
    """Live Trinity Dynamics visualization as base64 PNG + JSON data"""
    describe_trinity_state()  # console log for server

    # Generate plot in memory
    fig, ax = plt.subplots(figsize=(11, 7))
    # ... (reuse your existing plot_trinity_harmonics logic here or call it)
    # For simplicity we reuse the function and capture output
    buf = BytesIO()
    plt.savefig(buf, format="png", facecolor="#0a0a0a")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")

    # Return JSON + image for React
    return {
        "status": "IGNITED",
        "preset": preset,
        "custom_damp": custom_damp,
        "trinity_data": {
            "ground_state": GROUND_STATE,
            "difference": DIFFERENCE,
            "ratio": RATIO,
            "phase": trinity.phase,
            "stability": trinity.trinity_factor(1.0)
        },
        "image": f"data:image/png;base64,{img_base64}"
    }
@app.get("/api/sovereign-ledger")
async def sovereign_ledger():
    """Real data feed from Turbo_Takeoff + Sovereign Resonance Economy"""
    # Example: pull from your resonance economy or Supabase
    sre = SovereignResonanceEconomy()  # your class
    
    # Mock / real data from Turbo_Takeoff (replace with actual DB call)
    project_data = {
        "language_training_hours": 60,
        "gwichin_business_value": 45000,
        "land_stewardship_funds": 15000,
        "community_contribution_points": 25,
        "shielding_efficiency": 92
    }
    
    result = sre.braid_positive_bbee(project_data)
    ancsa_result = sre.integrate_with_ancsa({"land_stewardship_days": 30, "corporate_revenue_reinvested": 120000})
    
    return {
        "resonance": result["resonance_score"],
        "gtc_balance": round(result["resonance_score"] * 1234, 0),  # example compounding
        "compound_years": 4.2,
        "hidden_balance": round(result["resonance_score"] * 15678, 0),
        "forfeited_short_game": round(result["resonance_score"] * 11456, 0),
        "status": result["recommendation"]
    }