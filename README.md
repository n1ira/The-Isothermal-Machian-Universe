# The Isothermal Machian Universe
**Status:** ⚠️ **FRAMEWORK PROPOSED** (Under Review)
See [Scientific Status & Limitations](SCIENTIFIC_STATUS.md) for a critical assessment.

> "The universe is not expanding. Mass is evolving."

## 🔭 Project Overview
The **Isothermal Machian Universe (IMU)** is a unified scalar-tensor framework designed to explore whether "dark sector" phenomena (Dark Matter/Energy) can be explained by modified inertia and vacuum energy. While promising, it is a research agenda with significant open challenges.

### Key Findings
1.  **Structure Formation:**
    *   Our P3M N-body simulation (Experiment 8) reproduced CDM-like clustering on small scales ($n_{eff} \approx -2.54$).
    *   *Note:* This confirms the mechanism works in principle, but relies on effective parameters.

2.  **Galactic Rotation:**
    *   Flat rotation curves are modeled via an inertial mass gradient $m(r) \propto e^{-r/R}$.
    *   *Note:* Validated against SPARC data (NGC 6503), but requires screening to satisfy Solar System bounds.

3.  **Cosmic Expansion:**
    *   Redshift is modeled as shrinking atomic rulers ($m(t) \propto t^{-1}$) in a static background.
    *   *Result:* Simulation confirms observational equivalence with $\Lambda$CDM for geometric probes (SNIa).

4.  **Gravitational Lensing:**
    *   Non-minimal photon coupling $\lambda_\gamma \nabla \phi \cdot F^2$ reproduces the lensing signal.
    *   *Prediction:* A ~37% deficit in Shapiro time delays is predicted, serving as a falsifiable test.

---

## 🚀 Quick Start

### 1. Start the Backend (Physics Engine)
Runs the FastAPI server exposing the physics kernels.
```powershell
# Terminal 1 (Windows)
.\venv\Scripts\python.exe -m uvicorn lab.api:app --reload --port 8000
```
*   *Status Check:* Open [http://localhost:8000](http://localhost:8000) (Returns JSON status)
*   *API Docs:* [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Start the Frontend (Dashboard)
Runs the React/Vite application with TailwindCSS v4.
```bash
# Terminal 2
cd web
npm run dev
```
*   *Access App:* Open [http://localhost:5173](http://localhost:5173) (or port shown in terminal)

---

## 🛠️ Development Setup

### Prerequisites
*   Python 3.11+
*   Node.js 18+
*   CUDA Toolkit (Optional, for GPU acceleration)
*   LaTeX Distribution (MiKTeX/TeXLive) for paper compilation

### Installation
1.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install fastapi uvicorn scipy
    ```

2.  **Install Frontend Dependencies:**
    ```bash
    cd web
    npm install
    ```
    *   `src/api/` - Axios client for backend communication.
*   `papers/` - **Research Papers** (LaTeX)
    *   Automated PDF generation with `tools/build_papers.py`.
*   `data/` - **Observational Data**
    *   SPARC database files (e.g., `ngc6503.dat`).
