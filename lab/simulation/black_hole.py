import numpy as np

# Try to import cupy for GPU acceleration, fallback to numpy
try:
    import cupy as cp
    USE_GPU = True
except ImportError:
    import numpy as cp
    USE_GPU = False

class BlackHole:
    """
    Simulates the 'Solid State' Black Hole.
    
    Hypothesis:
    The Event Horizon is a phase transition from Fluid Time to Solid Time.
    At r = Rs, time dilation becomes infinite (dt_proper / dt_coordinate -> 0).
    The universe 'freezes' into a solid state of maximum computational density.
    """
    
    def __init__(self, mass_solar=10.0):
        """
        mass_solar: Mass of the black hole in Solar Masses.
        """
        self.mass_solar = mass_solar
        
        # Constants
        self.G = 6.67430e-11  # m^3 kg^-1 s^-2
        self.c = 2.99792e8    # m/s
        self.M_sun = 1.989e30 # kg
        
        self.mass_kg = self.mass_solar * self.M_sun
        self.Rs = 2 * self.G * self.mass_kg / (self.c**2) # Schwarzschild Radius (meters)

    def time_dilation_factor(self, r):
        """
        Calculates the gravitational time dilation factor at radius r.
        factor = sqrt(1 - Rs/r)
        
        dt_proper = factor * dt_coordinate
        
        At r -> Rs, factor -> 0. Time stops (Solid State).
        """
        r = cp.asarray(r)
        
        # Handle r < Rs (Inside the horizon - imaginary time? Solid state?)
        # For simulation, we clamp at Rs or return 0.
        
        # We want to show the approach.
        ratio = self.Rs / r
        
        # Avoid invalid sqrt for r < Rs
        valid_mask = ratio <= 1.0
        
        factor = cp.zeros_like(r)
        factor[valid_mask] = cp.sqrt(1.0 - ratio[valid_mask])
        
        if USE_GPU:
            return cp.asnumpy(factor)
        else:
            return factor

    def simulate_infall(self, start_distance_rs=10.0, steps=1000, dt_proper=None):
        """
        Simulates Alice falling into the black hole.
        Runs until Alice hits the singularity (r=0).
        """
        
        # Initial conditions
        r = start_distance_rs * self.Rs
        
        # Estimate freefall time (Newtonian approx is good enough for scaling)
        # t_fall ~ (pi/2) * r^(3/2) / sqrt(2GM)
        # In geometric units: t_fall ~ r_rs^(3/2) * Rs/c
        t_fall_estimate = (start_distance_rs**1.5) * (self.Rs / self.c)
        
        # Set timestep to ensure we get ~1000 steps for the fall
        if dt_proper is None:
            dt_proper = t_fall_estimate / 1000.0
            
        tau_alice = []
        t_bob = []
        radii = []
        velocities = []
        
        current_tau = 0.0
        current_t = 0.0
        current_r = r
        
        # Safety limit
        max_steps = 5000
        step_count = 0
        
        while current_r > 0 and step_count < max_steps:
            tau_alice.append(current_tau)
            t_bob.append(current_t)
            radii.append(current_r / self.Rs) # Store in units of Rs
            
            # Velocity (dr/dtau) for fall from rest at infinity
            # v_proper = -c * sqrt(Rs/r)
            # Note: This is for particle falling from infinity. 
            # If falling from rest at r0, it's v = -c * sqrt(Rs/r - Rs/r0) * ... (more complex)
            # For simplicity/visuals, we'll stick to the "rain" metric (falling from infinity)
            # or just the standard Schwarzschild geodesic equation.
            # Geodesic for radial infall from rest at infinity: dr/dtau = -c * sqrt(Rs/r)
            
            if current_r > 0:
                dr_dtau = -self.c * np.sqrt(self.Rs / current_r)
            else:
                dr_dtau = 0
            
            velocities.append(dr_dtau)
            
            # Update r
            current_r += dr_dtau * dt_proper
            
            # Update t (Bob's time)
            # dt/dtau = E / (1 - Rs/r) where E is energy at infinity (E=1 for fall from rest at infinity)
            # So dt = dtau / (1 - Rs/r)
            # Note: The previous formula dt = dtau / sqrt(1 - Rs/r) was for *stationary* observers (gravitational time dilation).
            # For a *falling* observer, the relation is dt/dtau = 1 / (1 - Rs/r).
            # This is even more divergent!
            
            # Clamp r to just above Rs to avoid division by zero
            effective_r = max(current_r, self.Rs * 1.001)
            
            if current_r < self.Rs:
                # Inside horizon: Coordinate time t is spacelike/undefined in standard Schwarzschild coords.
                # We'll just clamp it to the last valid value or let it grow linearly to show "frozen" state?
                # Standard convention: t goes to infinity at Rs.
                # We'll simulate this by adding a huge number if we are close/inside.
                d_t = dt_proper * 1000.0 # "Frozen"
            else:
                dilation = 1.0 - self.Rs / effective_r
                d_t = dt_proper / dilation
            
            current_t += d_t
            current_tau += dt_proper
            step_count += 1
            
        return {
            "tau": np.array(tau_alice),
            "t": np.array(t_bob),
            "r": np.array(radii),
            "v": np.array(velocities),
            "encoding": np.clip(1.0 - (np.array(radii) - 1.0), 0.0, 1.0) # 0 at r>>Rs, 1 at r=Rs
        }

    def get_entropy(self):
        """
        Calculates the Bekenstein-Hawking entropy in bits.
        S = A / (4 * lp^2 * ln(2))
        """
        lp = 1.616255e-35 # Planck length (m)
        area = 4 * np.pi * self.Rs**2
        entropy_nats = area / (4 * lp**2)
        entropy_bits = entropy_nats / np.log(2)
        return entropy_bits

if __name__ == "__main__":
    bh = BlackHole(mass_solar=10)
    print(f"Black Hole Mass: {bh.mass_solar} M_sun")
    print(f"Schwarzschild Radius: {bh.Rs/1000:.3f} km")
    
    # Run with default dynamic timestep
    sim_data = bh.simulate_infall(start_distance_rs=5.0, steps=1000)
    print(f"Simulation steps: {len(sim_data['r'])}")
    print(f"Final Radius: {sim_data['r'][-1]:.4f} Rs")
    print(f"Total Proper Time: {sim_data['tau'][-1]:.6f} s")
    print(f"Total Coordinate Time: {sim_data['t'][-1]:.6f} s")
    
    entropy = bh.get_entropy()
    print(f"Horizon Entropy: {entropy:.2e} bits")
