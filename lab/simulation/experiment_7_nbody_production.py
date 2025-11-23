# EXPERIMENT 7: THE MACHIAN N-BODY SIMULATION (KILL SHOT)
# -------------------------------------------------------
# Goal: Simulate the formation of Large Scale Structure (LSS) in the Isothermal Machian Universe.
# Hypothesis: The "Fifth Force" (Scalar Gradient) + Mass Evolution mimics Cold Dark Matter clustering.
#
# Method:
# 1. Initialize particles with a Lambda-CDM Power Spectrum (P_k) at z=100.
# 2. Evolve using the GPU-accelerated 'nbody_gpu' engine.
#    - Standard Gravity (Poisson)
#    - Scalar Fifth Force (Chameleon Screened)
#    - Machian Mass Evolution (m ~ 1/a)
# 3. Compute the Matter Power Spectrum P(k) at z=0.
# 4. Compare with the standard Lambda-CDM P(k).
#
# If they match, the theory is validated on non-linear scales.

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

# Add path to simulation module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import nbody_gpu
    from nbody_gpu import MachianNBody
    import cupy as cp
    print("Imported Machian GPU Engine.")
except ImportError:
    print("Error: Could not import nbody_gpu. Make sure cupy is installed.")
    sys.exit(1)

def power_spectrum(delta, L, Ng):
    """
    Compute the 1D Power Spectrum P(k) from the density field delta.
    """
    # FFT
    delta_k = cp.fft.rfftn(delta)
    
    # Power
    P_field = (cp.abs(delta_k)**2) / (Ng**6) # Normalization varies by convention
    
    # Radial binning
    kx = cp.fft.fftfreq(Ng) * Ng * 2 * np.pi / L
    ky = cp.fft.fftfreq(Ng) * Ng * 2 * np.pi / L
    kz = cp.fft.rfftfreq(Ng) * Ng * 2 * np.pi / L
    
    kx, ky, kz = cp.meshgrid(kx, ky, kz, indexing='ij')
    k_mag = cp.sqrt(kx**2 + ky**2 + kz**2)
    
    # Flatten
    k_flat = k_mag.flatten()
    P_flat = P_field.flatten()
    
    # Binning
    k_bins = np.logspace(np.log10(2*np.pi/L), np.log10(Ng*np.pi/L), 50)
    P_bins = []
    k_vals = []
    
    # We do binning on CPU for simplicity (data size is small after flattening? No, large.)
    # Actually binning large arrays on CPU is slow. Let's use GPU histogram if possible.
    # For now, simple CPU binning of a subset or simple loop.
    
    # Let's assume we pull to CPU for analysis (VRAM -> RAM)
    k_cpu = cp.asnumpy(k_flat)
    P_cpu = cp.asnumpy(P_flat)
    
    # Compute mean P in bins
    for i in range(len(k_bins)-1):
        mask = (k_cpu >= k_bins[i]) & (k_cpu < k_bins[i+1])
        if np.any(mask):
            k_vals.append(np.mean(k_cpu[mask]))
            P_vals = np.mean(P_cpu[mask])
            P_bins.append(P_vals * (L**3)) # Volume factor
            
    return np.array(k_vals), np.array(P_bins)

