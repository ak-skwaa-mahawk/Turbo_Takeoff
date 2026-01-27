from fpt_core.logic.glyph_math import GlyphEngine, SENDER, RECEIVER

def initiate_takeoff(node_count: int):
    """
    Validates the resonance field strength before deployment.
    """
    engine = GlyphEngine()
    field = engine.calculate_resonance(SENDER, node_count, RECEIVER)
    
    print(f"Handshake Initiated: {field['semantic_layer']}")
    
    if field['field_strength'] >= 35:
        print(f"Resonance Verified ({field['field_strength']}). Launching Vehicle...")
        return True
    else:
        print(f"Resonance Insufficient ({field['field_strength']}). Takeoff Aborted.")
        return False
