# Faultline Prompt Design

## Purpose

Mythadis Faultline uses structured prompts to turn a submitted idea, plan,
claim, product decision, or technical design into practical risk analysis and
validation planning. The tool does not guarantee truth, does not browse the
web, and does not create citations. It does not store prompts or results.

The output is decision support, not a final decision. High-stakes legal,
medical, financial, safety, security, and compliance decisions still require
qualified human review.

## Two-Pass Review

The **Primary Faultline Scanner** produces the initial report. Its role is to
surface hidden assumptions, pressure points, collapse risks, weak evidence,
failure conditions, validation tests, and questions that should be answered
before commitment.

The **Independent Faultline Auditor** receives the original input, selected scan
mode, and parsed scanner report. It challenges missed risks, vague reasoning,
weak tests, and unsupported risk ratings. The second pass reduces simple
agreement bias, but it is still AI output and may miss important issues.

Neither pass claims certainty, external access, or factual verification beyond
the submitted text.

## Scan Modes

### `business_idea`

Scanner guidance covers market assumptions, customer pain, buyer clarity,
willingness to pay, pricing, differentiation, competition, distribution, sales
friction, operating burden, margin risk, and failure reasons.

Auditor guidance challenges whether a real buyer exists, paid intent is tested,
distribution is credible, founder effort can scale, and substitutes or
competition were understated.

### `technical_architecture`

Scanner guidance covers dependencies, scaling limits, resilience, single points
of failure, data flow, integrations, operations, recovery, security,
observability, and failure modes.

Auditor guidance challenges hidden coupling, ownership boundaries, failover,
rollback, operational burden, security assumptions, and vague resilience
claims.

### `product_feature`

Scanner guidance covers user value, adoption friction, usability, edge cases,
maintenance cost, workflow fit, unnecessary complexity, and assumptions about
user behavior.

Auditor guidance challenges whether the feature is needed, whether a simpler
solution exists, its support burden, likely adoption, and ignored edge cases.

### `security_risk_decision`

Scanner guidance covers threats, control gaps, compliance and operational risk,
misuse, blast radius, recovery, identity and access, monitoring, residual risk,
and risk acceptance.

Auditor guidance challenges the threat model, compensating controls, blast
radius, monitoring, recovery, compliance language, and whether risk acceptance
is justified.

### `strategic_decision`

Scanner guidance covers incentives, timing, opportunity cost, reversibility,
stakeholders, second-order consequences, dependencies, evidence, downside,
execution, and lock-in.

Auditor guidance challenges reversibility, timing, incentive alignment,
opportunity cost, second-order effects, and whether evidence supports
commitment.

## Safety And Limitations

Both prompts state that Faultline provides structured risk analysis rather than
guaranteed truth. They prohibit invented citations, sources, data, legal or
compliance claims, market numbers, and technical facts. They also prohibit
claims of web browsing or access to external systems.

When evidence is absent, the model is asked to identify what is missing. For
high-stakes topics, findings must remain risk analysis support and recommend
qualified review where appropriate. Outputs must remain defensive,
evaluative, validation-oriented, and must not enable harm, evasion, credential
theft, exploitation, or unsafe activity.

## Scanner JSON Contract

The finalized scanner JSON contract is:

```json
{
  "faultline_summary": "string",
  "surface_claim": "string",
  "hidden_assumptions": ["string"],
  "pressure_points": ["string"],
  "collapse_risks": ["string"],
  "weak_evidence": ["string"],
  "what_would_break_this": ["string"],
  "validation_tests": ["string"],
  "questions_before_commitment": ["string"],
  "risk_level": "low | medium | high | critical",
  "recommended_next_move": "string"
}
```

Fields must not be renamed, added, or removed without an explicit contract
change across the schema, prompt, parser, route, tests, and documentation.

## Auditor JSON Contract

The finalized auditor JSON contract is:

```json
{
  "audit_summary": "string",
  "missed_risks": ["string"],
  "weak_or_vague_findings": ["string"],
  "validation_plan_gaps": ["string"],
  "risk_level_challenge": "string",
  "recommended_report_improvements": ["string"],
  "auditor_confidence": "low | medium | high",
  "final_caution": "string"
}
```

The same coordinated-change rule applies to the auditor contract.

## Parsing And Fallbacks

Provider text is parsed as JSON and validated against the corresponding
Pydantic report model. The parser can recover JSON from Markdown fences or
limited surrounding text. Malformed output or invalid constrained values
produce an explicit conservative fallback report; raw provider output is not
returned in an error or stored.

## Known Limitations

- Findings depend on the quality and specificity of the submitted text.
- The models may overlook risks, infer incorrectly, or produce generic advice.
- The auditor may repeat scanner assumptions instead of challenging them.
- No external facts, current market data, laws, vulnerabilities, or compliance
  obligations are verified.
- A structured report cannot replace domain expertise or accountable human
  judgment.

## Rules For Future Changes

1. Keep scanner and auditor roles separate.
2. Preserve JSON field names unless a versioned API change is intentional.
3. Update schema, prompt, parser, route tests, and this document together.
4. Keep mode guidance static, explicit, and independently testable.
5. Preserve the no-browsing, no-citation, no-storage, and backend-only key
   boundaries.
6. Test prompt changes with mocked providers; automated tests must never call a
   real provider.
