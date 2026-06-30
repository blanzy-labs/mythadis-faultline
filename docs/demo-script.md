# Demo Script

## Demo Purpose

Show how AI Faultline turns a proposal into a structured first-pass risk
report, challenges it with a second AI, and exports the current result without
adding accounts or saved history.

## 60–90 Second Short Demo

**0-10 seconds: Introduce it**

"AI Faultline is a local-first AI stress-test tool from Blanzy Labs that finds
the crack before the collapse. It challenges an idea before time and money are
committed."

Show the title, tagline, and backend-online indicator.

**10-25 seconds: Set up the scan**

Paste a fictional sample proposal. Select the relevant scan mode, one provider
for the Primary Scanner, and one for the Independent Auditor.

"The browser sends provider choices, not API keys. Credentials stay in the
local backend."

**25-55 seconds: Run and read**

Run the scan. Point out the hidden assumptions, weak evidence, collapse risks,
risk level, and recommended next move.

"The first model produces the structured Faultline Report. The second model
audits it for missed risks, vague findings, and gaps in the validation plan."

**55-75 seconds: Export and boundaries**

Download the Markdown report.

"The current result stays in browser memory. Markdown is generated in the
browser and saved only when I download it. There are no accounts, database,
prompt history, or telemetry."

**75-90 seconds: Close**

"Faultline does not browse or verify facts, and AI output can be wrong. It is a
way to ask better questions before commitment. Find the crack before the
collapse."

## 5–8 Minute Walkthrough

1. **Open with the purpose.** Show "AI Faultline" and "Find the crack before
   the collapse." Explain that this is part of the Blanzy Labs AI app family
   and is a practical stress-testing tool.
2. **Explain local setup.** Point to the backend status. State that the app runs
   locally by default, while real scans still send data to the selected
   external providers.
3. **Enter an idea.** Use a fictional, non-sensitive sample and explain what
   makes a useful input: enough detail to expose assumptions and tradeoffs.
4. **Choose a scan mode.** Briefly compare business idea, technical
   architecture, product feature, security risk decision, and strategic
   decision.
5. **Choose the scanner provider.** Explain that the Primary Scanner creates
   the initial structured analysis.
6. **Choose the auditor provider.** Explain that the Independent Auditor
   receives the original input and scanner report, then challenges the first
   pass. It may use the same or a different configured provider.
7. **Run the scan.** Mention that provider calls occur only now, not during
   startup or health checks.
8. **Explain the Faultline Report.** Walk through the summary, surface claim,
   assumptions, pressure points, collapse risks, weak evidence, break
   conditions, validation tests, questions, risk level, and next move.
9. **Explain the Second-AI Audit Review.** Highlight missed risks, vague
   findings, validation gaps, the risk level challenge, improvements,
   confidence, and final caution. Do not imply the auditor guarantees quality.
10. **Download Markdown.** Show the download action and explain that export is
    generated from the current browser state without a backend export endpoint.
11. **Explain privacy boundaries.** State that there is no login, database,
    history, browser storage, or telemetry. Clearly warn that scan content is
    sent through the local backend to the selected providers.
12. **Close with limitations.** Faultline does not browse the web, verify facts,
    or replace qualified human review. Its job is to expose questions and tests
    that deserve attention.

## Demo Setup Checklist

- [ ] Start the backend and frontend and confirm the backend indicator is online.
- [ ] Test the sample input before recording.
- [ ] Confirm the selected provider credentials work.
- [ ] Close terminals or tabs that could expose private information.
- [ ] Keep `.env`, provider dashboards, billing pages, and account pages closed.
- [ ] Disable notifications and remove confidential desktop items.
- [ ] Prepare `docs/sample-report.md` as the fallback.
- [ ] Confirm the download location contains no private reports.
- [ ] Use a clean browser window without unrelated extensions or tabs.

## Recommended Sample Inputs

**Business idea**

> We are considering launching a local-first AI tool that helps small
> businesses stress-test product ideas before they spend money building them.

**Operational workflow**

> We want to replace our manual incident review process with an AI-assisted
> workflow that identifies weak evidence, missed risks, and follow-up
> validation tests.

**Product feature**

> We plan to add a weekly executive summary that condenses project status,
> unresolved decisions, and delivery risks into one page for team leads.

All demo inputs should be fictional or sanitized.

## What to Show on Screen

- App title, tagline, and backend status
- A fictional input and selected scan mode
- Scanner and auditor provider choices
- Loading state
- Faultline Report
- Second-AI Audit Review
- Model metadata without credentials
- Markdown download action
- The public sample report when explaining fallback behavior

## What Not to Show

- Real API keys or `.env` contents
- Private prompts, customer data, or proprietary plans
- Provider dashboards, account identifiers, billing, or quota details
- Terminal history that may contain secrets
- An exported report containing sensitive material

Do not claim that Faultline browses the web, verifies facts, guarantees truth,
or replaces expert review.

## Fallback Demo if Provider Keys Are Unavailable

1. Show the running UI and explain the input, scan modes, and provider
   selectors.
2. Open [sample-report.md](sample-report.md).
3. Walk through the scanner report, audit, metadata, limitations, and expected
   Markdown shape.
4. Explain that live scans require backend-side provider keys.
5. Label the report clearly as sample content. Do not present it as a live
   provider result.

## Closing Talking Points

- Two passes encourage challenge instead of simple model agreement.
- Structured output turns concerns into assumptions, risks, questions, and
  validation tests.
- Provider credentials remain in the backend.
- Results are not retained by the app unless the user downloads Markdown.
- Provider data handling still matters because real scans leave the machine.
- AI analysis is fallible decision support, not guaranteed truth.
- Find the crack before the collapse.
