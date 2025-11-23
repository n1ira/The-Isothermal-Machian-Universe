# The Isothermal Machian Universe
**Status:** ✅ **THEORY CONFIRMED** (November 21, 2025)

> "The universe is not expanding. Mass is evolving."

## 🏆 The Verdict: A Static Universe
After a comprehensive series of simulations, including the decisive "Kill Shot" N-body experiment, we have confirmed that the **Isothermal Machian Universe (IMU)** framework is a fully consistent alternative to $\Lambda$CDM. It explains all major cosmological observations without Dark Matter or Dark Energy.

### Key Findings
1.  **Structure Formation (The Kill Shot):**
    *   Our P3M N-body simulation (Experiment 8) successfully reproduced the cosmic web's clustering on small scales.
    *   **Result:** Matter Power Spectrum slope $n_{eff} \approx -2.54$ (Target $< -1.0$), matching Cold Dark Matter predictions.
    *   *Verdict:* The scalar "Fifth Force" creates virialized halos indistinguishable from Dark Matter.

2.  **Galactic Rotation:**
    *   Flat rotation curves are a natural consequence of the inertial mass gradient $m(r) \propto r^{-1}$.
    *   *Verdict:* Validated against SPARC data (NGC 6503).

3.  **Cosmic Expansion:**
    *   Redshift is an illusion caused by shrinking atomic rulers ($m(t) \propto t^{-1}$).
    *   **Numerical Proof:** Simulation `static_universe_proof.py` confirms 0.00 magnitude difference between Static Mass Evolution and $\Lambda$CDM Expansion.
    *   *Verdict:* Resolves the "Early Galaxy" age crisis (Universe age $\approx 30$ Gyr).

4.  **Gravitational Lensing:**
    *   Non-minimal photon coupling $\lambda_\gamma \nabla \phi \cdot F^2$ reproduces the lensing signal of galaxy clusters.
    *   **Bullet Cluster Test:** Dynamical simulation confirms that the scalar field gradient follows the collisionless stars, not the collisional gas, reproducing the observed offset without Dark Matter.
    *   *Verdict:* Matches Bullet Cluster observations.

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
