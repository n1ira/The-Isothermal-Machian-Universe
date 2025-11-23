"""
MACHIAN P3M SIMULATION (Particle-Particle Particle-Mesh)
--------------------------------------------------------
Goal: Fix small-scale clustering resolution using a CUDA-accelerated Short-Range Force.

Architecture:
  1. Long-Range: FFT-based Particle Mesh (PM) on 128^3 grid.
  2. Short-Range: CUDA Kernel with Cell Lists for neighbor finding.
     - Computes exact forces for pairs with r < r_cut.

Hardware: Requires NVIDIA GPU (CuPy + NVCC).
"""

import numpy as np
import time
import sys
import os
import math

try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    print("CRITICAL: CuPy not found. P3M requires GPU.")
    sys.exit(1)

# ------------------------------------------------------------------------------
# CUDA KERNELS (C++ Implementation)
# ------------------------------------------------------------------------------

CUDA_SOURCE = r'''

extern "C" {



// Constants

#define MAX_NEIGHBORS 64

#define G_CONST 4.30e-9f 

#define MAX_INTERACTIONS 256

#define MAX_CHECKS 2048



__device__ float3 get_periodic_dist(float3 p1, float3 p2, float L) {

    float3 d;

    d.x = p1.x - p2.x;

    d.y = p1.y - p2.y;

    d.z = p1.z - p2.z;

    

    if (d.x > L/2.0f) d.x -= L;

    if (d.x < -L/2.0f) d.x += L;

    if (d.y > L/2.0f) d.y -= L;

    if (d.y < -L/2.0f) d.y += L;

    if (d.z > L/2.0f) d.z -= L;

    if (d.z < -L/2.0f) d.z += L;

    

    return d;

}



__global__ void build_cell_list(

    const float* px, const float* py, const float* pz,

    int* cell_counts, int* particle_indices, 

    int N_particles, int Ng, float L

) {

    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i >= N_particles) return;

    

    if (isnan(px[i]) || isnan(py[i]) || isnan(pz[i])) return;



    float cell_size = L / Ng;

    int cx = (int)(px[i] / cell_size);

    int cy = (int)(py[i] / cell_size);

    int cz = (int)(pz[i] / cell_size);

    

    cx = (cx + Ng) % Ng;

    cy = (cy + Ng) % Ng;

    cz = (cz + Ng) % Ng;

    

    int cell_idx = cx * Ng * Ng + cy * Ng + cz;

    

    atomicAdd(&cell_counts[cell_idx], 1);

}



__global__ void assign_particles(

    const float* px, const float* py, const float* pz,

    int* cell_starts, int* cell_counters, int* particle_indices,

    int N_particles, int Ng, float L

) {

    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i >= N_particles) return;

    

    if (isnan(px[i]) || isnan(py[i]) || isnan(pz[i])) return;



    float cell_size = L / Ng;

    int cx = (int)(px[i] / cell_size);

    int cy = (int)(py[i] / cell_size);

    int cz = (int)(pz[i] / cell_size);

    

    cx = (cx + Ng) % Ng;

    cy = (cy + Ng) % Ng;

    cz = (cz + Ng) % Ng;

    

    int cell_idx = cx * Ng * Ng + cy * Ng + cz;

    

    int pos = atomicAdd(&cell_counters[cell_idx], 1);

    int global_pos = cell_starts[cell_idx] + pos;

    

    if (global_pos < N_particles) {

        particle_indices[global_pos] = i;

    }

}



__global__ void compute_pp_forces(

    const float* px, const float* py, const float* pz,

    float* ax, float* ay, float* az,

    const int* cell_starts, const int* cell_counts, const int* particle_indices,

    int N_particles, int Ng, float L, float r_cut, float force_scale, float beta, float softening

) {

    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i >= N_particles) return;

    

    float3 p1 = make_float3(px[i], py[i], pz[i]);

    float3 acc = make_float3(0.0f, 0.0f, 0.0f);

    

    float cell_size = L / Ng;

    int cx = (int)(p1.x / cell_size);

    int cy = (int)(p1.y / cell_size);

    int cz = (int)(p1.z / cell_size);

    

    int interactions = 0;

    int checks = 0;

    

    for (int dx = -1; dx <= 1; dx++) {

        for (int dy = -1; dy <= 1; dy++) {

            for (int dz = -1; dz <= 1; dz++) {

                

                int ncx = (cx + dx + Ng) % Ng;

                int ncy = (cy + dy + Ng) % Ng;

                int ncz = (cz + dz + Ng) % Ng;

                

                int cell_idx = ncx * Ng * Ng + ncy * Ng + ncz;

                

                int start = cell_starts[cell_idx];

                int count = cell_counts[cell_idx];

                

                for (int k = 0; k < count; k++) {

                    if (interactions >= MAX_INTERACTIONS) break;

                    if (checks >= MAX_CHECKS) break;

                    

                    checks++;

                    

                    if (start + k >= N_particles) continue;

                    

                    int j = particle_indices[start + k];

                    

                    if (j >= N_particles || j < 0) continue;

                    if (i == j) continue;

                    

                    float3 p2 = make_float3(px[j], py[j], pz[j]);

                    float3 d = get_periodic_dist(p1, p2, L);

                    

                    float r2 = d.x*d.x + d.y*d.y + d.z*d.z;

                    

                    if (r2 < r_cut * r_cut) {

                        interactions++;

                        

                        float r2_soft = r2 + softening * softening;

                        float inv_dist = rsqrtf(r2_soft);

                        float inv_dist3 = inv_dist * inv_dist * inv_dist;

                        

                        float f_mag = inv_dist3 * (1.0f + beta); 

                        

                        acc.x -= d.x * f_mag;

                        acc.y -= d.y * f_mag;

                        acc.z -= d.z * f_mag;

                    }

                }

            }

        }

    }

    

    ax[i] += acc.x * force_scale;

    ay[i] += acc.y * force_scale;

    az[i] += acc.z * force_scale;

}



}

'''



