# Hermes

**Evidence-first product data extraction and normalization.**

Hermes is an AI-powered product information extraction system designed to convert messy product descriptions into **structured, validated, and traceable product data**.

Instead of simply asking an LLM to return JSON, Hermes is being designed around three core ideas:

> **Evidence → Confidence → Conflict Detection**

The goal is to make extracted product data easier to **trust, verify, and eventually use in real content and commerce systems.**

---

## 🚧 Current Status

Hermes is currently under active development as an MVP.

### Implemented

* Structured product information extraction using Gemini
* Pydantic-based output validation
* Evidence attached to extracted fields
* Confidence scores for extracted values
* Product-level validation
* Basic value normalization
* Initial conflict-detection foundation
* FastAPI backend
* Health-check endpoint

### In Progress

* Multi-source evidence
* Robust conflict detection
* Confidence calibration
* UOM normalization
* Ground-truth evaluation
* Extraction accuracy metrics
* Better handling of ambiguous product descriptions

---

# The Problem

Product data is often messy.

A single product description might contain information like:

```text
Diablo 1/2" x 18" Sanding Belt, 6 Pack
```

A traditional extraction system might produce:

```json
{
  "width": "1/2 in",
  "length": "18 in",
  "quantity": 6
}
```

But this doesn't tell us:

* Where did the value come from?
* Was the value explicitly present?
* How confident is the system?
* What happens if another source says something different?
* Can a human verify the extraction?

Hermes attempts to solve these problems by making extracted information **traceable**.

---

# Hermes Approach

Instead of:

```text
Product Description
        ↓
       LLM
        ↓
      JSON
```

Hermes is being designed as:

```text
                Product Data
                     │
                     ▼
              ┌──────────────┐
              │   Extraction │
              │    Gemini    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   Evidence   │
              │     Layer    │
              └──────┬───────┘
                     │
              ┌──────┴───────┐
              ▼              ▼
        Confidence      Validation
              │              │
              └──────┬───────┘
                     ▼
             Conflict Detection
                     │
                     ▼
              Structured Data
```

The long-term goal is for Hermes to answer not only:

> **"What is the product information?"**

but also:

> **"Why should I trust this information?"**

---

# Example

### Input

```text
DCB518ASTS06G Diablo 1/2" x 18" Sanding Belt, 6 Pack
```

### Hermes Output

```json
{
  "part_number": "DCB518ASTS06G",
  "brand": "Diablo",
  "product_type": "Sanding Belt",
  "quantity_value": 6,
  "quantity_uom": "pc",
  "width": {
    "value": "1/2 in",
    "evidence": "1/2\"",
    "source": "Part_Desc",
    "confidence": 0.98
  },
  "length": {
    "value": "18 in",
    "evidence": "18\"",
    "source": "Part_Desc",
    "confidence": 0.98
  },
  "conflicts": []
}
```

The important difference is that Hermes doesn't only return:

```text
width = 1/2 in
```

It also returns:

```text
Evidence: 1/2"
Source: Part_Desc
Confidence: 0.98
```

This makes the extraction **auditable**.

---

# Evidence

Every important extracted field can contain:

| Property     | Purpose                         |
| ------------ | ------------------------------- |
| `value`      | Normalized extracted value      |
| `evidence`   | Exact text supporting the value |
| `source`     | Where the evidence came from    |
| `confidence` | Model's confidence from 0–1     |

For example:

```json
{
  "value": "1/2 in",
  "evidence": "1/2\"",
  "source": "Part_Desc",
  "confidence": 0.98
}
```

The evidence should come directly from the input rather than being invented by the model.

---

# Conflict Detection

One of Hermes' key goals is detecting disagreements between sources.

For example:

```text
Part_Desc:
1/2" sanding belt

Catalog:
3/4" sanding belt
```

A conventional extraction system might silently choose one value.

Hermes should instead be able to represent the disagreement:

