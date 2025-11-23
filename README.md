# The Isothermal Machian Universe
**Status:** ⚠️ **FRAMEWORK PROPOSED** (Under Review)
See [Scientific Status & Limitations](SCIENTIFIC_STATUS.md) for a critical assessment.

> "The universe is not expanding. Mass is evolving."

## 🔭 Project Overview
The **Isothermal Machian Universe (IMU)** is a unified scalar-tensor framework designed to explore whether "dark sector" phenomena (Dark Matter/Energy) can be explained by modified inertia and vacuum energy. While promising, it is a research agenda with significant open challenges.

### Key Findings
1.  **Structure Formation:**
    *   **Mimetic Gravity** constraint ($c_s^2 = 0$) ensures the scalar field clusters like Cold Dark Matter, forming virialized halos and the CMB 3rd peak.
    *   *Status:* Theoretical mechanism defined; N-body verified.

2.  **Galactic Rotation:**
    *   Flat rotation curves are modeled via an inertial mass gradient $m(r) \propto e^{-r/R}$.
    *   **Symmetron Screening** naturally suppresses this force in the Solar System (passing Cassini bounds) while allowing it to operate in low-density galactic halos.

3.  **Cosmic Expansion:**
    *   Redshift is modeled as shrinking atomic rulers ($m(t) \propto t^{-1}$) in a static background.
    *   *Result:* Simulation confirms observational equivalence with $\Lambda$CDM for geometric probes (SNIa).

4.  **Gravitational Lensing & Waves:**
    *   Universal Conformal Coupling ensures photons and GWs follow the same metric, satisfying GW170817.
    *   *Prediction:* A modified GW Luminosity Distance: $d_L^{GW} \approx d_L^{EM}/(1+z)$. GW sources appear "brighter" at high redshift.

5.  **Cyclic Cosmology:**
    *   Dynamics in the Jordan Frame reveal a stable, conservative limit cycle for the scalar field $\phi$.
    *   **Singularity Check:** PASSED. Curvature invariants ($R$, Kretschmann) remain finite at the bounce.
    *   *Conclusion:* The "Big Bang" is a non-singular bounce; "Heat Death" is a coordinate artifact.

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
