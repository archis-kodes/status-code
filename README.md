
# Medicine Equivalence Checker (OpenFDA)

A minimal Flask + HTML app that compares two medicine names using the OpenFDA Drug Label API, estimates a confidence score for "will it work the same way for the same problem", and shows indications, adverse reactions (side effects), and warnings.

> ⚠️ **Limitations**
> - OpenFDA primarily covers FDA-regulated (US) drugs. Local/non-US brands may not be found.
> - The confidence score is heuristic (ingredients, route, dosage form, parsed strengths). It is **not medical advice**.
> - Strength parsing from free text can be imperfect.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open http://localhost:8000 in your browser.

## How scoring works

- **Ingredient overlap (60%)**: Jaccard similarity of active ingredient names (from `openfda.substance_name` and `active_ingredient` text).
- **Route match (15%)**: exact match of `openfda.route` (e.g., ORAL vs TOPICAL).
- **Dosage form match (10%)**: exact match of `openfda.dosage_form` (e.g., TABLET vs SUSPENSION).
- **Strength match (15%)**: compares numeric values with same unit within 10–25% tolerance, parsed from `active_ingredient` field if present.

If there is **no ingredient overlap**, the total score is capped at 30.

## API

`POST /api/compare`

```json
{
  "prescribed": "Tylenol",
  "available": "Acetaminophen 500 mg tablets"
}
```

Response:
```json
{
  "score": 97.5,
  "breakdown": {
    "ingredient_similarity": 1.0,
    "route_match": 1.0,
    "form_match": 1.0,
    "strength_match": 1.0
  },
  "prescribed": { ... },
  "available": { ... }
}
```
