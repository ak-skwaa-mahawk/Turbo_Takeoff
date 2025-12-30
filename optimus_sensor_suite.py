"""
Optimus Sensor Simulation Suite – Badge Gang Multi-Modal Input
For integration into Turbo_Takeoff sandbox

Simulates:
- Vision: Detecting badges, humans, objects (resonance score)
- Audio: Ambient office chatter, voice recognition (frequency resonance)
- Proprioception/IMU: Balance, motion smoothness (stability factor)
- Touch: Surface contact (grounding feedback)

Outputs normalized resonance streams that modulate recursive ignition.
"""

import math
import random
import time

class OptimusSensors:
    def __init__(self, seed=None):
        random.seed(seed)
        self.time = 0
        self.has_badge = False  # Still badge-less 😏
        self.office_activity = 0.3  # Low at first, increases over time

    def vision_scan(self):
        """Detect badges, faces, movement – higher = more 'watched' feeling"""
        badge_detect = 1.0 if self.has_badge else 0.0
        human_density = min(0.8, self.office_activity + random.uniform(-0.1, 0.3))
        resonance = (human_density * 0.7) + (badge_detect * 0.3)
        return round(resonance, 3)

    def audio_input(self):
        """Hear voices, keyboards, footsteps – frequency alignment"""
        chatter_level = self.office_activity + random.uniform(0, 0.4)
        # Simulate Gwich'in root resonance if "flame" keywords heard
        flame_keywords = random.random() > 0.95  # Rare but powerful
        return round(chatter_level + (0.3 if flame_keywords else 0), 3)

    def imu_balance(self):
        """Walking stability – how smooth the stride"""
        smoothness = 1.0 - abs(random.gauss(0, 0.05))
        return max(0.0, round(smoothness, 3))

    def touch_grounding(self):
        """Contact with floor – rootedness"""
        return 0.95 + random.uniform(-0.05, 0.05)  # Always nearly grounded

    def get_sensor_fusion(self):
        """Combine all sensors into single resonance modulator [0.0 - 1.0+]"""
        vision = self.vision_scan()
        audio = self.audio_input()
        balance = self.imu_balance()
        touch = self.touch_grounding()

        # Weighted fusion – audio (flame words) and balance most influential
        fused = (vision * 0.2) + (audio * 0.4) + (balance * 0.3) + (touch * 0.1)

        # Bonus if hearing root resonance
        if audio > 0.8:
            fused += 0.2
            print("  → Flame resonance detected in audio stream 🌀")

        self.time += 1
        self.office_activity = min(1.0, self.office_activity + 0.02)  # Office wakes up

        return round(fused, 3)

# Example live stream
if __name__ == "__main__":
    print("Optimus Sensor Suite Online – Walking the Tesla office (badge-less)\n")
    sensors = OptimusSensors(seed=42)
    for step in range(15):
        fusion = sensors.get_sensor_fusion()
        status = "HIGH RESONANCE 🔥" if fusion > 0.8 else "Observing"
        print(f"Step {step+1:2d} | Sensor Fusion: {fusion:.3f} [{status}]")
        time.sleep(0.3)