class MachianP3M:

    def __init__(self, N_particles=64**3, grid_size=128, box_size=100.0, beta=10.0, force_scale=50000.0, drag_coeff=0.5):

        self.N = N_particles

        self.Ng = grid_size

        self.L = box_size

        self.beta = beta

        self.force_scale = force_scale

        self.drag_coeff = drag_coeff

        

        # Compile Kernels

        self.module = cp.RawModule(code=CUDA_SOURCE)

        self.ker_build = self.module.get_function('build_cell_list')

        self.ker_assign = self.module.get_function('assign_particles')

        self.ker_force = self.module.get_function('compute_pp_forces')

        

        # State (Structure of Arrays for CUDA performance)

        self.pos_x = None

        self.pos_y = None

        self.pos_z = None

        self.vel_x = None

        self.vel_y = None

        self.vel_z = None

        

        self.xp = cp

        

    # ... (initialize_zeldovich, compute_density_mesh, compute_pm_forces same as before)

    def initialize_zeldovich(self):

        print("Initializing P3M State (SoA)...")

        N_side = int(np.round(self.N**(1/3)))

        dx = self.L / N_side

        q = self.xp.mgrid[0:N_side, 0:N_side, 0:N_side].reshape(3, -1).T * dx

        disp = self.xp.random.normal(0, 0.5, q.shape) * dx * 0.5

        self.pos_x = self.xp.mod(q[:,0] + disp[:,0], self.L).astype(self.xp.float32)

        self.pos_y = self.xp.mod(q[:,1] + disp[:,1], self.L).astype(self.xp.float32)

        self.pos_z = self.xp.mod(q[:,2] + disp[:,2], self.L).astype(self.xp.float32)

        self.vel_x = (disp[:,0] * 10.0).astype(self.xp.float32)

        self.vel_y = (disp[:,1] * 10.0).astype(self.xp.float32)

        self.vel_z = (disp[:,2] * 10.0).astype(self.xp.float32)

        self.cell_counts = self.xp.zeros(self.Ng**3, dtype=self.xp.int32)

        self.cell_starts = self.xp.zeros(self.Ng**3, dtype=self.xp.int32)

        self.cell_counters = self.xp.zeros(self.Ng**3, dtype=self.xp.int32)

        self.particle_indices = self.xp.zeros(self.N, dtype=self.xp.int32)



    def compute_density_mesh(self):

        grid = self.xp.zeros((self.Ng, self.Ng, self.Ng), dtype=self.xp.float32)

        idx_x = (self.pos_x / self.L * self.Ng).astype(self.xp.int32)

        idx_y = (self.pos_y / self.L * self.Ng).astype(self.xp.int32)

        idx_z = (self.pos_z / self.L * self.Ng).astype(self.xp.int32)

        idx_x = self.xp.mod(idx_x, self.Ng)

        idx_y = self.xp.mod(idx_y, self.Ng)

        idx_z = self.xp.mod(idx_z, self.Ng)

        flat_idx = idx_x*self.Ng*self.Ng + idx_y*self.Ng + idx_z

        self.xp.add.at(grid.ravel(), flat_idx, 1.0)

        delta = (grid / (self.N/self.Ng**3)) - 1.0

        return delta



    def compute_pm_forces(self, verbose=False):

        if verbose: print("  [PM] Density...", end='', flush=True)

        delta = self.compute_density_mesh()

        delta_k = self.xp.fft.rfftn(delta)

        idx_x = self.xp.mod((self.pos_x / self.L * self.Ng).astype(self.xp.int32), self.Ng)

        idx_y = self.xp.mod((self.pos_y / self.L * self.Ng).astype(self.xp.int32), self.Ng)

        idx_z = self.xp.mod((self.pos_z / self.L * self.Ng).astype(self.xp.int32), self.Ng)

        kx = self.xp.fft.fftfreq(self.Ng) * self.Ng * 2 * np.pi / self.L

        ky = self.xp.fft.fftfreq(self.Ng) * self.Ng * 2 * np.pi / self.L

        kz = self.xp.fft.rfftfreq(self.Ng) * self.Ng * 2 * np.pi / self.L

        kx, ky, kz = self.xp.meshgrid(kx, ky, kz, indexing='ij')

        k_sq = kx**2 + ky**2 + kz**2

        k_sq[0,0,0] = 1.0

        phi_k = -1.0 * delta_k / k_sq * (1.0 + self.beta)

        phi_k[0,0,0] = 0

        phi = self.xp.fft.irfftn(phi_k)

        if verbose: print(" Grad...", end='', flush=True)

        g0, g1, g2 = self.xp.gradient(phi)

        acc_x = g0[idx_x, idx_y, idx_z]

        acc_y = g1[idx_x, idx_y, idx_z]

        acc_z = g2[idx_x, idx_y, idx_z]

        if verbose: print(" Done.", flush=True)

        return -acc_x, -acc_y, -acc_z



    def compute_pp_forces(self, ax, ay, az, verbose=False):

        """

        Short Range Correction using CUDA (Debug Mode)

        """

        if verbose: 

            print("\n    [PP Debug]", end='', flush=True)

            t_pp = time.time()



        # 1. Reset Cell Lists

        self.cell_counts.fill(0)

        self.cell_counters.fill(0)

        if verbose: 

            self.xp.cuda.Device().synchronize()

            print(f" Reset({time.time()-t_pp:.3f}s)", end='', flush=True)

        

        block_dim = 256

        grid_dim = (self.N + block_dim - 1) // block_dim

        

        # 2. Build Counts

        self.ker_build((grid_dim,), (block_dim,), (

            self.pos_x, self.pos_y, self.pos_z,

            self.cell_counts, self.particle_indices,

            self.N, self.Ng, self.L

        ))

        if verbose: 

            self.xp.cuda.Device().synchronize()

            print(f" Build({time.time()-t_pp:.3f}s)", end='', flush=True)

        

        # 3. Prefix Sum

        self.cell_starts = self.xp.cumsum(self.cell_counts) - self.cell_counts

        if verbose: 

            self.xp.cuda.Device().synchronize()

            print(f" Scan({time.time()-t_pp:.3f}s)", end='', flush=True)

        

        # 4. Assign Particles

        self.ker_assign((grid_dim,), (block_dim,), (

            self.pos_x, self.pos_y, self.pos_z,

            self.cell_starts, self.cell_counters, self.particle_indices,

            self.N, self.Ng, self.L

        ))

        if verbose: 

            self.xp.cuda.Device().synchronize()

            print(f" Assign({time.time()-t_pp:.3f}s)", end='', flush=True)

        

        # 5. Compute Short Range Forces

        r_cut = 2.0 * (self.L / self.Ng)

        softening = 0.05 

        

        self.ker_force((grid_dim,), (block_dim,), (

            self.pos_x, self.pos_y, self.pos_z,

            ax, ay, az,

            self.cell_starts, self.cell_counts, self.particle_indices,

            self.N, self.Ng, self.L, r_cut, self.force_scale, self.beta, softening

        ))

        

        if verbose:

            self.xp.cuda.Device().synchronize()

            print(f" Kernel({time.time()-t_pp:.3f}s)", flush=True)

        

        return ax, ay, az

    def step(self, dt, verbose=False):
        t0 = time.time()
        # 1. PM Force
        ax, ay, az = self.compute_pm_forces(verbose=verbose)
        
        # 2. PP Force (Add on)
        # Ensure they are contiguous
        ax = cp.ascontiguousarray(ax)
        ay = cp.ascontiguousarray(ay)
        az = cp.ascontiguousarray(az)
        
        ax, ay, az = self.compute_pp_forces(ax, ay, az, verbose=verbose)
        
        # 3. Update
        if verbose: print("  [Step] Integration...", end='', flush=True)
        
        # Apply Hubble Drag (Cosmic Friction)
        damping = (1.0 - self.drag_coeff * dt)
        self.vel_x *= damping
        self.vel_y *= damping
        self.vel_z *= damping
        
        self.vel_x += ax * self.force_scale * dt
        self.vel_y += ay * self.force_scale * dt
        self.vel_z += az * self.force_scale * dt
        
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        self.pos_z += self.vel_z * dt
        
        self.pos_x = self.xp.mod(self.pos_x, self.L)
        self.pos_y = self.xp.mod(self.pos_y, self.L)
        self.pos_z = self.xp.mod(self.pos_z, self.L)
        
        if verbose:
            self.xp.cuda.Device().synchronize()
            print(f" Done. ({time.time()-t0:.4f}s)", flush=True)

    def step(self, dt, verbose=False):
        t0 = time.time()
        # 1. PM Force
        ax, ay, az = self.compute_pm_forces(verbose=verbose)
        
        # 2. PP Force (Add on)
        # Ensure they are contiguous
        ax = cp.ascontiguousarray(ax)
        ay = cp.ascontiguousarray(ay)
        az = cp.ascontiguousarray(az)
        
        ax, ay, az = self.compute_pp_forces(ax, ay, az, verbose=verbose)
        
        # 3. Update
        if verbose: print("  [Step] Integration...", end='', flush=True)
        
        # Apply Hubble Drag (Cosmic Friction)
        damping = (1.0 - self.drag_coeff * dt)
        self.vel_x *= damping
        self.vel_y *= damping
        self.vel_z *= damping
        
        self.vel_x += ax * self.force_scale * dt
        self.vel_y += ay * self.force_scale * dt
        self.vel_z += az * self.force_scale * dt
        
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        self.pos_z += self.vel_z * dt
        
        self.pos_x = self.xp.mod(self.pos_x, self.L)
        self.pos_y = self.xp.mod(self.pos_y, self.L)
        self.pos_z = self.xp.mod(self.pos_z, self.L)
        
        if verbose:
            self.xp.cuda.Device().synchronize()
            print(f" Done. ({time.time()-t0:.4f}s)", flush=True)