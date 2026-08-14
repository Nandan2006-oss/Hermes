# Hermes

**AI-powered product intelligence for industrial commerce.**

Hermes turns scattered, incomplete product information — spec sheets, supplier pages, one-line descriptions — into structured, validated, and explainable product data that's ready for a commerce catalog.

Built for **UniHack by Unilog** (Hack2skill), under the challenge: *AI-Powered Product Intelligence for Industrial Commerce*.

---

## The problem

Industrial companies manage product information scattered across websites, catalogs, and technical documents. Turning that scattered information into accurate, structured, commerce-ready data is slow, manual, and error-prone — and at catalog scale, it doesn't hold up.

## What Hermes does

Give Hermes whatever you have — a product name, a raw description, a spec sheet PDF, a supplier URL — and it returns a complete structured product record:

- **Structured data generation** — extracts and organizes attributes into a category-aware schema, not a generic key-value blob
- **Enrichment** — fills gaps using AI reasoning and similar products in the catalog, clearly marked as inferred rather than sourced
- **Validation** — catches inconsistencies, unit mismatches, and conflicting values across sources
- **Explainability** — every field carries its source, extraction method, and a confidence score, so nothing is a black box
- **Scale** — batch-processes full catalogs, not just one product at a time

Hermes doesn't just guess. When data is missing or sources disagree, it says so — and shows its work.

---

## How it works

```
Ingestion → Extraction → Structuring → Enrichment & Validation → Explainable Output
```

1. **Ingestion** — accepts raw text, PDF spec sheets, supplier URLs, or partial CSV/JSON rows
2. **Extraction** — an LLM pulls structured attributes out of unstructured text, tables, and documents
3. **Structuring** — extracted fields are mapped onto a category-specific schema (a bearing and a cable connector don't share attributes)
4. **Enrichment & validation** — missing fields are inferred where reasonable, conflicting or out-of-range values are flagged, everything gets a confidence score
5. **Output** — a commerce-ready structured record, with full source provenance per field

---

## Tech stack

| Layer | Tool |
|---|---|
| AI / extraction engine | Gemini API (Google AI Studio, free tier) — native PDF understanding, structured JSON output |
| Backend | Python, FastAPI |
| Database | SQLite |
| Frontend | React |
| Web fetching | `requests` + `BeautifulSoup` (for URL-based product pages) |

All free-tier tools — no paid services required to run this project.

---

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com)

### Setup

```bash
# clone the repo
git clone https://github.com/Nandan2006-oss/hermes.git
cd hermes

# backend setup
cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt

# add your Gemini API key
cp .env.example .env
# then edit .env and set GEMINI_API_KEY=your_key_here

# run the backend
uvicorn main:app --reload
```

```bash
# frontend setup (in a new terminal)
cd frontend
npm install
npm run dev
```

The app should now be running at `http://localhost:5173` (frontend) with the API at `http://localhost:8000`.

---

## Usage

1. Open the app and go to **Add a product**
2. Provide any combination of: product name, description, a spec sheet PDF, or a source URL
3. Click **Generate product intelligence**
4. Review the structured output — each field shows its source and confidence; flagged fields need a human look
5. Use **Batch mode** to run multiple products at once and see catalog-wide completeness and confidence stats

---

## Project structure

```
hermes/
├── backend/
│   ├── main.py              # FastAPI app entrypoint
│   ├── extraction/          # LLM prompts and extraction logic
│   ├── schemas/              # category-specific product schemas
│   ├── validation/          # conflict detection, confidence scoring
│   └── db/                  # SQLite models and access
├── frontend/
│   ├── src/
│   │   ├── components/      # input form, results view, batch dashboard
│   │   └── App.jsx
│   └── package.json
└── README.md
```

---

## Why Hermes is different

Most extraction tools stop at "LLM pulls out some fields." Hermes treats **trust** as the core feature, not an afterthought:

- Every field is traceable to its source — click any value to see exactly where it came from
- Conflicts between sources are surfaced, not silently resolved
- Confidence scores are functional — low-confidence fields route to review instead of shipping silently
- Batch runs report real numbers (completeness %, flagged count, avg processing time) instead of a single cherry-picked demo product

---

## Roadmap

- [ ] Human-in-the-loop review queue for flagged fields
- [ ] Similarity search across the catalog to improve enrichment quality
- [ ] Export to common PIM/catalog formats
- [ ] Confidence calibration testing against verified ground-truth data

---

## Team

Built by Nandan Nalwade M for UniHack by Unilog, 2026.

## License

MIT
