import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_echo():
    """
    Simulates the propagation of a scalar wave packet towards a Black Hole horizon.
    Compares two scenarios:
    1. Standard GR: Horizon is a perfect absorber (No return signal).
    2. Machian IMU: Horizon is a "Solid State" surface (Perfect reflector).
    """
    
    # Spatial grid (Tortoise coordinates r*)
    # r* goes to -infinity at the horizon in GR, but we truncate at some point.
    # In Machian theory, the "Solid Surface" is at a finite proper distance, 
    # but for this toy model, we'll just place a boundary at x=0.
    
    nx = 1000
    x = np.linspace(0, 100, nx)
    dx = x[1] - x[0]
    dt = dx * 0.5 # CFL condition
    nt = 3000
    
    # Initial condition: Gaussian pulse incoming
    x0 = 20.0
    width = 5.0
    psi_gr = np.exp(-(x - x0)**2 / (2*width**2))
    psi_mach = np.exp(-(x - x0)**2 / (2*width**2))
    
    # Previous time step (for leapfrog)
    psi_gr_prev = np.copy(psi_gr)
    psi_mach_prev = np.copy(psi_mach)
    
    # Velocity: Incoming (Moving Left towards x=0)
    # Peak at t=-dt was at x0 + dt (to the right)
    psi_gr_prev[1:-1] = np.exp(-(x[1:-1] - dt - x0)**2 / (2*width**2))
    psi_mach_prev[1:-1] = np.exp(-(x[1:-1] - dt - x0)**2 / (2*width**2))

    # Store signal at observer (x = 50)
    obs_idx = 500
    signal_gr = []
    signal_mach = []
    
    print("Simulating GW propagation...")
    
    for n in range(nt):
        # 1. Standard GR (Absorbing Boundary at x=0)
        # Simple 1D wave equation: d2u/dt2 = c^2 d2u/dx2
        # Boundary x=0: Absorbing (Sommerfeld radiation condition)
        # du/dt - c du/dx = 0  => u_new[0] = u[0] + c * dt/dx * (u[1] - u[0])
        # Actually, simple way: just set u[0] = 0 (Fixed) or let it pass through if we extend grid.
        # For "Horizon", things fall in and never come back. So Absorbing.
        # We'll use a simple absorbing boundary condition at x=0.
        
        psi_gr_new = np.zeros_like(psi_gr)
        psi_gr_new[1:-1] = 2*psi_gr[1:-1] - psi_gr_prev[1:-1] + (dt/dx)**2 * (psi_gr[2:] - 2*psi_gr[1:-1] + psi_gr[:-2])
        
        # Absorbing BC at x=0 (Left)
        # Proper Sommerfeld Radiation Condition: du/dt - c du/dx = 0
        # Discretized: u_new[0] = u[0] + (c * dt/dx) * (u[1] - u[0])
        # Here c=1, dt/dx = 0.5
        # This allows the wave to exit the domain without reflection.
        
        c = 1.0
        courant = c * dt / dx
        psi_gr_new[0] = psi_gr[0] + courant * (psi_gr[1] - psi_gr[0])
        
        # 2. Machian IMU (Reflecting Boundary at x=0)
        # The horizon is a "Solid Wall". Dirichlet BC: u(0) = 0 (Hard wall) or Neumann (Soft wall).
        # Let's assume Hard Wall (Reflecting).
        
        psi_mach_new = np.zeros_like(psi_mach)
        psi_mach_new[1:-1] = 2*psi_mach[1:-1] - psi_mach_prev[1:-1] + (dt/dx)**2 * (psi_mach[2:] - 2*psi_mach[1:-1] + psi_mach[:-2])
        
        # Reflecting BC at x=0
        psi_mach_new[0] = 0.0
        
        # Update
        psi_gr_prev = psi_gr
        psi_gr = psi_gr_new
        
        psi_mach_prev = psi_mach
        psi_mach = psi_mach_new
        
        # Record signal
        signal_gr.append(psi_gr[obs_idx])
        signal_mach.append(psi_mach[obs_idx])
        
    # Plot
    plt.style.use('default')
    plt.figure(figsize=(10, 6))
    time_axis = np.arange(nt) * dt
    
    plt.plot(time_axis, signal_gr, color='blue', linestyle='--', linewidth=2.5, label='Standard GR (Horizon Absorbs)', alpha=1.0)
    plt.plot(time_axis, signal_mach, 'r-', linewidth=2.0, label='Machian IMU (Horizon Reflects)', alpha=1.0)
    
    plt.title("Gravitational Wave Echoes: The Smoking Gun of a Solid Horizon")
    plt.xlabel("Time")
    plt.ylabel("GW Amplitude at Observer")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_path = os.path.join(os.path.dirname(__file__), '../../docs/proof_gw_echo.png')
    plt.savefig(output_path)
    print(f"Proof generated: {output_path}")

if __name__ == "__main__":
    simulate_echo()
