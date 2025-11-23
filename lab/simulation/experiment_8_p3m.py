# EXPERIMENT 8: P3M VALIDATION (High Resolution)
# -------------------------------------------------------
# Goal: Verify if P3M (Particle-Particle Particle-Mesh) fixes the small-scale clustering.
# Method: Run Machian N-Body with Short-Range Force correction.

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

# Add path to simulation module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import nbody_p3m
    from nbody_p3m import MachianP3M
    import cupy as cp
    print("Imported Machian P3M Engine.")
except ImportError:
    print("Error: Could not import nbody_p3m. Make sure cupy is installed.")
    sys.exit(1)

def power_spectrum(delta, L, Ng):
    """
    Compute the 1D Power Spectrum P(k) from the density field delta.
    """
    # FFT
    delta_k = cp.fft.rfftn(delta)
    
    # Power
    P_field = (cp.abs(delta_k)**2) / (Ng**6) 
    
    # Radial binning
    kx = cp.fft.fftfreq(Ng) * Ng * 2 * np.pi / L
    ky = cp.fft.fftfreq(Ng) * Ng * 2 * np.pi / L
    kz = cp.fft.rfftfreq(Ng) * Ng * 2 * np.pi / L
    
    kx, ky, kz = cp.meshgrid(kx, ky, kz, indexing='ij')
    k_mag = cp.sqrt(kx**2 + ky**2 + kz**2)
    
    # Flatten
    k_flat = k_mag.flatten()
    P_flat = P_field.flatten()
    
    # Binning (Move to CPU)
    k_cpu = cp.asnumpy(k_flat)
    P_cpu = cp.asnumpy(P_flat)
    
    k_bins = np.logspace(np.log10(2*np.pi/L), np.log10(Ng*np.pi/L), 50)
    P_bins = []
    k_vals = []
    
    for i in range(len(k_bins)-1):
        mask = (k_cpu >= k_bins[i]) & (k_cpu < k_bins[i+1])
        if np.any(mask):
            k_vals.append(np.mean(k_cpu[mask]))
            P_vals = np.mean(P_cpu[mask])
            P_bins.append(P_vals * (L**3))
            
    return np.array(k_vals), np.array(P_bins)

def verify_results(k_sim, P_sim):
    print("\n" + "="*65)
    print("VERIFICATION ANALYSIS (P3M Check)")
    print("="*65)
    print(f"{ 'k [h/Mpc]':<15} | { 'P(k) Sim':<15} | { 'Slope (n_eff)':<15}")
    print("-" * 65)
    
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
    
    # Check High-k Slope (Small Scales)
    high_k_slope = (np.log(P_sim[-1]) - np.log(P_sim[-5])) / (np.log(k_sim[-1]) - np.log(k_sim[-5]))
    print(f"Small Scale Slope:       {high_k_slope:.4f} (Target < -1.0)")

    if high_k_slope < -1.0:
        print("\n>>> SUCCESS: P3M RESTORED CLUSTERING <<<")
    else:
        print("\n>>> WARNING: STILL TOO FLAT (Check Force Tuning) <<<")
    print("="*65 + "\n")

def run_simulation():
    print(f"Running Experiment 8: P3M Test (High Res)")
    print("-" * 60)
    
    N_side = 64
    Grid_side = 128
    Box_Size = 50.0 
    
    print(f"Particles: {N_side}^3")
    print(f"Grid:      {Grid_side}^3")
    
    # Tuned Parameters from Exp 7 + Drag
    sim = MachianP3M(N_particles=N_side**3, grid_size=Grid_side, box_size=Box_Size, 
                     beta=10.0, force_scale=50.0, drag_coeff=0.5)
    
    sim.initialize_zeldovich()
    
    # Evolution Loop
    z_start = 50.0
    z_end = 0.0
    steps = 400
    a_vals = np.linspace(1.0/(1.0+z_start), 1.0, steps)
    
    print(f"Evolving from z={z_start} to z={z_end} ({steps} steps)...")
    
    t0 = time.time()
    for i, a in enumerate(a_vals):
        z = 1.0/a - 1.0
        
        # Verbose for first 10 steps, then every 20
        verbose = (i < 10) or (i % 20 == 0)
        
        if verbose:
            cp.cuda.Device().synchronize()
            elapsed = time.time() - t0
            if i > 0:
                avg_per_step = elapsed / i
                remaining = (steps - i) * avg_per_step
                eta_str = f"{remaining/60:.1f}m"
            else:
                eta_str = "?"
            
            # Check stability
            max_v = float(cp.max(cp.sqrt(sim.vel_x**2 + sim.vel_y**2 + sim.vel_z**2)))
            print(f"\nStep {i}/{steps} (z={z:.1f}) [Elapsed: {elapsed:.1f}s, ETA: {eta_str}, Max V: {max_v:.1f}]:")
        
        sim.step(0.001, verbose=verbose) 
            
    cp.cuda.Device().synchronize()
    print(f"\nDone in {time.time()-t0:.2f}s")
    
    # Analysis
    delta = sim.compute_density_mesh()
    k, P = power_spectrum(delta, Box_Size, Grid_side)
    
    verify_results(k, P)
    
    # Save Data
    header = "k [h/Mpc]    P(k) [(Mpc/h)^3]"
    np.savetxt("lab/simulation/p3m_power_spectrum.dat", np.column_stack((k, P)), header=header)
    print("Saved lab/simulation/p3m_power_spectrum.dat")
    
    # Save Plot
    plt.figure()
    plt.loglog(k, P, label='Machian P3M')
    plt.title("P3M Power Spectrum")
    plt.xlabel("k [h/Mpc]")
    plt.ylabel("P(k)")
    plt.legend()
    plt.savefig("experiment_8_result.png")
    print("Saved experiment_8_result.png")

if __name__ == "__main__":
    run_simulation()
