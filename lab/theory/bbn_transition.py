"""
BBN TRANSITION SIMULATION
-------------------------
Goal: Design a Scalar Potential V(phi, T) that pins the field (constant mass) during BBN (T > 0.1 MeV)
      and releases it (evolving mass) afterwards.

Model:
  V(phi, T) = V_Machian(phi) + V_Thermal(phi, T)
  
  V_Machian(phi) ~ phi^(-alpha)  (Runaway "Dark Energy" like)
  V_Thermal(phi, T) ~ T^4 * (phi/M_pl)^2  (Thermal Mass)

  Equation of Motion:
  phi'' + 3H phi' + dV/dphi = Coupling * rho_m

  We check if phi stays constant until t ~ 1 sec.
"""

import numpy as np
import matplotlib.pyplot as plt

def run_bbn_simulation():
    # Units: Planck units or MeV? Let's use MeV and seconds.
    # Constants
    M_pl = 2.4e18 * 1e3 # GeV -> 2.4e21 MeV. Let's scale everything to MeV.
    M_pl_MeV = 2.435e21
    
    # Time range: 1e-2 sec (High T) to 1e4 sec (Post BBN)
    t = np.logspace(-4, 5, 1000) # seconds
    
    # Temperature evolution in Radiation Era: T(t) approx 1 MeV / sqrt(t_sec)
    T_MeV = 1.0 / np.sqrt(t)
    
    # Scalar Field Parameters
    phi_0 = M_pl_MeV * 0.1 # Initial value (fraction of Planck mass)
    
    # The Machian Potential (Driving Force)
    # V ~ M^4 (M/phi)^alpha
    # We want this to drive phi evolution at late times.
    Lambda = 1e-3 * 1e-9 # eV scale ~ 1e-12 MeV ? No, Dark Energy scale is (2e-3 eV)^4
    # Let's just model the "Force" vs "Restoring Force"
    
    # Dynamics:
    # Inertia: phi''
    # Friction: 3H phi' ~ 3/(2t) phi'
    # Thermal Restoring Force: d/dphi (1/2 c T^2 phi^2) = c T^2 phi
    # Machian Driving Force: d/dphi (V_runaway) ~ -V'
    
    # We want Stability Condition: V''_thermal > V''_machian
    # c T^2 > V''_machian
    
    # Let's integrate numerically
    phi = np.zeros_like(t)
    phi[0] = phi_0
    phi_dot = 0.0
    
    # Tunable Coupling
    # Potential V ~ lambda * T^4 * (phi / M_pl)^2
    # Force dV/dphi ~ lambda * T^4 * phi / M_pl^2
    # M_pl in MeV is 2.4e21. T at 1 sec is 1 MeV.
    # Factor = T^4 / M_pl^2 = 1 / 10^42. Too small!
    # We need a non-minimal coupling that is strong.
    # Let's try V ~ T^2 * phi^2 (Effective Mass m^2 ~ T^2).
    # Force ~ T^2 * phi.
    # At t=1s, T=1 MeV. phi=10^20 MeV. Force ~ 1 * 10^20.
    # Friction ~ H * phi_dot.
    
    c_therm = 1.0e2 # Strong coupling
    
    # Machian Drive
    # Let's make it zero to test pure stability first
    F_drive = 0.0 
    
    # Initial kick perturbation to see if it restores
    phi_dot = 1.0e10 
    
    # Arrays to store mass deviation
    mass_deviation = []
    
    print(f"Running with T_init = {T_MeV[0]:.2e} MeV...")
    
    for i in range(len(t)-1):
        dt = t[i+1] - t[i]
        curr_t = t[i]
        curr_T = T_MeV[i]
        curr_phi = phi[i]
        
        # Hubble Friction
        H = 0.5 / curr_t
        
        # Forces
        # Thermal Mass: m_eff = c * T
        # F = - m_eff^2 * (phi - phi_0)
        F_thermal = - (c_therm * curr_T)**2 * (curr_phi - phi_0)
        
        # Total Force
        acc = F_thermal
        
        # Friction
        acc -= 3 * H * phi_dot
        
        # Update (Euler)
        phi_dot += acc * dt
        phi[i+1] = curr_phi + phi_dot * dt
        
        dm = (phi[i+1] - phi_0) / phi_0
        mass_deviation.append(dm)
        
        if i % 100 == 0:
            pass # Debug print if needed
        
    mass_deviation = np.array(mass_deviation)
    
    # Plot
    plt.figure(figsize=(10, 6))
    
    # Plot Temperature
    plt.subplot(2, 1, 1)
    plt.loglog(t, T_MeV, 'r-', label='Temperature (MeV)')
    plt.axhline(1.0, color='k', linestyle='--', label='BBN Threshold (1 MeV)')
    plt.axvline(1.0, color='k', linestyle='--', label='1 second')
    plt.ylabel('T [MeV]')
    plt.legend()
    plt.grid(True)
    
    # Plot Mass Deviation
    plt.subplot(2, 1, 2)
    plt.loglog(t[:-1], np.abs(mass_deviation) + 1e-20, 'b-', label='Mass Deviation |dm/m|')
    plt.axhline(0.01, color='g', linestyle=':', label='1% Tolerance')
    plt.axvline(1.0, color='k', linestyle='--')
    plt.xlabel('Time [sec]')
    plt.ylabel('Deviation')
    plt.legend()
    plt.grid(True)
    
    plt.suptitle("BBN Phase Transition: Mass Stability")
    plt.savefig("bbn_check.png")
    print("Simulation complete. Saved bbn_check.png")
    
    # Check at t=1 sec
    idx_1s = np.searchsorted(t, 1.0)
    dev_1s = mass_deviation[idx_1s]
    print(f"Mass Deviation at 1 sec (BBN): {dev_1s:.2e}")
    
    if abs(dev_1s) < 0.05:
        print(">> PASS: Mass is stable during BBN.")
    else:
        print(">> FAIL: Mass varies too much.")

if __name__ == "__main__":
    run_bbn_simulation()
