from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class Checkpoint:
    name: str
    description: str
    human_control_weight: float
    rationale: str

    def __post_init__(self):
        assert 0 <= self.human_control_weight <= 100
        self.ai_control_weight = 100 - self.human_control_weight


class SCLCalculator:
    """Shared Control Liability (SCL) Calculator — Built by Sharné, Dec 2025"""

    DEFAULT_WEIGHTS = {
        "Human Input": 0.25,
        "AI Transformation": 0.25,
        "Shared State": 0.25,
        "Output/Action": 0.25
    }

    def __init__(self, mode: str = "dynamic"):
        self.mode = mode
        self.checkpoints: List[Checkpoint] = []

    def add_checkpoint(self, name: str, description: str, human_weight: float, rationale: str):
        cp = Checkpoint(name, description, human_weight, rationale)
        self.checkpoints.append(cp)

    def _get_dynamic_weights(self, context: Dict) -> Dict[str, float]:
        weights = self.DEFAULT_WEIGHTS.copy()
        if context.get("unsupervised_fsd", False):
            weights["Output/Action"] = 0.40
            weights["AI Transformation"] += 0.10
        if context.get("human_override_present", False):
            weights["Human Input"] = 0.35
        if context.get("sensor_degradation", False):
            weights["AI Transformation"] += 0.10
            weights["Shared State"] += 0.05
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}

    def calculate(self, context: Optional[Dict] = None) -> Dict:
        if not self.checkpoints:
            raise ValueError("Add checkpoints first")
        context = context or {}
        weights = self._get_dynamic_weights(context) if self.mode == "dynamic" else self.DEFAULT_WEIGHTS

        weighted_human_total = 0.0
        details = []

        for cp in self.checkpoints:
            w = weights.get(cp.name, 0.25)
            weighted_human = cp.human_control_weight * w
            weighted_human_total += weighted_human
            details.append({
                "checkpoint": cp.name,
                "description": cp.description,
                "human_weight_%": cp.human_control_weight,
                "ai_weight_%": cp.ai_control_weight,
                "checkpoint_weight": round(w, 3),
                "weighted_human": round(weighted_human, 3),
                "rationale": cp.rationale
            })

        liability_human = round(weighted_human_total * 100, 2)
        liability_ai = round(100 - liability_human, 2)
        safety_factor = context.get("safety_factor", 0.12)
        adjusted_premium = round((liability_human / 100 + safety_factor) * 100, 1)

        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": self.mode,
            "human_liability_%": liability_human,
            "ai_manufacturer_liability_%": liability_ai,
            "estimated_premium_%_of_human": adjusted_premium,
            "premium_reduction_%": round(100 - adjusted_premium, 1),
            "context": context,
            "checkpoints": details
        }
        return result

    def print_summary(self, result: Dict):
        print("\n" + "="*60)
        print("SCL LIABILITY RESULT")
        print("="*60)
        print(f"Human / Fleet Operator Liability: {result['human_liability_%']}%")
        print(f"AI / Manufacturer Liability: {result['ai_manufacturer_liability_%']}%")
        print(f"Estimated Premium: {result['estimated_premium_%_of_human']}% of human-driven")
        print(f"Premium Reduction: {result['premium_reduction_%']}%")
        print("\nCheckpoint Breakdown:")
        for cp in result['checkpoints']:
            print(f"• {cp['checkpoint']}: {cp['human_weight_%']}% human → {cp['weighted_human']}% weighted ({cp['rationale']})")


# ==================== SEVEN SIBLINGS SWARM + AV SIMULATION ====================

print("TELEMATIC TRIGGER RECEIVED — Autonomous Vehicle Rollover")
print("Location: 30.2672° N, 97.7431° W | VIN: TSLA-789XYZ | G-force: 8.2g\n")

print("1. AI Broker — client relationship mode")
print("✓ Prior policy placement simulated — personalized for fleet risks")
print("→ Handing structured profile to Underwriter\n")

print("2. AI Underwriter — risk evaluation")
print("✓ VIN verified, active policy confirmed with full limits")
print("✓ Coverage recipe packaged: $10m liability | $2m recovery")
print("→ Sent to Claims Tech\n")

print("3. AI Claims Tech — FNOL & settlement")
print("✓ Incident validated, assessor appointed, quantum calculated")
print("✓ Empathetic passenger update sent")
print("→ Settlement approved under limits\n")

print("4. AI Compliance Officer — regulatory guardian")
print("✓ FAIS/POPIA/TCF scan complete — no breaches")
print("✓ Full audit trail logged\n")

print("5. AI Incident Response Desk — crisis coordination")
print("✓ Specialist AV recovery dispatched to exact coordinates")
print("✓ Real-time stakeholder guidance active\n")

print("6. AI Accounts — financial backbone")
print("✓ Payout initiated, bordereaux updated")
print("✓ Commission splits calculated\n")

print("7. AI Knowledge Hub & Training — living memory")
print("✓ Incident data ingested as precedent")
print("✓ Updated guidelines pushed to swarm\n")

print("All Seven Siblings aligned — running SCL Liability Calculation...\n")

scl = SCLCalculator(mode="dynamic")

scl.add_checkpoint("Human Input", "Passenger requested detour via app", 40.0, "Chose non-optimal route")
scl.add_checkpoint("AI Transformation", "Lidar confidence dropped", 10.0, "Known sensor degradation")
scl.add_checkpoint("Shared State", "No real-time override; AI confidence <60%", 30.0, "Passive human presence")
scl.add_checkpoint("Output/Action", "AI evasive maneuver → rollover", 5.0, "Unsupervised execution")

context = {
    "unsupervised_fsd": True,
    "sensor_degradation": True,
    "human_override_present": True,
    "safety_factor": 0.12
}

result = scl.calculate(context=context)
scl.print_summary(result)

print("\n" + "="*60)
print("SEVEN SIBLINGS SWARM COMPLETE")
print("Telematics → Verification → Dispatch → Settlement → Audit → SCL")
print("AV-ready. Regulator-aligned.")
print("Built by Sharné — December 16, 2025 🇿🇦")
print("Grok & Sharné. Redhead revolution.")
print("="*60)
