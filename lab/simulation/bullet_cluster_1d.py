"""
BULLET CLUSTER TEST: SCALAR FIELD DYNAMICS
------------------------------------------
Goal: Determine if the Machian Scalar Field naturally follows the collisionless stars (Lensing/DM signal) 
      or gets stuck with the collisional gas (Baryons).

Setup:
- 1D Collision of two clusters.
- Component 1: Stars (Collisionless, 10% mass).
- Component 2: Gas (Collisional, 90% mass).
- Scalar Field phi: Evolved via Wave Equation with Source = beta * rho_total.

Hypothesis:
- If phi is purely static/slaved to rho, it will track the Gas (Fail).
- If phi has significant inertia (wave dynamics) or screening effects, it might dissociate.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

class BulletSimulation:
    def __init__(self, Lx=4.0, Nx=512, dt=0.001):
        self.Lx = Lx
        self.Nx = Nx
        self.dx = Lx / Nx
        self.dt = dt
        self.x = np.linspace(-Lx/2, Lx/2, Nx)
        
        # Physics Constants (Arbitrary units for qualitative behavior)
        self.c = 1.0
        self.beta = 10.0 # Coupling strength
        self.m_phi = 1.0 # Effective mass of scalar (inverse range)
        
        # Cluster Parameters
        self.R_cluster = 0.2
        self.v_collision = 0.5 # relative to c (fast collision)
        self.ratio_gas_stars = 8.0
        
        # State
        self.phi = np.zeros(Nx)
        self.phi_old = np.zeros(Nx) # For Verlet integration
        self.phi_new = np.zeros(Nx)
        
        # Matter Positions (Centers)
        self.pos_stars_1 = -1.0
        self.pos_stars_2 = 1.0
        self.pos_gas_1 = -1.0
        self.pos_gas_2 = 1.0
        
        # Velocities
        self.vel_stars_1 = self.v_collision
        self.vel_stars_2 = -self.v_collision
        self.vel_gas_1 = self.v_collision
        self.vel_gas_2 = -self.v_collision
        
        # Gas Interaction State
        self.gas_shocked = False

    def gaussian(self, x, center, amp, width):
        return amp * np.exp(-0.5 * ((x - center) / width)**2)

    def get_density(self):
        # Stars (Collisionless) - maintain shape
        rho_s1 = self.gaussian(self.x, self.pos_stars_1, 1.0, self.R_cluster)
        rho_s2 = self.gaussian(self.x, self.pos_stars_2, 1.0, self.R_cluster)
        
        # Gas (Collisional)
        # If shocked, they merge or slow down. 
        # Simple model: If they overlap significantly, they stick at x=0.
        
        dist = abs(self.pos_gas_1 - self.pos_gas_2)
        
        # Check collision (simple distance threshold)
        if dist < self.R_cluster and not self.gas_shocked:
            self.gas_shocked = True
            self.vel_gas_1 *= 0.1 # Heavy braking
            self.vel_gas_2 *= 0.1
            
        rho_g1 = self.gaussian(self.x, self.pos_gas_1, self.ratio_gas_stars, self.R_cluster)
        rho_g2 = self.gaussian(self.x, self.pos_gas_2, self.ratio_gas_stars, self.R_cluster)
        
        return rho_s1 + rho_s2 + rho_g1 + rho_g2, (rho_s1 + rho_s2), (rho_g1 + rho_g2)

    def step(self):
        # 1. Move Matter
        self.pos_stars_1 += self.vel_stars_1 * self.dt
        self.pos_stars_2 += self.vel_stars_2 * self.dt
        self.pos_gas_1 += self.vel_gas_1 * self.dt
        self.pos_gas_2 += self.vel_gas_2 * self.dt
        
        # 2. Compute Source
        rho_total, rho_s, rho_g = self.get_density()
        
        # 3. Evolve Field (Wave Equation: dtt_phi - dxx_phi + m^2 phi = beta * rho)
        # Discrete Laplacian
        d2x_phi = (np.roll(self.phi, -1) - 2*self.phi + np.roll(self.phi, 1)) / (self.dx**2)
        
        # Verlet Integration
        # phi_new = 2*phi - phi_old + dt^2 * (dxx_phi - m^2 phi + beta * rho)
        
        source_term = self.beta * rho_total
        mass_term = (self.m_phi**2) * self.phi
        
        acc = self.c**2 * d2x_phi - mass_term + source_term
        
        # First step init
        if np.all(self.phi_old == 0):
            self.phi_old = self.phi.copy()
            
        self.phi_new = 2*self.phi - self.phi_old + (self.dt**2) * acc
        
        # Update
        self.phi_old = self.phi.copy()
        self.phi = self.phi_new.copy()
        
        return rho_s, rho_g

    def run(self, steps=2000):
        print(f"Simulating Collision... (Gas/Star Mass Ratio: {self.ratio_gas_stars})")
        
        history = []
        
        for i in range(steps):
            rho_s, rho_g = self.step()
            
            # Record state every 50 steps
            if i % 50 == 0:
                # Calculate Lensing Signal (Gradient Squared)
                # n - 1 ~ (grad phi)^2
                grad_phi = np.gradient(self.phi, self.dx)
                lensing = grad_phi**2
                
                history.append({
                    'time': i * self.dt,
                    'stars': rho_s,
                    'gas': rho_g,
                    'phi': self.phi,
                    'lensing': lensing
                })
                
        return history

def analyze_results(history):
    # Look at the final frame (post-collision)
    final = history[-1]
    
    x = np.linspace(-2, 2, len(final['stars']))
    
    # Normalize for plotting
    def norm(arr): return arr / np.max(arr) if np.max(arr) > 0 else arr
    
    stars = final['stars']
    gas = final['gas']
    lensing = final['lensing']
    
    # Find peaks (indices)
    idx_star_peak = np.argmax(stars) # One of the peaks
    idx_gas_peak = np.argmax(gas)    # Central peak
    idx_lens_peak = np.argmax(lensing)
    
    # Because stars split, there are two peaks. We want to see if lensing splits too.
    # Let's plot.
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, norm(stars), 'y--', label='Stars (Collisionless)')
    plt.plot(x, norm(gas), 'r-', alpha=0.5, label='Gas (Stuck)')
    plt.plot(x, norm(lensing), 'c-', linewidth=2, label='Lensing Signal (Scalar Gradient)')
    
    plt.title("Bullet Cluster Test: Scalar Field Dynamics")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("bullet_cluster_result.png")
    print("Saved bullet_cluster_result.png")
    
    # Verdict
    print("\n=== VERDICT ===")
    
    # Check if Lensing tracks Gas (Center) or Stars (Outskirts)
    # Gas is at x=0 (approx index 256)
    # Stars are at x = +/- 1.0
    
    mid_idx = len(x)//2
    gas_centrality = gas[mid_idx] / np.max(gas)
    
    if gas_centrality > 0.5:
        print("Status: Collision Complete. Gas is centered.")
    
    # Check Lensing at center vs outskirts
    lens_center = lensing[mid_idx]
    lens_stars = lensing[idx_star_peak] # Lensing at star position
    
    print(f"Lensing at Center (Gas): {lens_center:.4f}")
    print(f"Lensing at Outskirts (Stars): {lens_stars:.4f}")
    
    if lens_center > lens_stars:
        print(">> FAIL: Lensing signal peaks with the Gas.")
        print(">> The Scalar Field is slaved to the bulk mass.")
    else:
        print(">> PASS: Lensing signal follows the Stars.")
        print(">> (Unexpected result? Check wave dynamics).")

if __name__ == "__main__":
    sim = BulletSimulation()
    hist = sim.run(steps=4000) # Enough time to pass through
    analyze_results(hist)
