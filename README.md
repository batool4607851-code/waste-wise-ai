# WasteWise AI

## AI-Powered Manufacturing Loss & Rework Intelligence

> **Turn factory data into actionable waste intelligence.**

WasteWise AI is an AI-powered decision-support application for food manufacturing. It combines factory spreadsheets, PDFs and SOP documents to help operations teams identify costly manufacturing losses, investigate potential contributing factors, and determine what to check next.



---

## The Problem

Food manufacturers often have useful operational information scattered across:

- CSV and Excel production records
- Waste and loss logs
- Quality-control records
- SOPs and operational manuals
- Employee knowledge

The challenge is not simply collecting data. It is turning fragmented information into clear, evidence-based decisions.

Managers need to answer:

- Where are losses occurring?
- Which products, lines, shifts, or categories are most affected?
- What are the major loss patterns?
- How much is the loss costing?
- What does the factory's own SOP recommend?
- What should the team investigate next?

---

## Our Solution

WasteWise brings these sources together into one workflow:

```text
CSV / XLSX
     │
     ▼
Python Analytics ───────┐
                        │
PDF / SOP ──► RAG ──────┤
                        │
                        ▼
              Evidence-Based Insight
                        │
                        ▼
              Investigation Recommendation
```

The application follows:

> **Upload → Analyze → Ask → Investigate**

---

## Core Features

### 1. Production & Loss Data

Upload factory data in:

- CSV
- XLSX

WasteWise validates the uploaded data and calculates relevant manufacturing-loss metrics.

### 2. Manufacturing Analytics

The dashboard can analyze:

- Total production
- Total loss/waste
- Loss rate
- Loss by product
- Loss by production line
- Loss by shift
- Loss by category
- Loss by reason
- Trends over time
- Basic anomalies

### 3. SOP Intelligence with RAG

Upload factory SOPs and operational documents as PDFs.

WasteWise:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Search
 ↓
Relevant Evidence
 ↓
AI Answer
```

Document-based answers include source information where available.

### 4. AI Analyst

Groq combines calculated analytics, document evidence, and visual evidence to explain findings in natural language.

The AI can help answer questions such as:

> Which production line should we investigate first?

> What are the main loss drivers?

> What does the SOP recommend?


### 5. Investigation Recommendations

WasteWise does not simply identify a problem.

It can suggest practical investigation steps based on the available evidence.

Example:

```text
Finding:
Line 2 has an unusually high loss rate.

Data Evidence:
Line 2 shows higher packaging losses than other lines.

SOP Evidence:
The relevant SOP contains procedures for checking packaging equipment.

Investigation Hypothesis:
A packaging-related issue could be contributing to the elevated loss.

Recommended Checks:
1. Review Line 2 calibration records.
2. Compare affected shifts.
3. Inspect packaging-material lots.
4. Verify relevant SOP compliance.

Confidence:
Medium
```

The system explicitly distinguishes evidence from hypotheses and recommendations.

---

## Manufacturing Loss & Rework Model

WasteWise is designed to distinguish different types of manufacturing outcomes rather than treating everything as generic "food waste."

The broader model can represent:

- Production
- Process loss
- Material loss
- Packaging loss
- Quality deviation
- Rework
- Recovery
- Final loss

For example:

```text
Production
    ↓
Quality Deviation
    ↓
Rework
    ↓
Recovered Material ──► Saleable Product
    │
    └─────────────────► Final Loss
