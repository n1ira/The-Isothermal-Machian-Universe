"""
Experiment 1: The Galaxy Rotation "Kill Shot"
Goal: Prove that a scalar field phi creates a flat rotation curve without Dark Matter.
"""

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.constants as const

# Constants
G = const.G.to(u.kpc**3 / (u.M_sun * u.s**2)).value
c = const.c.to(u.kpc / u.s).value
# M_sun = 1.989e30 kg
# kpc = 3.086e19 m

# Parameters for NGC 6503 (from prompt)
R_scale = 0.89 # kpc
beta = 0.98
M_galaxy = 5e9 # Solar masses (approximate for disk)
phi_0 = c**2 # Background potential (approx c^2)

# Tuning parameter to match observations (v ~ 200 km/s)
# v_flat^2 approx c^2 * beta * coupling / 2
# (200 km/s / 300,000 km/s)^2 approx 4e-7
# So coupling should be around 1e-6
coupling = 1.0e-6 

def scalar_field(r):
    """The Machian scalar field profile."""
    return phi_0 * (1 + r / R_scale)**beta

def machian_acceleration(r):
    """
    Calculates the Machian 'boost' acceleration.
    a = (c^2 / 2phi) * dphi/dr * coupling
    """
    phi = scalar_field(r)
    # Analytical derivative of phi:
    # dphi/dr = phi_0 * beta * (1 + r/R)^(beta-1) * (1/R)
    dphi_dr = phi_0 * beta * (1 + r / R_scale)**(beta - 1) / R_scale
    
    a_machian = (c**2 / (2 * phi)) * dphi_dr * coupling
    return a_machian

def newtonian_acceleration(r, M):
    """Standard Newtonian gravity."""
    return G * M / r**2

def total_velocity(r, M):
    """Calculates the circular velocity v = sqrt(r * a_total)."""
    a_newt = newtonian_acceleration(r, M)
    a_mach = machian_acceleration(r)
    return jnp.sqrt(r * (a_newt + a_mach))

def newtonian_velocity(r, M):
    return jnp.sqrt(r * newtonian_acceleration(r, M))

def run_simulation():
    print("Running Experiment 1: Galaxy Rotation 'Kill Shot'")
    print(f"Parameters: R={R_scale} kpc, beta={beta}")
    
    # Generate radii from 0.1 to 30 kpc
    radii = jnp.linspace(0.1, 30.0, 100)
    
    # Calculate velocities
    v_total = vmap(total_velocity, in_axes=(0, None))(radii, M_galaxy)
    v_newt = vmap(newtonian_velocity, in_axes=(0, None))(radii, M_galaxy)
    
    # Convert to km/s for plotting
    # 1 kpc/s = 3.086e16 km / s ... wait.
    # const.c is in m/s. 
    # Let's be careful with units.
    # G is in kpc^3 / (M_sun s^2)
    # c is in kpc / s
    # v is in kpc / s
    # To convert kpc/s to km/s:
    kpc_to_km = 3.08567758e16
    v_total_kms = v_total * kpc_to_km
    v_newt_kms = v_newt * kpc_to_km
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(radii, v_total_kms, label='Machian (Modified Inertia)', color='cyan', linewidth=2)
    plt.plot(radii, v_newt_kms, label='Newtonian (Baryons Only)', color='red', linestyle='--', linewidth=2)
    
    plt.title(f"Galaxy Rotation Curve (NGC 6503)\nR={R_scale} kpc, beta={beta}")
    plt.xlabel("Radius (kpc)")
    plt.ylabel("Velocity (km/s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linewidth=0.5)
    
    output_file = "experiment_1_result.png"
    plt.savefig(output_file)
    print(f"Simulation complete. Plot saved to {output_file}")
    
    # Verification check
    # Check if the curve is flat at large radii (relative slope)
    # We check the fractional change over the last 20% of the range
    v_last = v_total_kms[-1]
    v_prev = v_total_kms[-20]
    r_last = radii[-1]
    r_prev = radii[-20]
    
    slope = (v_last - v_prev) / (r_last - r_prev)
    relative_slope = slope / v_last # fractional change per kpc
    
    print(f"Velocity at {r_last:.1f} kpc: {v_last:.2e} km/s")
    print(f"Slope: {slope:.2f} km/s/kpc")
    print(f"Relative Slope: {relative_slope:.2e} /kpc")
    
    if abs(relative_slope) < 0.01: # Less than 1% change per kpc
        print("SUCCESS: Rotation curve is effectively flat.")
    else:
        print("WARNING: Rotation curve is not flat.")
        
    # Note on magnitude
    if v_last > 300000:
        print("NOTE: Velocity exceeds speed of light. This suggests the 'beta' parameter or coupling constant in the prompt implies a relativistic regime or requires scaling.")
    elif v_last > 1000:
        print("NOTE: Velocity is relativistic (>1000 km/s). The Machian boost is very strong with these parameters.")

if __name__ == "__main__":
    run_simulation()
