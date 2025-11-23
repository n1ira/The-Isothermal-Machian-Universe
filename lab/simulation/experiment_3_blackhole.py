"""
SIMULATION 3: Horizon Phase Transition
Goal: Visualize the "Cold Firewall" phase transition where time freezes at the horizon.
"""

import jax
import jax.numpy as jnp
from jax import jit
import matplotlib.pyplot as plt
import numpy as np

# 1. SETUP
Rs = 1.0  # Schwarzschild Radius
epsilon = 0.1 # The Machian scalar coupling constant
E = 1.0 # Energy per unit mass

# 2. DEFINE THE METRIC
@jit
def metric_g00(r):
    # Machian Paper 3 Eq 2:
    # g00 = (1 - Rs/r)^(1 + epsilon)
    val = 1.0 - Rs / r
    val = jnp.maximum(val, 1e-10) # Avoid singularity/negative
    return val**(1.0 + epsilon)

# 3. TRAJECTORY SOLVER
@jit
def derivatives(state, tau):
    """
    State = [t, r]
    Returns [dt/dtau, dr/dtau]
    """
    t, r = state
    g00 = metric_g00(r)
    
    # dt/dtau = E / g00
    dt_dtau = E / g00
    
    # dr/dtau = -sqrt(E^2 - g00)
    dr_dtau = -jnp.sqrt(jnp.maximum(E**2 - g00, 0.0))
    
    return jnp.array([dt_dtau, dr_dtau])

def run_simulation():
    print("Running Experiment 3: The 'Solid State' Event Horizon")
    print(f"Parameters: Rs={Rs}, epsilon={epsilon}")
    
    # Initial conditions
    r0 = 10.0 * Rs
    t0 = 0.0
    state = jnp.array([t0, r0])
    
    # Simulation loop
    dtau = 0.001 # Smaller step
    steps = 20000 # More steps
    
    tau_values = []
    t_values = []
    r_values = []
    
    current_tau = 0.0
    current_state = state
    
    print("Simulating infall...")
    
    for i in range(steps):
        tau_values.append(current_tau)
        t_values.append(float(current_state[0]))
        r_values.append(float(current_state[1]))
        
        # RK4 step
        k1 = derivatives(current_state, current_tau)
        k2 = derivatives(current_state + 0.5 * dtau * k1, current_tau + 0.5 * dtau)
        k3 = derivatives(current_state + 0.5 * dtau * k2, current_tau + 0.5 * dtau)
        k4 = derivatives(current_state + dtau * k3, current_tau + dtau)
        
        current_state = current_state + (dtau / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        current_tau += dtau
        
        r_curr = float(current_state[1])
        t_curr = float(current_state[0])
        
        # Stop if we are extremely close to Rs
        if r_curr < Rs * 1.00001:
            # We want to see divergence, so let it run until t is large
            if t_curr > 1000.0:
                print(f"Coordinate time diverged (>1000) at step {i}, r={r_curr:.6f}")
                break
            
            # Or if we get TOO close and g00 blows up numerically
            if r_curr < Rs * 1.0000001:
                print(f"Reached numerical limit at step {i}, r={r_curr:.8f}")
                break
                
    # Convert to numpy for plotting
    tau_arr = np.array(tau_values)
    t_arr = np.array(t_values)
    r_arr = np.array(r_values)
    
    # 5. VISUALIZATION
    plt.figure(figsize=(10, 6))
    
    plt.plot(t_arr, r_arr, label="Bob's View (Coordinate Time)", color='red', linestyle='--')
    plt.plot(tau_arr, r_arr, label="Alice's View (Proper Time)", color='cyan', linewidth=2)
    
    plt.axhline(y=Rs, color='k', linestyle=':', label="Event Horizon (Rs)")
    plt.xlabel("Time (t or tau)")
    plt.ylabel("Radius (r)")
    plt.title(f"Black Hole Infall: Phase Transition (epsilon={epsilon})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(Rs * 0.9, Rs * 5.0)
    
    output_file = "experiment_3_result.png"
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")
    
    # Verification
    final_r = float(current_state[1])
    final_t = float(current_state[0])
    final_tau = current_tau
    
    print(f"\nFinal State:")
    print(f"Radius: {final_r:.6f} Rs")
    print(f"Proper Time (Alice): {final_tau:.2f}")
    print(f"Coordinate Time (Bob): {final_t:.2e}")
    
    ratio = final_t / final_tau if final_tau > 0 else 0
    print(f"Time Dilation Ratio: {ratio:.2e}")
    
    if final_t > 1000 or ratio > 50.0:
        print("SUCCESS: Coordinate time is diverging relative to proper time. 'Holographic Freezing' confirmed.")
    else:
        print("WARNING: Time dilation effect is small. Check epsilon.")

if __name__ == "__main__":
    run_simulation()
