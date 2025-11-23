import numpy as np
import time
from lab.simulation.galaxy_rotation import BaryonicMassGradient, USE_GPU

if USE_GPU:
    import cupy as cp
else:
    import numpy as cp

class NBodySimulator:
    def __init__(self, n_particles=1000, m0=1e11, scale_length=15.0, beta=5.0):
        self.n_particles = n_particles
        self.physics = BaryonicMassGradient(m0, scale_length, beta)
        
        # Initialize particles in a disk
        # Random radii with exponential distribution (matches mass density)
        # P(r) ~ r * e^-r/R
        # We'll just use uniform for visual simplicity in the 'test'
        self.radii = cp.random.uniform(0.1, 50.0, n_particles)
        self.angles = cp.random.uniform(0, 2*np.pi, n_particles)
        
        # Calculate initial velocities to be in circular orbit
        # v = v_machian(r)
        # calculate_velocity_profile returns numpy array always
        # We pass self.radii directly. If on GPU, it's a cupy array, which galaxy_rotation handles.
        v_cpu = self.physics.calculate_velocity_profile(self.radii)
        self.velocities = cp.asarray(v_cpu)
        
        # State: x, y, vx, vy
        self.x = self.radii * cp.cos(self.angles)
        self.y = self.radii * cp.sin(self.angles)
        
        # Velocity vectors (tangential)
        # v_x = -v * sin(theta)
        # v_y = v * cos(theta)
        self.vx = -self.velocities * cp.sin(self.angles)
        self.vy = self.velocities * cp.cos(self.angles)
        
    def step(self, dt=0.01):
        """
        Evolve system.
        """
        r = cp.sqrt(self.x**2 + self.y**2)
        
        # Calculate velocity profile
        # Pass r directly.
        v_mag_cpu = self.physics.calculate_velocity_profile(r)
        v_mag = cp.asarray(v_mag_cpu)
        
        a_mag = (v_mag**2) / r
        
        ax = -a_mag * (self.x / r)
        ay = -a_mag * (self.y / r)
        
        # Leapfrog or Euler
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        return self.x, self.y

if __name__ == "__main__":
    print("Initializing N-Body Simulation...")
    sim = NBodySimulator(n_particles=5000)
    print(f"Running on {'GPU' if USE_GPU else 'CPU'}")
    
    start = time.time()
    for i in range(100):
        sim.step()
    end = time.time()
    
    print(f"Simulated 100 steps in {end-start:.4f}s")
