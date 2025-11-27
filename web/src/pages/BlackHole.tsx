import { useEffect, useState, useMemo } from 'react';
import { fetchInfallTrajectory, type InfallData } from '../api/client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ReferenceLine } from 'recharts';
import { Disc, Info } from 'lucide-react';
import Latex from '../components/Latex';
import HolographicScreen from '../components/HolographicScreen';

const BlackHole = () => {
    const [data, setData] = useState<InfallData | null>(null);
    const [mass, setMass] = useState(10);
    const [startDist, setStartDist] = useState(10);

    useEffect(() => {
        const loadData = async () => {
            try {
                const result = await fetchInfallTrajectory(mass, startDist);
                setData(result);
            } catch (error) {
                console.error("Failed to fetch black hole data", error);
            }
        };
        loadData();
    }, [mass, startDist]);

    const chartData = useMemo(() => {
        if (!data) return [];
        return data.radius.map((r, i) => ({
            r: r * data.rs_km, // Convert Rs units to km
            t: data.t_coordinate[i],
            tau: data.tau_proper[i],
        }));
    }, [data]);

    return (
        <div className="space-y-8 animate-fade-in">
            <header>
                <h2 className="text-4xl font-bold mb-2 flex items-center gap-3">
                    <Disc className="text-accent-purple" size={40} />
                    Black Hole: The Event Horizon
                </h2>
                <p className="text-gray-400 max-w-2xl">
                    Simulating the trajectory of an observer (Alice) falling into a Schwarzschild Black Hole.
                    Compare Coordinate Time (distant observer) vs Proper Time (Alice's wristwatch).
                </p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Controls */}
                <div className="space-y-6 lg:col-span-1">
                    <div className="glass-panel p-6">
                        <h3 className="text-lg font-bold mb-4 text-accent-purple">Parameters</h3>
                        <div className="space-y-6">
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Black Hole Mass: {mass} <Latex>$M_\odot$</Latex></label>
                                <input
                                    type="range"
                                    min="5"
                                    max="100"
                                    step="1"
                                    value={mass}
                                    onChange={(e) => setMass(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-purple"
                                />
                            </div>

                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Start Distance: {startDist} <Latex>$R_s$</Latex></label>
                                <input
                                    type="range"
                                    min="2"
                                    max="50"
                                    step="1"
                                    value={startDist}
                                    onChange={(e) => setStartDist(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-purple"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="glass-panel p-6">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <Info size={18} />
                            Time Dilation
                        </h3>
                        <p className="text-sm text-gray-400 leading-relaxed">
                            As Alice approaches the Event Horizon (<Latex>$R_s$</Latex>):
                            <br /><br />
                            <span className="text-accent-cyan font-bold">Coordinate Time (<Latex>$t$</Latex>)</span> goes to infinity (she never seems to cross).
                            <br /><br />
                            <span className="text-accent-pink font-bold">Proper Time (<Latex>$\tau$</Latex>)</span> is finite. She crosses in a finite amount of time on her watch.
                        </p>
                    </div>
                </div>

                {/* Main Chart */}
                <div className="lg:col-span-3 flex flex-col gap-8">
                    <div className="glass-panel p-6 min-h-[500px] flex flex-col">
                        <h3 className="text-xl font-bold mb-6">Infall Trajectory (Time vs Distance)</h3>

                        <div className="flex-1 w-full h-full min-h-[400px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                    <XAxis
                                        dataKey="r"
                                        type="number"
                                        reversed={true}
                                        stroke="#666"
                                        label={{ value: 'Distance from Singularity (km)', position: 'insideBottom', offset: -5, fill: '#666' }}
                                        domain={['auto', 'auto']}
                                    />
                                    <YAxis
                                        stroke="#666"
                                        label={{ value: 'Time (s)', angle: -90, position: 'insideLeft', fill: '#666' }}
                                    />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#0a0a0a', borderColor: '#333', color: '#fff' }}
                                        itemStyle={{ color: '#fff' }}
                                        labelFormatter={(value) => `Distance: ${Number(value).toFixed(0)} km`}
                                    />
                                    <Legend />
                                    {data && (
                                        <ReferenceLine
                                            x={data.rs_km}
                                            stroke="red"
                                            strokeDasharray="3 3"
                                            label={{ value: 'Event Horizon', fill: 'red', position: 'insideTopLeft' }}
                                        />
                                    )}
                                    <Line
                                        type="monotone"
                                        dataKey="t"
                                        name="Coordinate Time (Distant)"
                                        stroke="#00f3ff"
                                        strokeWidth={2}
                                        dot={false}
                                    />
                                    <Line
                                        type="monotone"
                                        dataKey="tau"
                                        name="Proper Time (Alice)"
                                        stroke="#ff00ff"
                                        strokeWidth={2}
                                        dot={false}
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Holographic Screen Visualization */}
                    <div className="glass-panel p-6">
                        <h3 className="text-xl font-bold mb-4 text-accent-cyan">Holographic Screen</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                            <div>
                                <p className="text-gray-400 mb-4">
                                    As Alice approaches the horizon, her information is encoded onto the surface.
                                    The "Solid State" hypothesis suggests the horizon is a hard drive of maximum density.
                                </p>
                                <div className="bg-black/40 p-4 rounded-lg border border-gray-800">
                                    <div className="text-sm text-gray-500 mb-1">Horizon Entropy (Bekenstein-Hawking)</div>
                                    <div className="text-2xl font-mono text-accent-pink">
                                        {data ? data.entropy_bits.toExponential(2) : '...'} bits
                                    </div>
                                </div>
                            </div>

                            {/* Visual representation of bits accumulating */}
                            <div className="relative h-40 bg-black rounded-lg overflow-hidden border border-gray-800 flex items-center justify-center">
                                <HolographicScreen entropy={data ? data.entropy_bits : 0} />
                                <div className="z-10 text-center pointer-events-none mix-blend-difference">
                                    <div className="text-accent-cyan font-bold text-lg mb-2">Information Density</div>
                                    <div className="text-xs text-gray-400 font-mono">
                                        {data ? "SURFACE ACTIVE" : "WAITING FOR DATA..."}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BlackHole;
