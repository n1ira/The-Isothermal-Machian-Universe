# The Isothermal Machian Universe
**Status:** 🟢 **Phase 10 Complete** (Manuscript Ready)

> *Exploring the hypothesis: The universe is not expanding. Mass is evolving.*

## 🔭 Project Overview
The **Isothermal Machian Universe (IMU)** is a proposed scalar-tensor framework that attempts to replace the "Dark Sector" (Dark Matter & Dark Energy) with a single evolving scalar field $\phi$. By exploring the possibility that the fundamental mass scale of the universe evolves ($m(t) \propto t^{-1}$) in a static background, the project aims to reproduce the observables of the standard $\Lambda$CDM model while addressing its tensions (Hubble Tension, Singularity, Information Paradox).

This repository contains the derivation, simulation, and statistical analysis of the theory, including a full Bayesian likelihood analysis against Planck 2018 data.

## 📄 Research Papers

### Main Papers

#### [Paper A: Core Theory](papers/source/paper_A_core_theory.tex)
*   **Focus:** Theoretical Foundation.
*   **Summary:** Proposes a unified scalar-tensor theory (IMU) combining Scale Invariance, Mimetic Gravity, and a Symmetron potential. Investigates if Dark Matter and Dark Energy can be modeled as manifestations of a single evolving scalar field, and examines the "Universal Conformal Coupling" for gravitational lensing.

#### [Paper B: Cosmology Tension](papers/source/paper_B_cosmology_tension.tex)
*   **Focus:** Hubble Tension Resolution.
*   **Summary:** Investigates the Hubble Tension ($H_0$ mismatch) through the lens of mass evolution. Suggests that a breakdown of Etherington's distance duality ($D_L \neq (1+z)^2 D_A$) could reconcile the CMB acoustic scale with local $H_0$ measurements ($H_0 \approx 71.3$ km/s/Mpc).

#### [Paper C: Forecasts](papers/source/paper_C_forecasts.tex)
*   **Focus:** Observational Predictions & Falsifiability.
*   **Summary:** Derives potential observational signatures for falsifying the theory, including specific predictions for Gravitational Wave Luminosity Distances (LISA/Einstein Telescope) and high-redshift halo abundances (JWST).

#### [Paper D: Speculative Extensions](papers/source/paper_D_speculative.tex)
*   **Focus:** Black Holes & Cyclic Cosmology.
*   **Summary:** Explores theoretical extensions regarding Black Hole horizons and Cyclic Cosmology. Discusses a "Solid State" horizon model (Fuzzball-like) and a potential mechanism for entropy reset at the cosmic bounce.

### Supplementary Papers
Detailed derivations and specific component analyses.

*   **[Paper 1: Galaxy Rotation](papers/source/paper_01_galaxy_rotation.tex)** - Analysis of SPARC data and rotation curves.
*   **[Paper 2: Cosmology](papers/source/paper_02_cosmology.tex)** - Initial cosmology derivation and distance duality.
*   **[Paper 3: Black Holes](papers/source/paper_03_black_holes.tex)** - Investigation of the Information Paradox and horizons.
*   **[Paper 4: Gravitational Lensing](papers/source/paper_04_lensing.tex)** - Lensing mass vs. dynamic mass.
*   **[Paper 5: Unified Field Theory](papers/source/paper_05_unified_field.tex)** - Lagrangian formulation (DHOST/Symmetron).
*   **[Paper 6: CMB Power Spectrum](papers/source/paper_06_cmb.tex)** - Acoustic peaks and scalar perturbations.
*   **[Paper 7: The Dilaton](papers/source/paper_07_dilaton.tex)** - Scale invariance and the Weak Equivalence Principle.
*   **[Paper 8: Cyclic Cosmology](papers/source/paper_08_cyclic.tex)** - Thermodynamics of the bounce.
*   **[Paper 9: Precision Constraints (MCMC)](papers/source/paper_09_mcmc.tex)** - Statistical validation and likelihood analysis.
*   **[Letter: The Kill Shot](papers/source/letter_kill_shot.tex)** - Summary of key predictive signatures.

---

## 🚀 Quick Start

### 1. Start the Backend (Physics Engine)
Runs the FastAPI server exposing the physics kernels.
```powershell
# Terminal 1 (Windows)
.\venv\Scripts\python.exe -m uvicorn lab.api:app --reload --port 8000
```
*   *Status Check:* Open [http://localhost:8000](http://localhost:8000)
*   *API Docs:* [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Start the Frontend (Dashboard)
Runs the React/Vite application.
```bash
# Terminal 2
cd web
npm run dev
```
*   *Access App:* Open [http://localhost:5173](http://localhost:5173)

---

## 🛠️ Development Setup

### Prerequisites
*   Python 3.11+
*   Node.js 18+
*   LaTeX (MiKTeX/TeXLive) for paper compilation

### Installation
1.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Install Frontend Dependencies:**
    ```bash
    cd web
    npm install
    ```

### Build Papers
To compile all research papers into PDFs:
```bash
python tools/build_papers.py
```