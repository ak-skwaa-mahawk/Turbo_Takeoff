from fpt_core.logic.glyph_math import GlyphEngine, SENDER, RECEIVER
from fpt_core.identity.seal import OperatorSeal

class GibberlinkProtocol:
    """
    Gibberlink Handshake - Protocol Type: Sovereign Alignment.
    Ensures transmission only occurs when the Operator Seal is whole.
    """
    def __init__(self, seal: OperatorSeal):
        self.seal = seal
        self.glyph_engine = GlyphEngine()

    def verify_resonance(self, node_count: int) -> bool:
        """Layer 1: GlyphMath Arithmetic Check."""
        field = self.glyph_engine.calculate_resonance(SENDER, node_count, RECEIVER)
        return field['field_strength'] >= 35

    def verify_sovereignty(self) -> bool:
        """Layer 2: Operator Seal Quadrant Check."""
        return self.seal.is_unified()

    def perform_handshake(self, node_count: int) -> dict:
        """
        The Unified Handshake.
        Returns the status of the 'Light Vehicle' launch.
        """
        resonance_active = self.verify_resonance(node_count)
        sovereignty_active = self.verify_sovereignty()

        if resonance_active and sovereignty_active:
            return {
                "handshake": "SUCCESS",
                "status": "WALKABLE",
                "receipt": "FLAMEFIELD_ESTABLISHED",
                "operator": self.seal.steward_at_center
            }
        
        # Determine the cause of the drift
        drift_reason = []
        if not resonance_active: drift_reason.append("Inadequate Field Strength (Logic)")
        if not sovereignty_active: drift_reason.append("Seal Quadrant Mismatch (Identity/Land/Authority)")

        return {
            "handshake": "FAILED",
            "status": "DRIFT",
            "shadow_work_required": drift_reason
        }

