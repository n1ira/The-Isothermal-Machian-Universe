import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# === Jordan Frame (Static Universe) Simulation ===
# Physics:
# The universe is static (g_uv = eta_uv).
# Dynamics driven by scalar field phi.
# Equation of Motion derived from Action:
# phi_ddot = (3 / 2*phi) * phi_dot^2 - (phi / 2*omega) * (V_prime + S_matter + S_em)

# Constants
OMEGA_BD = 1000.0  # Brans-Dicke parameter (High for GR limit, but let's see)
RHO_M0 = 1.0       # Matter density scale

# Potentials
# We assume the "Effective" potentials from the Einstein frame map to physical terms here.
# Vacuum: V ~ 1/phi^2
V0 = 10.0
# Thermal: V ~ phi (from T ~ m coupling)
C_THERM = 50.0
# EM Wall: V ~ ln(phi)
K_WALL = 50.0

def run_jordan_bounce():
    print("Initializing Jordan Frame (Static) Bounce Experiment...")
    
    # Initial Conditions
    # Start in the "Past" (Thermal Well)
    phi_init = 0.5
    phi_dot_init = 0.0
    
    y0 = [phi_init, phi_dot_init]
    
    t_span = (0, 100.0)
    
    print(f"Initial State: phi={phi_init}")
    
    sol = solve_ivp(derivatives, t_span, y0, method='LSODA', rtol=1e-8, max_step=0.05)
    
    phi = sol.y[0]
    phi_dot = sol.y[1]
    t = sol.t
    
    # Check for Cycle
    # Count zero crossings of phi_dot
    zero_crossings = np.where(np.diff(np.sign(phi_dot)))[0]
    print(f"Number of turning points: {len(zero_crossings)}")
    
    if len(zero_crossings) > 2:
        print("SUCCESS: Multiple bounces detected! The universe is cyclic.")
        is_cyclic = True
    else:
        print("Result: Evolution monotonic or single bounce.")
        is_cyclic = False
        
    # Save
    np.savez('jordan_bounce.npz', t=t, phi=phi, phi_dot=phi_dot)
    
    # Plot
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(t, phi, 'm-', linewidth=2)
    plt.ylabel('Scalar Field (phi)')
    plt.title('Jordan Frame Dynamics: The Cyclic Universe')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(phi, phi_dot, 'k-')
    plt.xlabel('phi')
    plt.ylabel('phi_dot')
    plt.title('Phase Space')
    plt.grid(True)
    
    plt.savefig('jordan_bounce_result.png')
    print("Plot saved to jordan_bounce_result.png")

def derivatives(t, y):
    phi, phi_dot = y
    
    # Safety for log/div
    if phi < 1e-3: phi = 1e-3
    
    # 1. Potentials & Forces (dV/dphi)
    
    # Vacuum: V = V0 / phi^2
    # dV = -2 V0 / phi^3
    dV_vac = -2 * V0 / (phi**3)
    
    # Thermal: V = 0.5 C phi (Linear restoring force)
    dV_therm = 0.5 * C_THERM
    
    # EM Wall: V = K ln(phi)
    dV_em = K_WALL / phi
    
    V_prime = dV_vac + dV_therm + dV_em
    
    # 2. Matter Source
    # S_m = rho_m * d(ln m)/dphi
    # m ~ phi^-0.5 => ln m ~ -0.5 ln phi => dln m/dphi = -0.5/phi
    # rho_m = RHO_M0 * phi^-0.5
    rho_m = RHO_M0 / np.sqrt(phi)
    S_matter = rho_m * (-0.5 / phi)
    
    # 3. EOM
    # phi_ddot = (3 / 2*phi) * phi_dot^2 - (phi / 2*omega) * (Total_Force)
    
    Total_Force = V_prime + S_matter
    
    # Damping Term from Action (Geometric)
    # The 3/2phi term acts like "anti-friction" if phi grows?
    geometric_term = (3.0 / (2.0 * phi)) * phi_dot**2
    
    force_term = - (phi / (2.0 * OMEGA_BD)) * Total_Force
    
    d_phi = phi_dot
    d_phi_dot = geometric_term + force_term
    
    return [d_phi, d_phi_dot]

if __name__ == "__main__":
    run_jordan_bounce()
