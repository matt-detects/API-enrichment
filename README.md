# API-enrichment

This project demonstrates basic enrichment workflows using external threat intelligence APIs.

The focus is on integrating detection events with contextual data to improve signal quality and triage effectiveness.

---

## Objectives

- Call REST APIs using Python
- Handle authentication headers
- Parse JSON responses
- Extract relevant threat context
- Structure enriched output for downstream use

---

## Key Concepts Demonstrated

- Python `requests` library
- API parameter handling
- JSON parsing and error handling
- Structured enrichment output
- Simple resilience handling (status codes, failures)

---

## Example Use Cases

- IP reputation lookup during alert triage
- Enriching suspicious domains with external intelligence
- Adding contextual scoring to detection outputs

---

## Notes

This lab focuses on workflow logic and structured enrichment handling.

API keys are excluded from the repository and must be configured locally.

All examples use public or synthetic data.
