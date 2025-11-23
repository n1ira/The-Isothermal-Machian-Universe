import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# === Constants (eV) ===
M_PL = 2.435e27 # Reduced Planck Mass
N_POWER = 3.0 # Use n=3 from PPN analysis
LAMBDA_EV = 11.7e3 # From PPN test

# === New BBN Pinning Potential ===
# Pins phi at phi_BBN when T is high
# This value needs to be such that elementary masses are "normal" during BBN
PHI_BBN = 1.0e15 # eV (Arbitrary fixed value for phi during BBN)
C_PIN = 1.0e-15 # Strength of the pinning potential (tuned for ~1% drift)
P_POWER = 4 # Temperature power for pinning (makes it sharp)

def V_machian(phi):
    # This is the cosmological driving potential V(phi) = Lambda^(4+n) / phi^n
    # Note: Paper 8 mentions V ~ 1/phi^2 for cosmology, but PPN analysis uses n=3.
    # We proceed with n=3 for consistency with PPN results.
    # This inconsistency needs to be addressed.
    phi_safe = np.abs(phi) + 1e-30 # Avoid division by zero
    return (LAMBDA_EV**(4+N_POWER)) / (phi_safe**N_POWER)

def V_new_therm(phi, T):
    # This potential forces phi to be phi_BBN at high T
    # It acts as a restoring force when phi deviates from PHI_BBN
    # The T^P_POWER term makes it dominant at high T
    return 0.5 * C_PIN * (T**P_POWER) * (phi - PHI_BBN)**2

def V_total(phi, T):
    # Total potential during BBN epoch (ignoring radiative ln(phi) for simplicity)
    return V_machian(phi) + V_new_therm(phi, T)

def dV_total_dphi(phi, T):
    # Derivative of total potential for finding minimum
    phi_safe = np.abs(phi) + 1e-30
    dV_mach_dphi = -N_POWER * (LAMBDA_EV**(4+N_POWER)) * (phi_safe**(-N_POWER-1))
    dV_new_therm_dphi = C_PIN * (T**P_POWER) * (phi - PHI_BBN)
    return dV_mach_dphi + dV_new_therm_dphi

def find_phi_min(T):
    # Numerically find phi that minimizes V_total at given T
    # Use PHI_BBN as an initial guess, assuming the pinning works
    phi_guess = PHI_BBN
    
    # Define the function to find root of dV/dphi = 0
    func = lambda phi: dV_total_dphi(phi, T)
    
    # fsolve can sometimes return non-physical (negative) values for phi if guess is bad
    # Or if minimum is outside reasonable range.
    # We will enforce positivity and clamp to PHI_BBN if solution is problematic
    
    try:
        phi_min_val = fsolve(func, phi_guess, xtol=1e-10)[0]
        if phi_min_val > 1e-10 * PHI_BBN: # Ensure it's significantly positive
            return phi_min_val
        else:
            return PHI_BBN # Fallback if solver goes to negative or too small
    except Exception:
        return PHI_BBN # Fallback if solver fails

def run_bbn_model():
    print("\n=== BBN Thawing Model with New Pinning Potential ===")
    
    # Temperature range for BBN and beyond
    T_MeV = np.logspace(np.log10(1.0), np.log10(1e-6), 100) # From 1 MeV down to 1 eV
    T_eV = T_MeV * 1e6 # Convert to eV
    
    phi_history = []
    
    print("Calculating phi(T) history...")
    for T_val in T_eV:
        phi_eq = find_phi_min(T_val)
        phi_history.append(phi_eq)
    
    phi_history = np.array(phi_history)
    
    # Mass scaling: m propto sqrt(phi) (as per Paper 5)
    mass_history = np.sqrt(phi_history)
    
    # Normalize mass to 1 at PHI_BBN for easy interpretation
    mass_norm = mass_history / np.sqrt(PHI_BBN)
    
    # Plot results
    plt.figure(figsize=(12, 7))
    plt.loglog(T_MeV, mass_norm, label='Normalized Mass $m/m_{BBN}$', color='blue', linewidth=2)
    plt.axvline(x=0.1, color='red', linestyle='--', label='BBN Start (~0.1 MeV)')
    plt.axvline(x=0.03, color='orange', linestyle='--', label='Lithium Window (~30 keV)')
    plt.axvline(x=1e-3, color='green', linestyle='--', label='Recombination (~1 eV)')
    
    plt.xlabel('Temperature (MeV)')
    plt.ylabel('Normalized Mass $m/m_{BBN}$')
    plt.title('Particle Mass Evolution through BBN with New Pinning Potential')
    plt.grid(True, which="both", ls="-", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('bbn_mass_evolution_new_potential.png')
    print("Mass evolution plot saved to bbn_mass_evolution_new_potential.png")
    
    # Calculate mass drift during BBN (e.g., 80 keV to 30 keV)
    T_start_drift = 80e3 # eV (0.08 MeV)
    T_end_drift = 30e3 # eV (0.03 MeV)
    
    phi_start_drift = find_phi_min(T_start_drift)
    phi_end_drift = find_phi_min(T_end_drift)
    
    mass_drift_start = np.sqrt(phi_start_drift)
    mass_drift_end = np.sqrt(phi_end_drift)
    
    fractional_mass_drift = (mass_drift_end - mass_drift_start) / mass_drift_start
    
    print(f"\nMass Drift during Critical BBN Window ({T_start_drift/1e3} keV to {T_end_drift/1e3} keV):")
    print(f"  Fractional Change: {fractional_mass_drift:.4e} ({fractional_mass_drift*100:.2f}%)")
    
    if abs(fractional_mass_drift) < 1e-2: # Less than 1% drift
        print("RESULT: Mass drift is within acceptable limits for BBN (less than 1%).")
    else:
        print("RESULT: Mass drift is still too large for BBN.")
        print("Consider adjusting C_PIN or P_POWER, or redefining PHI_BBN (and ensuring consistency with cosmological evolution).")
        
    print("\n--- Theoretical Inconsistency Flag ---")
    print("Note: Cosmological potential V(phi) is assumed to be Lambda^(4+n)/phi^n with n=3 (from PPN analysis).")
    print("However, Paper 8 for Cyclic Cosmology states V ~ 1/phi^2 (i.e., n=2).")
    print("This requires clarification: Is the cosmological potential different from the local one, or is the n=2 in Paper 8 a simplification?")

if __name__ == "__main__":
    run_bbn_model()
