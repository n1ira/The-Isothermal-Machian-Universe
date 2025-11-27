import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
});

export interface LookbackData {
    z: number;
    machian_gyr: number;
    lcdm_gyr: number;
    mass_factor: number;
}

export interface RotationData {
    r: number;
    v: number;
}

export interface InfallData {
    t_coordinate: number[];
    tau_proper: number[];
    radius: number[];
    velocity: number[];
    encoding: number[];
    rs_km: number;
    entropy_bits: number;
}

export const fetchLookbackTime = async (minZ = 0, maxZ = 15) => {
    const response = await api.get<LookbackData[]>('/api/cosmology/lookback', { params: { min_z: minZ, max_z: maxZ } });
    return response.data;
};

export const fetchRotationCurve = async (m0: number, scale: number, beta: number) => {
    const response = await api.get<{ data: RotationData[], gpu: boolean }>('/api/galaxy/rotation', {
        params: { m0, scale_length: scale, beta }
    });
    return response.data;
};

export const fetchInfallTrajectory = async (mass: number, startDist: number) => {
    const response = await api.get<InfallData>('/api/blackhole/infall', {
        params: { mass, start_dist: startDist }
    });
    return response.data;
};

export const checkHealth = async () => {
    try {
        const response = await api.get('/');
        return response.data;
    } catch {
        return null;
    }
}
