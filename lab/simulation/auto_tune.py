# AUTO-TUNER FOR MACHIAN N-BODY SIMULATION
# ------------------------------------------
# Goal: Automatically find the parameters (Force Scale, Velocity Factor, Beta)
#       that reproduce the observed Matter Power Spectrum features:
#       1. Large Scale Slope > 0 (Harrison-Zeldovich)
#       2. Small Scale Slope < -1 (Clustering/Virialization)

import numpy as np
import sys
import os
import time
import itertools

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
    delta_k = cp.fft.rfftn(delta)
    P_field = (cp.abs(delta_k)**2) / (Ng**6) 
    
    kx = cp.fft.fftfreq(Ng) * Ng * 2 * np.pi / L
    ky = cp.fft.fftfreq(Ng) * Ng * 2 * np.pi / L
    kz = cp.fft.rfftfreq(Ng) * Ng * 2 * np.pi / L
    
    kx, ky, kz = cp.meshgrid(kx, ky, kz, indexing='ij')
    k_mag = cp.sqrt(kx**2 + ky**2 + kz**2)
    
    k_flat = k_mag.flatten()
    P_flat = P_field.flatten()
    
    # Binning on CPU
    k_cpu = cp.asnumpy(k_flat)
    P_cpu = cp.asnumpy(P_flat)
    
    # Log bins
    k_bins = np.logspace(np.log10(2*np.pi/L), np.log10(Ng*np.pi/L), 20)
    P_vals_binned = []
    k_vals_binned = []
    
    for i in range(len(k_bins)-1):
        mask = (k_cpu >= k_bins[i]) & (k_cpu < k_bins[i+1])
        if np.any(mask):
            k_vals_binned.append(np.mean(k_cpu[mask]))
            P_vals_binned.append(np.mean(P_cpu[mask]) * (L**3))
            
    return np.array(k_vals_binned), np.array(P_vals_binned)

def analyze_result(k_sim, P_sim):
    """
    Analyze slopes and determine pass/fail.
    """
    if len(k_sim) < 5:
        return -99, -99, False
        
    # Low k slope (first few bins)
    low_k_slope = (np.log(P_sim[3]) - np.log(P_sim[0])) / (np.log(k_sim[3]) - np.log(k_sim[0]))
    
    # High k slope (last few bins)
    high_k_slope = (np.log(P_sim[-1]) - np.log(P_sim[-5])) / (np.log(k_sim[-1]) - np.log(k_sim[-5]))
    
    # Success Criteria:
    # 1. Low k > 0 (Harrison Zeldovich)
    # 2. High k < -1 (Clustering)
    # 3. Low k should not be crazy (> 4 is likely unstable/runaway)
    success = (low_k_slope > 0) and (low_k_slope < 4.0) and (high_k_slope < -1.0)
    return low_k_slope, high_k_slope, success

def run_tuning_grid():
    print("STARTING AUTO-TUNING GRID SEARCH (Phase 2: Stability)")
    print("=" * 60)
    
    # Parameter Grid
    # Previous runs showed instability with Force > 50k + Large Range.
    # We need to throttle back significantly.
    
    force_scales = [1000.0, 5000.0, 15000.0]
    velocity_factors = [1.0, 2.0, 5.0] 
    
    # Fixed Sim Parameters for Tuning (Fast but representative)
    N_side = 128 
    Grid_side = 128
    Box_Size = 200.0
    Steps = 200
    
    best_score = -999
    best_params = None
    
    combinations = list(itertools.product(force_scales, velocity_factors))
    print(f"Testing {len(combinations)} combinations...")
    
    for i, (f_scale, v_factor) in enumerate(combinations):
        print(f"\nRun {i+1}/{len(combinations)}: Force={f_scale}, Vel={v_factor}")
        
        try:
            sim = MachianNBody(N_particles=N_side**3, grid_size=Grid_side, box_size=Box_Size, 
                               beta=10.0, force_scale=f_scale, velocity_factor=v_factor)
            
            sim.initialize_zeldovich()
            
            # Run loop
            dt = 0.01 # Standard step
            for _ in range(Steps):
                sim.step(dt)
                
            # Analyze
            delta = sim.compute_density_mesh()
            k_sim, P_sim = power_spectrum(delta, Box_Size, Grid_side)
            low_slope, high_slope, success = analyze_result(k_sim, P_sim)
            
            print(f"  -> Low Slope: {low_slope:.4f} (Target > 0)")
            print(f"  -> High Slope: {high_slope:.4f} (Target < -1)")
            
            # Score: We want high_slope to be negative and large magnitude.
            # Heuristic score: 
            score = 0
            if low_slope > 0: score += 10
            score -= high_slope * 5 # If high_slope is -2, adds 10. If 0, adds 0.
            
            print(f"  -> Score: {score:.2f}")
            
            if score > best_score:
                best_score = score
                best_params = (f_scale, v_factor)
                print("  *** NEW BEST ***")
                
            if success:
                print("  >>> SUCCESS CRITERIA MET! <<<")
                # Could stop early, but let's finish grid to find "best" best?
                # Nah, finding one is good enough for now.
                break
                
        except Exception as e:
            print(f"  Run failed: {e}")
            
    print("\n" + "="*60)
    print("TUNING COMPLETE")
    print(f"Best Parameters Found: Force Scale = {best_params[0]}, Velocity Factor = {best_params[1]}")
    print("="*60)
    
    # Write optimal params to a file or instruction for the user
    with open("lab/simulation/optimal_params.txt", "w") as f:
        f.write(f"FORCE_SCALE={best_params[0]}\n")
        f.write(f"VELOCITY_FACTOR={best_params[1]}\n")

if __name__ == "__main__":
    run_tuning_grid()