```text
Width
├── 1/2 in
│   └── Part_Desc
│
└── 3/4 in
    └── Catalog

CONFLICT
```

This allows the system to eventually make better decisions based on:

* source reliability
* evidence quality
* confidence
* explicitness of the information
* agreement between sources

---

# Current Data Model

Hermes currently uses Pydantic models to define its structured output.

Conceptually:

```text
AnalysisResponse
│
├── part_number
├── brand
├── product_type
├── quantity_value
├── quantity_uom
│
├── width
│   ├── value
│   ├── evidence
│   ├── source
│   └── confidence
│
├── length
│   ├── value
│   ├── evidence
│   ├── source
│   └── confidence
│
└── conflicts
```

Using a schema ensures that the LLM output is not treated as arbitrary text.

---

# Tech Stack

### Backend

* **Python**
* **FastAPI**
* **Pydantic**

### AI

* **Google Gemini**
* Gemini structured output

### Configuration

* **python-dotenv**

### Development

* Git
* GitHub
* VS Code

---

# API

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Analyze Product

```http
POST /analyze
```

Request:

```json
{
  "text": "DCB518ASTS06G Diablo 1/2\" x 18\" Sanding Belt, 6 Pack"
}
```

The endpoint sends the description to Gemini, validates the structured response using Pydantic, normalizes extracted dimensions, validates the result, and returns the structured product information.

---

# Project Structure

The project is currently centered around the FastAPI backend.

```text
Hermes/
│
├── backend/
│   ├── ...
│
├── .gitignore
├── README.md
└── ...
```

The architecture will evolve as Hermes gains additional processing and evaluation components.

---

# Development Philosophy

Hermes is being built incrementally.

The project intentionally avoids treating an LLM as a black box.

Each stage is being tested and understood before moving to the next:

```text
Understand the data
        ↓
Build extraction
        ↓
Attach evidence
        ↓
Validate output
        ↓
Normalize values
        ↓
Detect conflicts
        ↓
Calibrate confidence
        ↓
Evaluate against ground truth
```

The **200-item ground-truth dataset** is being used as the primary evaluation dataset.

This allows Hermes to be tested against known expected outputs rather than relying only on whether an individual example "looks correct."

---

# Roadmap

### Phase 1 — Foundation

* [x] FastAPI backend
* [x] Product extraction
* [x] Structured Gemini output
* [x] Pydantic validation
* [x] Evidence fields
* [x] Confidence fields
* [x] Basic normalization
* [x] Initial conflict model

### Phase 2 — Evidence Engine

* [ ] Multiple evidence sources
* [ ] Evidence-to-value mapping
* [ ] Stronger evidence validation
* [ ] Source reliability

### Phase 3 — Conflict Engine

* [ ] Detect conflicting values
* [ ] Associate each value with its source
* [ ] Handle multiple conflicting fields
* [ ] Decide when conflicts should affect confidence

### Phase 4 — Evaluation

* [ ] Run against the 200-item ground truth
* [ ] Measure extraction accuracy
* [ ] Measure field-level accuracy
* [ ] Evaluate evidence correctness
* [ ] Evaluate conflict detection
* [ ] Analyze failure cases

### Phase 5 — Product

* [ ] User interface
* [ ] Human-readable evidence display
* [ ] Confidence visualization
* [ ] Conflict warnings
* [ ] Product comparison
* [ ] Exportable structured data

---

# Why "Hermes"?

Hermes was the messenger of the Greek gods.

The name reflects the role of the system:

```text
Messy Product Data
        ↓
      Hermes
        ↓
Structured + Explainable Product Data
```

Hermes acts as a bridge between unstructured product information and reliable structured data.

---

# Current Goal

The immediate goal is not simply to make an LLM extract product attributes.

The goal is to build a system where every important extracted value can answer:

> **What is the value?**

> **Where did it come from?**

> **How confident are we?**

> **Does other evidence disagree?**

That is the foundation Hermes is being built on.
