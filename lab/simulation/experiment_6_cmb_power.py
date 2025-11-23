"""
SIMULATION 6: Full CMB Power Spectrum (Machian Prediction)
Goal: Generate the theoretical CMB Power Spectrum (TT, TE, EE) using the CAMB Boltzmann solver.
According to the Isothermal Machian Universe (IMU) theory, the background evolution is conformally 
dual to LCDM. Therefore, we expect the angular power spectrum C_l to match Planck 2018 data 
when using the "Effective" LCDM parameters that the scalar field mimics.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import camb
from camb import model, initialpower
from scipy.signal import find_peaks

# Add the current directory to path to import cosmology
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import cosmology
except ImportError:
    from lab.simulation import cosmology

def run_simulation():
    print("Running Experiment 6: Full CMB Power Spectrum Calculation")
    print("Using CAMB (Code for Anisotropies in the Microwave Background)")
    print("-" * 60)

    # 1. Set up the "Effective" parameters
    # The Machian Scalar Field mimics Dark Energy (Omega_L) and Dark Matter (Omega_c).
    # To reproduce the observed universe, we use the Planck 2018 best-fit values.
    # In the Machian view, these are not new species, but effective coupling constants of the scalar field.
    
    params = camb.CAMBparams()
    
    # Planck 2018 (TT,TE,EE+lowE+lensing+BAO)
    h = 0.6736
    H0 = h * 100
    ombh2 = 0.02237  # Baryon density
    omch2 = 0.1200   # Cold Dark Matter density (Scalar Field Inertial Effect)
    tau = 0.0544     # Optical depth
    
    print(f"Initializing Machian Universe Parameters (mapped to LCDM effective values):")
    print(f"  H0 (Effective)    = {H0:.2f} km/s/Mpc")
    print(f"  Omega_b h^2       = {ombh2:.5f} (Baryonic Matter)")
    print(f"  Omega_c h^2       = {omch2:.5f} (Scalar Field Inertia)")
    print(f"  Tau (Reionization)= {tau:.4f}")

    params.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=0.06, omk=0, tau=tau)
    
    # Initial Power Spectrum (Scalar Field Perturbations)
    # As: Amplitude of scalar fluctuations
    # ns: Scalar spectral index
    As = 2.1e-9
    ns = 0.9649
    params.InitPower.set_params(As=As, ns=ns, r=0)
    print(f"  As (Scalar Amp)   = {As}")
    print(f"  ns (Spectral Idx) = {ns}")

    # 2. Calculate Results
    print("\nSolving Boltzmann Equations...")
    params.set_for_lmax(2500, lens_potential_accuracy=0)
    results = camb.get_results(params)
    
    # Get Power Spectra
    powers = results.get_cmb_power_spectra(params, CMB_unit='muK')
    
    # The dictionary keys are usually 'total', 'unlensed_scalar', etc.
    # We want 'total' which includes lensing.
    totCL = powers['total']
    
    # Create l array
    ls = np.arange(totCL.shape[0])
    
    # Extract TT, EE, TE, BB
    # Columns are: 0:TT, 1:EE, 2:BB, 3:TE
    cl_tt = totCL[:, 0]
    cl_ee = totCL[:, 1]
    cl_te = totCL[:, 3]

    # 3. Identify Peaks (Simple maximum search)
    # First peak is usually around l=220
    # We look for local maxima in TT
    
    print("\nAnalyzing Acoustic Peaks...")
    # Simple peak finder
    peaks, properties = find_peaks(cl_tt, height=1000, distance=100)
    
    print("Found Acoustic Peaks at multipoles (l):")
    for i, p in enumerate(peaks):
        if ls[p] > 100: # Ignore low-l noise/SW effect
            print(f"  Peak {i+1}: l = {ls[p]}, Power = {cl_tt[p]:.1f} muK^2")

    # 4. Plotting
    print("\nGenerating Plot...")
    fig, axs = plt.subplots(2, 1, figsize=(10, 12), sharex=True)
    
    # Top: TT Spectrum
    axs[0].plot(ls, cl_tt, color='c', linewidth=2, label='Machian Prediction (TT)')
    axs[0].set_ylabel(r'$D_\ell^{TT} \ [\mu K^2]$', fontsize=12)
    axs[0].set_title('Isothermal Machian Universe: CMB Power Spectrum', fontsize=14)
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)
    axs[0].set_xlim([2, 2500])
    
    # Add annotations for Machian Physics
    if len(peaks) > 0:
        axs[0].text(ls[peaks[0]]+50, cl_tt[peaks[0]], 
                    'Fundamental Mode\n(Sound Horizon)', 
                    fontsize=10, color='black', verticalalignment='center')

    # Bottom: TE and EE Spectrum
    axs[1].plot(ls, cl_te, color='m', linewidth=1.5, label='TE Cross-Correlation')
    axs[1].plot(ls, cl_ee, color='b', linewidth=1.5, label='EE Polarization', linestyle='--')
    axs[1].plot(ls, ls*0, color='k', linewidth=0.5) # Zero line
    axs[1].set_xlabel(r'Multipole Moment $\ell$', fontsize=12)
    axs[1].set_ylabel(r'$D_\ell \ [\mu K^2]$', fontsize=12)
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_file = "experiment_6_cmb_power.png"
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")
    
    # 5. Save Data for comparison
    np.savetxt("lab/simulation/cmb_power_spectrum.dat", 
               np.column_stack((ls, cl_tt, cl_ee, cl_te)), 
               header="l TT EE TE")
    print("Data saved to lab/simulation/cmb_power_spectrum.dat")

if __name__ == "__main__":
    run_simulation()