```

This allows WasteWise to investigate questions such as:

- Which quality deviations generate the most rework?
- Which rework events ultimately result in final loss?
- Which products require the most rework?
- Where is the greatest financial impact occurring?

---

## AI Trust & Safety

WasteWise is a **decision-support system**, not an autonomous factory-control system.

The application distinguishes:

| Type | Example |
|---|---|
| **FACT** | Line 2 has a 7.12% loss rate. |
| **INFERENCE** | The findings may be related. |
| **RECOMMENDATION** | Review Line 2 calibration records. |

WasteWise must not present a hypothesis as a confirmed root cause.

It must not:

- invent measurements
- invent SOP requirements
- make autonomous product-disposal decisions
- make autonomous quality-approval decisions

When evidence is insufficient, the system should communicate that clearly.

---

## Technology Stack

### Frontend

- Streamlit

### Data Processing

- Python
- Pandas
- NumPy

### Documents

- PyPDF

### Retrieval

- FAISS
- Embeddings

### AI

- xAI / Groq
- Natural-language reasoning

### Development

- GitHub
- Google Colab for experimentation when useful

### Deployment

- Streamlit Community Cloud

The architecture intentionally avoids unnecessary infrastructure so that the core product remains reliable and achievable within the hackathon timeframe.



---

## Project Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │                             │
              ▼                             ▼
          CSV/XLSX                         PDF
              │                             │
              ▼                             ▼
        Python/Pandas                      RAG
              │                             │
              └──────────────┼──────────────┘
                             ▼
                      Grok Reasoning
                             │
                             ▼
                    WasteWise AI Insight
                             │
                             ▼
                   Human Investigation
```

---

As development progresses, additional analytics, data-loading, RAG, AI modules will be added to `src/`.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/waste-wise-ai.git
cd waste-wise-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a local `.env` file containing:

```text
XAI_API_KEY=your_api_key_here
XAI_MODEL=your_model_name
```

Never commit `.env` or API keys to GitHub.

For deployment, configure secrets through the deployment platform.

The repository contains `.env.example` as a safe template.

---

## Running the Application

Run:

```bash
streamlit run app.py
```

The application should open in your browser.

---

## Demo Workflow

The intended demonstration flow is:

```text
1. Upload factory data
        ↓
2. View manufacturing-loss dashboard
        ↓
3. Upload an SOP
        ↓
4. Ask WasteWise a question
        ↓
5. Retrieve relevant SOP evidence
        ↓
6. Combine data + SOP
        ↓
7. Generate an investigation finding
```

A synthetic demonstration dataset may be used to demonstrate the application.

> **Synthetic Demo Data — Not Real Factory Data**

---

## MVP Scope

The hackathon MVP focuses on:

- CSV upload
- Excel upload
- Manufacturing-loss analytics
- Dashboard
- PDF/SOP upload
- RAG
- Natural-language AI analysis
- Cross-source reasoning
- Investigation recommendations
- Basic anomaly detection

The development principle is:

> **WORKING > SIMPLE > RELIABLE > IMPRESSIVE > COMPLEX**

---

## Out of Scope

The MVP does **not** attempt to build:

- ERP integrations
- IoT infrastructure
- Live machine control
- Autonomous factory operations
- Advanced forecasting
- Custom computer-vision model training
- Predictive maintenance
- Digital twins
- Mobile applications
- Autonomous product disposition

These may be considered future capabilities rather than hackathon MVP requirements.




## Future Roadmap

```text
Waste Intelligence
        ↓
Predictive Waste
        ↓
Yield Intelligence
        ↓
Inventory & Expiry Intelligence
        ↓
Quality Intelligence
        ↓
Computer Vision
        ↓
Production Optimization
        ↓
Factory Digital Twin
        ↓
AI Factory Operations OS
```

The long-term vision is to expand WasteWise from manufacturing-loss intelligence into a broader AI operations platform for food manufacturing.



---

## Development Philosophy

WasteWise is intentionally built in controlled phases:

```text
PLAN
  ↓
BUILD
  ↓
RUN
  ↓
TEST
  ↓
FIX
  ↓
CHECKPOINT
  ↓
NEXT PHASE
```

The data and analytics foundation is built before the higher-level AI reasoning components.

This reduces technical risk and makes the application easier to test and debug.



---

## License

No open-source license has been selected for this hackathon repository yet.
