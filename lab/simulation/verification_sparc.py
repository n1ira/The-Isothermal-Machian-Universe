import numpy as np
import matplotlib.pyplot as plt
from simulation.galaxy_rotation import BaryonicMassGradient, USE_GPU

def mock_sparc_data():
    """
    Returns mock data representing a typical spiral galaxy (e.g., NGC 3198).
    Flat rotation curve at ~150 km/s from 5 kpc to 50 kpc.
    """
    r = np.linspace(2, 50, 20) # kpc
    # Flat curve with some noise
    v_obs = 150 + np.random.normal(0, 5, 20) 
    v_err = np.ones(20) * 10 # 10 km/s error bars
    return r, v_obs, v_err

def verify_model():
    print("Loading SPARC data (Mock)...")
    r_obs, v_obs, v_err = mock_sparc_data()
    
    print("Optimizing Beta Parameter...")
    
    best_beta = 0
    best_chi2 = float('inf')
    
    # Test Beta from 0.0 to 2.0 (since 5.0 blew up)
    for beta in np.linspace(0.0, 2.0, 21):
        sim = BaryonicMassGradient(m0=5.0e10, scale_length=15.0, beta=beta)
        v_model = sim.calculate_velocity_profile(r_obs)
        chi2 = np.sum(((v_obs - v_model) / v_err)**2)
        
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_beta = beta
            
    print(f"Best Beta found: {best_beta:.2f}")
    print(f"Best Chi-Squared: {best_chi2:.2f}")
    
    # Run with best beta
    sim = BaryonicMassGradient(m0=5.0e10, scale_length=15.0, beta=best_beta)
    v_model = sim.calculate_velocity_profile(r_obs)
    
    print(f"Model Predictions at 10 kpc: {sim.calculate_velocity_profile([10])[0]:.2f} km/s")
    print(f"Model Predictions at 50 kpc: {sim.calculate_velocity_profile([50])[0]:.2f} km/s")
    
    if best_chi2 < 1000.0: # Arbitrary threshold for "better"
        print("SUCCESS: Found a working Beta parameter.")
    else:
        print("WARNING: Still poor fit.")

if __name__ == "__main__":
    verify_model()
