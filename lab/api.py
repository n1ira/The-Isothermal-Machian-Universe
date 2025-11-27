from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from typing import List, Dict

# Import Physics Engines
from lab.simulation import cosmology
from lab.simulation.galaxy_rotation import BaryonicMassGradient, USE_GPU
from lab.simulation.black_hole import BlackHole

app = FastAPI(
    title="Isothermal Machian Universe API",
    description="Backend physics engine for the Machian Universe simulation.",
    version="1.0.0"
)

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "active", "gpu_acceleration": USE_GPU}

# --- Pillar I: Cosmology ---

@app.get("/api/cosmology/lookback")
def get_lookback_time(min_z: float = 0.0, max_z: float = 15.0, steps: int = 100):
    """
    Returns Lookback Time vs Redshift for Machian vs LCDM.
    """
    z_range = np.linspace(min_z, max_z, steps)
    
    data = []
    for z in z_range:
        data.append({
            "z": float(z),
            "machian_gyr": float(val) if (val := cosmology.lookback_time_machian(z)) != float('inf') else None,
            "lcdm_gyr": float(cosmology.lookback_time_lcdm(z)) if z >= 0 else None,
            "mass_factor": float(mf) if (mf := cosmology.get_mass_evolution_factor(z)) != float('inf') else None
        })
        
    return data

# --- Pillar II: Astrophysics ---

@app.get("/api/galaxy/rotation")
def get_rotation_curve(
    m0: float = 10.0, # 10^10 Solar Masses
    scale_length: float = 15.0, # kpc
    beta: float = 5.0,
    max_r: float = 50.0
):
    """
    Returns Velocity vs Radius for the Baryonic Mass Gradient.
    """
    # Convert input to physical units
    m0_val = m0 * 1e10
    
    sim = BaryonicMassGradient(m0=m0_val, scale_length=scale_length, beta=beta)
    
    r = np.linspace(0.1, max_r, 200)
    v_machian = sim.calculate_velocity_profile(r)
    
    # Return as list of points for easy plotting
    data = []
    for i in range(len(r)):
        data.append({
            "r": float(r[i]),
            "v": float(v_machian[i])
        })
        
    return {"data": data, "gpu": USE_GPU}

# --- Pillar III: Quantum Gravity ---

@app.get("/api/blackhole/infall")
def get_infall_trajectory(
    mass: float = 10.0, # Solar Masses
    start_dist: float = 10.0, # Schwarzschild Radii
    steps: int = 1000
):
    """
    Simulates Alice's fall into the Black Hole.
    """
    bh = BlackHole(mass_solar=mass)
    sim_data = bh.simulate_infall(start_distance_rs=start_dist, steps=steps)
    
    # Convert numpy arrays to list
    return {
        "t_coordinate": sim_data['t'].tolist(),
        "tau_proper": sim_data['tau'].tolist(),
        "radius": sim_data['r'].tolist(),
        "velocity": sim_data['v'].tolist(),
        "encoding": sim_data['encoding'].tolist(),
        "rs_km": bh.Rs / 1000.0,
        "entropy_bits": float(bh.get_entropy())
    }

# --- N-Body Simulation (WebSocket) ---

from fastapi import WebSocket, WebSocketDisconnect
from lab.simulation.nbody import NBodySimulator
import json
import asyncio

@app.websocket("/ws/nbody")
async def nbody_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # Wait for initialization parameters
        data = await websocket.receive_text()
        params = json.loads(data)
        
        n_particles = params.get("n_particles", 1000)
        m0 = params.get("m0", 10.0) * 1e10 # Convert to raw mass
        scale_length = params.get("scale_length", 15.0)
        beta = params.get("beta", 5.0)
        
        sim = NBodySimulator(
            n_particles=n_particles,
            m0=m0,
            scale_length=scale_length,
            beta=beta
        )
        
        # Simulation Loop
        while True:
            # Check for incoming control messages (non-blocking)
            # Note: In a simple loop, we might just run. 
            # For interactive controls during sim, we'd need a separate listener task.
            # For now, we'll just stream. Client can close/re-open to reset.
            
            # Step physics
            sim.step(dt=0.01)
            
            # Get positions (convert from CuPy if needed)
            if USE_GPU:
                import cupy as cp
                x = cp.asnumpy(sim.x).tolist()
                y = cp.asnumpy(sim.y).tolist()
            else:
                x = sim.x.tolist()
                y = sim.y.tolist()
            
            # Send frame
            await websocket.send_json({
                "x": x,
                "y": y
            })
            
            # Yield control to event loop briefly to allow for other requests/heartbeats
            await asyncio.sleep(0.01)
            
    except WebSocketDisconnect:
        print("Client disconnected from N-Body simulation")
    except Exception as e:
        print(f"Error in N-Body simulation: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
