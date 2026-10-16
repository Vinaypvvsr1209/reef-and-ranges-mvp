# reef-and-ranges-mvp
# Reef & Ranges Tours — AI Booking & FAQ MVP (Part 2)

## Overview
This prototype solves the two biggest operational bottlenecks identified in the audit for **Reef & Ranges Tours (Cairns)**:
1. **Eliminating Double Bookings:** Replaces the shared spreadsheet with real-time capacity validation.
2. **24/7 Instant Enquiry & FAQ Triage:** Answers repetitive questions (pickup times, packing lists, weather policies) and escalates low-confidence queries to human staff.

## Features Included
- **Access Control:** Role-based toggle with password-protected Staff Admin view (Demo passcode: `cairns2026`).
- **Synthetic Data Only:** Contained in `tours_data.csv`.
- **Automated Tests:** Included in `test_app.py` (run via `pytest`).

## Short AI-Use Note
- **Tools Used:** Gemini (Google AI) for rapid prototyping, synthetic dataset generation, and unit test scaffolding.
- **Main Prompts Given:** Asked AI to generate a lightweight Streamlit reservation validator and FAQ router tailored to Cairns reef/rainforest operators with human-in-the-loop escalation.
- **What the AI Got Wrong Initially:** Initially, the AI suggested connecting directly to an external LLM API requiring secret keys in the repo, and didn't enforce strict seat capacity limits on concurrent states.
- **What I Reviewed & Changed:** Removed external API key dependencies so the repo runs safely out-of-the-box with zero credential exposure, added explicit boundary checks (`booked + requested > capacity`) to strictly prevent double bookings, and enforced human fallback for weather cancellations.
## Part 3: Automation / Agent Architecture & Safe-Fail Design

### Workflow Summary
Built in **n8n**, this workflow automates the end-to-end enquiry triage for Reef & Ranges Tours:
1. **Trigger & Ingestion:** Captures incoming website and Facebook enquiries using synthetic customer payloads.
2. **AI Qualification & Confidence Scoring:** Evaluates guest count, tour type, and message intent, assigning a confidence score (`0.0` to `1.0`).
3. **Conditional Routing (Human-in-the-Loop):**
   - **High Confidence (>= 0.80):** Logs the record into the central CRM/booking sheet and dispatches an instant, personalized confirmation and FAQ follow-up (`Node 5B`).
   - **Low Confidence (< 0.80) or High-Risk Keywords:** Blocks automated replies and escalates immediately to a human reservation agent (`Node 5A`).

### How It Fails Safely (Safe-Fail Mechanisms)
1. **When the AI is Unsure or Wrong (Hallucination Guard):**
   - Any enquiry mentioning weather/cyclone risks, custom private charters, refunds, or group sizes > 10 automatically drops the confidence score below threshold (`0.42`) and sets `requires_human = true`.
   - Instead of guessing prices or making unsafe weather promises, the workflow suppresses the outbound email and creates a high-priority task for the Operations Manager with the draft held for review.
2. **When an External API (LLM / Email / CRM) is Down:**
   - **Retry with Exponential Backoff:** In production, external HTTP/API nodes are configured with n8n's built-in retry policy (3 attempts, 5-second backoff).
   - **Error Trigger / Dead-Letter Queue:** If the AI API times out or returns a `5xx` error, the node defaults to `requires_human = true` (Fail-Closed). The raw customer enquiry is written to a backup fallback sheet and routed directly to staff so zero leads are lost even during an outage.
3. **Zero Credential Exposure:**
   - All workflow exports use environment placeholders and synthetic execution blocks, ensuring no API keys, tokens, or real customer PII are exposed.
