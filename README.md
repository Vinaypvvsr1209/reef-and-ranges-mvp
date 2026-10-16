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