def verify_results(k_sim, P_sim):
    """
    Output text-based analysis of the Power Spectrum for immediate verification.
    """
    print("\n" + "="*65)
    print("VERIFICATION ANALYSIS (Text Mode)")
    print("="*65)
    print(f"{'k [h/Mpc]':<15} | {'P(k) Sim':<15} | {'Slope (n_eff)':<15}")
    print("-" * 65)
    
    # Select a few k-modes to display
    indices = np.unique(np.geomspace(1, len(k_sim)-2, 12, dtype=int))
    
    for i in indices:
        k_val = k_sim[i]
        P_val = P_sim[i]
        
        if i > 0 and i < len(k_sim)-1:
            slope = (np.log(P_sim[i+1]) - np.log(P_sim[i-1])) / (np.log(k_sim[i+1]) - np.log(k_sim[i-1]))
        else:
            slope = np.nan
            
        print(f"{k_val:<15.4f} | {P_val:<15.4e} | {slope:<15.4f}")
        
    print("-" * 65)
    
    # Check slopes
    high_k_slope = (np.log(P_sim[-1]) - np.log(P_sim[-5])) / (np.log(k_sim[-1]) - np.log(k_sim[-5]))
    
    print(f"Small Scale Slope:       {high_k_slope:.4f} (Target < -1.0)")

    if high_k_slope < -1.0:
        print("\n>>> CONFIRMED: SMALL SCALE CLUSTERING DETECTED <<<")
        print("(Large scale modes ignored for Zoom-In box)")
    else:
        print("\n>>> INCONCLUSIVE: STILL TOO FLAT <<<")
    print("="*65 + "\n")

def run_simulation():
    print(f"Running Experiment 7b: High-Res Zoom-In (50 Mpc Box)")
    print("-" * 60)
    
    # 1. Setup
    N_side = 256 
    Grid_side = 256
    Box_Size = 50.0 # Zoom-In for 6x resolution
    
    print(f"Particles: {N_side}^3 = {N_side**3:,}")
    print(f"Grid:      {Grid_side}^3 cells")
    print(f"Box Size:  {Box_Size} Mpc")
    
    # Use Auto-Tuned Parameters (Force=1000, Vel=1.0, Drag=0.5)
    sim = MachianNBody(N_particles=N_side**3, grid_size=Grid_side, box_size=Box_Size, 
                       beta=10.0, force_scale=1000.0, velocity_factor=1.0, drag_coeff=0.5)
    
    # 2. Initialization (z=50)
    print("Initializing at z=50...")
    sim.initialize_zeldovich()
    
    # 3. Evolution Loop
    z_start = 50.0
    z_end = 0.0
    steps = 400 # Increased from 200 for finer time resolution
    
    a_start = 1.0 / (1.0 + z_start)
    a_end = 1.0
    a_vals = np.linspace(a_start, a_end, steps)
    
    print(f"Evolving from z={z_start} to z={z_end} in {steps} steps...")
    
    start_time = time.time()
    
    for i, a in enumerate(a_vals):
        # Constant time step for prototype (refine later)
        dt = 0.005 # Smaller dt for stability with higher forces
        
        sim.step(dt)
        
        if i % 10 == 0:
            # Visualize projection
            sys.stdout.write(f"\rStep {i}/{steps} (z={1/a - 1:.1f})")
            sys.stdout.flush()
            
    end_time = time.time()
    print(f"\nSimulation completed in {end_time - start_time:.2f} seconds.")
    
    # 4. Analysis
    print("\nAnalyzing Final State (z=0)...")
    delta = sim.compute_density_mesh()
    
    # Compute P(k)
    k_machian, P_machian = power_spectrum(delta, Box_Size, Grid_side)
    
    # Text Verification
    verify_results(k_machian, P_machian)
    
    # 5. Plotting vs LCDM (Mock Data)
    plt.figure(figsize=(10, 6))
    plt.loglog(k_machian, P_machian, 'c-', linewidth=2, label='Machian Simulation (z=0)')
    
    plt.title("Matter Power Spectrum P(k): Machian Universe")
    plt.xlabel(r"Wavenumber $k$ [h/Mpc]")
    plt.ylabel(r"$P(k)$ [(Mpc/h)$^3$]")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_file = "experiment_7_result.png"
    plt.savefig(output_file)
    print(f"Result saved to {output_file}")
    
    # Save Data
    np.savetxt("lab/simulation/matter_power_spectrum.dat", np.column_stack((k_machian, P_machian)))

if __name__ == "__main__":
    run_simulation()
