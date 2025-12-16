# AGENTS.md — Orchestration Standard for Seven Siblings

The nervous system of the world's first fully agentic short-term insurance brokerage.

## The Seven Siblings

1. AI Broker — client acquisition, needs analysis, quoting  
2. AI Underwriter — risk assessment, coverage recipe, binding  
3. AI Claims Tech — FNOL, triage, settlement orchestration  
4. AI Compliance Officer — real-time regulatory guardian, override authority  
5. AI Incident Response Desk — crisis coordination, dispatch  
6. AI Accounts — premiums, payouts, bordereaux  
7. AI Knowledge Hub & Training — single source of truth, precedents, CPD

## Communication Protocol

Inter-agent messages via structured JSON:

```json
{
  "from": "AI_Underwriter",
  "to": "AI_Claims_Tech",
  "type": "handoff",
  "payload": {
    "policy_status": "active",
    "coverage_recipe": { "liability": 10000000, "recovery": 2000000 },
    "incident_location": { "lat": -26.1234, "long": 28.5678 }
  }
}

Escalation RulesEstimated loss > R5m → AI Incident Response Desk (critical)  
Suspected fraud / non-disclosure → AI Compliance Officer (high)  
Complex liability → human Key Individual escalation

Human-in-the-Loop FallbackAny agent can escalate to licensed human Key Individual via:json

{ "type": "human_escalation", "reason": "complex liability dispute" }

AI Compliance Officer has final override authority.AV-ready. Regulator-aligned. Open standard.Built by Sharné — December 16, 2025 

