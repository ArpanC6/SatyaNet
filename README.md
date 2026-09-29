# SatyaNet

**Trust-Aware Field Intelligence for Disaster Response**

SatyaNet ingests field media - photos and videos from volunteers, NGOs, and first responders - auto-organizes evidence by project, location, and timeline, and assigns a Bayesian trust score (0–100) to every AI insight so responders know exactly how much to rely on each piece of evidence before acting on it.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status: Active](https://img.shields.io/badge/status-active-success.svg)

---

## Table of Contents

- [The Problem](#the-problem)
- [Our Solution](#our-solution)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Why Bayesian Uncertainty](#why-bayesian-uncertainty)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Testing](#testing)
- [Author](#author)
- [License](#license)

---

## The Problem

During disasters - floods, earthquakes, communal violence - social media floods with **fake, recycled, or mislabeled media**.

- In **2023 Manipur violence**, a 2018 video went viral as current.
- In **2024 Assam floods**, roughly **40% of relief-evidence photos** submitted to NGOs were duplicates or mislabeled.

NGOs and NDRF teams waste critical hours and resources acting on false evidence - while real victims wait. Existing tools either:

1. Give a binary label ("real" / "fake") with no confidence measure, or
2. Rely on a single signal (e.g., reverse image search) that fails against novel fakes.

Neither is enough when lives and resources are at stake.

---

## Our Solution

SatyaNet combines **Bayesian uncertainty quantification** with **media forensics** to deliver a calibrated trust score for every piece of field evidence.

Instead of "this is AI-verified," SatyaNet says:

> "This damage assessment has **50.5/100** confidence. Reasons: EXIF timestamp ambiguous (±3 days), partial duplicate match in known-fake database, and weather conditions inconsistent with satellite pass."

Responders can then decide:

- **Act now** (score ≥ 80, verified)
- **Corroborate with a second source** (score 50–79, needs review)
- **Discard** (score < 50, likely fake)

---

## Key Features

### 1. Evidence Ingest with Cloudinary

- Upload field photos and videos via Cloudinary
- Automatic GPS and timestamp extraction from EXIF metadata
- Auto-tagging via Cloudinary AI (water, road, crowd, damage)
- Folder organization by project, location, and timeline

### 2. Bayesian Truth Score (Core Innovation)

Five weighted weak signals are fused via Bayesian inference:

| Signal | Weight | What It Measures |
|--------|--------|------------------|
| EXIF Integrity | 25% | Metadata intact? GPS and timestamp present? |
| Temporal Plausibility | 20% | Does the timestamp match the claim? |
| Satellite Consistency | 25% | Weather matches satellite pass at location and time? |
| Duplicate Detection | 20% | Perceptual hash match against known fakes? |
| Image Quality | 10% | Contrast adequate for forensic analysis? |

Output: calibrated trust score 0–100 with per-signal explanations.

- Score ≥ 80 - VERIFIED - safe to act
- Score 50–79 - NEEDS REVIEW - corroborate first
- Score < 50 - LIKELY FAKE - do not act

### 3. Semantic Evidence Search

Natural-language queries across the evidence corpus using Qdrant vector search:

- "Show flood damage from Siliguri, last week"
- "All verified road-blocking evidence in Manipur"

### 4. Situational Reports

Auto-generated PDF situation reports for incident commanders - evidence log, trust-score distribution, flagged items.

### 5. Geospatial Evidence View

Interactive map (Folium) with color-coded evidence pins by trust level.

---

## Architecture

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │ Field Media  │────▶│ Cloudinary   │────▶│  FastAPI     │
    │  (upload)    │     │ (media layer)│     │  (backend)   │
    └──────────────┘     └──────────────┘     └──────┬───────┘
                                                      │
                            ┌─────────────────────────┼─────────────────────────┐
                            │                         │                         │
                            ▼                         ▼                         ▼
                    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
                    │    EXIF      │         │  Bayesian    │         │   Qdrant     │
                    │  Forensics   │         │  Truth Score │         │   Vector     │
                    │              │         │   Engine     │         │   Store      │
                    └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
                           │                        │                        │
                           ▼                        ▼                        ▼
                    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
                    │  Satellite   │         │ Perceptual   │         │  Streamlit   │
                    │ Cross-check  │         │    Hash      │         │  Dashboard   │
                    └──────────────┘         └──────────────┘         └──────────────┘

---

## Tech Stack

**Backend**

- FastAPI - async API framework
- Pydantic v2 - strict validation
- Uvicorn - ASGI server
- Loguru - structured logging

**Media and Forensics**

- Cloudinary - upload, AI tagging, storage
- Pillow + piexif - EXIF extraction
- ImageHash - perceptual duplicate detection

**Intelligence**

- NumPy + SciPy - Bayesian fusion
- Qdrant - semantic vector search
- httpx - satellite and weather APIs

**Frontend**

- Streamlit - dashboard framework
- Plotly - custom gauge and radar chart
- Folium + streamlit-folium - geospatial view

**Reports**

- ReportLab - PDF generation

---

## Quick Start

### 1. Clone and Install

    git clone https://github.com/ArpanC6/satyanet.git
    cd satyanet
    python -m venv venv

On Windows:

    venv\Scripts\activate.bat

On macOS / Linux:

    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

### 2. Configure Environment

    cp .env.example .env

Edit .env with your Cloudinary credentials (optional - backend works offline too):

    CLOUDINARY_CLOUD_NAME=your_cloud_name
    CLOUDINARY_API_KEY=your_api_key
    CLOUDINARY_API_SECRET=your_api_secret

### 3. Run Backend

    uvicorn backend.main:app

- Backend live at http://127.0.0.1:8000
- Swagger docs at http://127.0.0.1:8000/docs

### 4. Run Frontend (new terminal)

    streamlit run frontend/app.py

- Frontend live at http://localhost:8501

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/verify | Upload and verify field evidence |
| POST | /api/v1/search | Semantic search across evidence |
| GET | /api/v1/projects | List all projects with summary |
| GET | /api/v1/projects/{name} | Get single project summary |
| GET | /health | Health check |
| GET | /docs | Swagger UI |

### Example Request

    curl -X POST http://127.0.0.1:8000/api/v1/verify \
      -F "file=@field_photo.jpg" \
      -F "project=Siliguri Flood 2026" \
      -F "location_label=Siliguri, WB" \
      -F "claimed_date=2026-09-30" \
      -F "latitude=26.7271" \
      -F "longitude=88.3953"

### Example Response

    {
      "verification": {
        "trust_score": 50.5,
        "trust_level": "needs_review",
        "signals": [
          {"signal": "exif_integrity", "score": 0.7, "weight": 0.25},
          {"signal": "temporal_plausibility", "score": 0.5, "weight": 0.20},
          {"signal": "satellite_consistency", "score": 0.6, "weight": 0.25},
          {"signal": "duplicate_check", "score": 0.4, "weight": 0.20},
          {"signal": "image_quality", "score": 0.5, "weight": 0.10}
        ],
        "reasons": [
          "EXIF metadata present",
          "Timestamp ambiguous (±3 days)",
          "Weather partially consistent (cloudy)"
        ]
      }
    }

---

## Why Bayesian Uncertainty?

Most media-verification tools give you a label - "authentic" or "fake". We give you a label **plus a statistically grounded confidence measure** derived from Bayesian fusion of multiple weak signals.

This methodology is inspired by ensemble uncertainty quantification literature (Lakshminarayanan et al., 2017) applied to forensic media verification - the same techniques used in medical imaging and autonomous systems.

**Why this matters:**

- A single weak signal (e.g., EXIF missing) is not enough to call a photo fake
- Fusing 5 independent signals gives a robust posterior estimate
- Explanations per signal allow human-in-the-loop review
- Responders can make risk-calibrated decisions instead of binary guesses

---

## Project Structure

    satyanet/
    ├── backend/                       FastAPI backend
    │   ├── main.py                    App entry, middleware, routers
    │   ├── config.py                  Pydantic settings
    │   ├── models/
    │   │   ├── enums.py               TrustLevel, SignalType, SignalStatus
    │   │   └── schemas.py             Pydantic v2 request/response models
    │   ├── services/
    │   │   ├── exif_forensics.py      EXIF + GPS extraction
    │   │   ├── perceptual_hash.py     Duplicate detection
    │   │   ├── cloudinary_service.py  Cloudinary integration
    │   │   ├── satellite_crosscheck.py Weather cross-check
    │   │   ├── truth_score.py         Bayesian UQ engine (core)
    │   │   ├── vector_store.py        Qdrant integration
    │   │   └── report_generator.py    PDF report generation
    │   ├── routes/
    │   │   ├── verify.py              POST /verify
    │   │   ├── search.py              POST /search
    │   │   └── projects.py            GET /projects
    │   └── utils/
    │       ├── logger.py              Structured logging
    │       └── exceptions.py          Custom exception hierarchy
    ├── frontend/                      Streamlit dashboard
    │   ├── app.py                     Main entry
    │   ├── components/
    │   │   ├── theme.py               Light professional theme
    │   │   ├── truth_gauge.py         Custom Trust Score gauge
    │   │   └── signal_chart.py        Signal radar chart
    │   └── pages/
    │       ├── 1_Dashboard.py         Project overview
    │       ├── 2_Verify.py            Evidence upload + verification
    │       ├── 3_Map.py               Geospatial view
    │       └── 4_Reports.py           PDF report generation
    ├── data/
    │   ├── known_fakes.json           Known-fake hash database
    │   └── sample_evidence/           Sample field media
    ├── docs/
    │   ├── architecture.md            System architecture
    │   └── methodology.md             Bayesian UQ methodology
    ├── tests/
    │   ├── test_truth_score.py        Truth Score engine tests
    │   ├── test_exif.py               EXIF extraction tests
    │   └── test_cloudinary.py         Cloudinary integration tests
    ├── requirements.txt
    ├── LICENSE
    └── README.md

---

## Roadmap

- [x] Bayesian Truth Score engine (5-signal fusion)
- [x] Cloudinary media pipeline
- [x] Qdrant semantic search
- [x] PDF situation reports
- [x] Premium Streamlit dashboard
- [ ] Qdrant Edge integration (on-device verification)
- [ ] NASA FIRMS satellite fire / disaster data
- [ ] Multi-language field UI (Hindi, Bengali, Assamese)
- [ ] UN OCHA partnership
- [ ] Mobile app (React Native)

---

## Testing

Run the full test suite:

    pytest

Run a specific test file:

    pytest tests/test_truth_score.py -v

---

## Author

**Arpan Chakraborty**

- Research Intern, Jadavpur University - Bayesian Deep Learning and Uncertainty Quantification for Medical Imaging
- Cornell University SEAL Lab - Probabilistic Programming and Numerical Testing
- SciML Collaborator (Prof. Chris Rackauckas) - Bayesian Inference for SDEs
- Open Source Contributor - TuringLang, RxInfer, Jenkins
- National Hackathon Winner - Hyperspace Innovation, TECHNEST 2025 (Satellite Imagery)
- Google Routes API Feature Requests - 2 accepted (street lighting, air quality routing)

GitHub: https://github.com/ArpanC6
Email: chakrabortyarpan151@gmail.com

---

## License

MIT - see LICENSE for details.

---

**Built for Code Cubicle 6.0 - HackCulture**

*"Quantify uncertainty. Then decide."*