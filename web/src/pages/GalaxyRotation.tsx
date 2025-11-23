import { useEffect, useState, useRef } from 'react';
import { fetchRotationCurve, type RotationData } from '../api/client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Activity, Info, Zap } from 'lucide-react';
import Latex from '../components/Latex';

const GalaxyRotation = () => {
    const [data, setData] = useState<RotationData[]>([]);
    const [m0, setM0] = useState(10);
    const [scaleLength, setScaleLength] = useState(10);
    const [beta, setBeta] = useState(1.5);
    const [gpuEnabled, setGpuEnabled] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            try {
                const result = await fetchRotationCurve(m0, scaleLength, beta);
                setData(result.data);
                setGpuEnabled(result.gpu);
            } catch (error) {
                console.error("Failed to fetch galaxy data", error);
            }
        };
        loadData();
    }, [m0, scaleLength, beta]);

    return (
        <div className="space-y-8 animate-fade-in">
            <header>
                <h2 className="text-4xl font-bold mb-2 flex items-center gap-3">
                    <Activity className="text-accent-cyan" size={40} />
                    Galaxy Rotation Problem
                </h2>
                <p className="text-gray-400 max-w-2xl">
                    Simulating galactic rotation curves without Dark Matter.
                    We use a Baryonic Mass Gradient (<Latex>{'$m(r) = m_0 e^{-r / R}$'}</Latex>) to generate flat rotation curves naturally.
                </p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Controls */}
                <div className="space-y-6">
                    <div className="glass-panel p-6">
                        <h3 className="text-lg font-bold mb-4 text-accent-cyan flex justify-between items-center">
                            Parameters
                            {gpuEnabled && <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded flex items-center gap-1"><Zap size={12} /> GPU ACTIVE</span>}
                        </h3>

                        <div className="space-y-6">
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Central Mass (<Latex>$M_0$</Latex>): {m0} &times; 10<sup>10</sup> M<sub>&odot;</sub></label>
                                <input
                                    type="range"
                                    min="1"
                                    max="50"
                                    step="1"
                                    value={m0}
                                    onChange={(e) => setM0(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-cyan"
                                />
                            </div>

                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Scale Length (<Latex>$R$</Latex>): {scaleLength} kpc</label>
                                <input
                                    type="range"
                                    min="1"
                                    max="50"
                                    step="1"
                                    value={scaleLength}
                                    onChange={(e) => setScaleLength(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-cyan"
                                />
                            </div>

                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Gradient Steepness (<Latex>{'$\\beta$'}</Latex>): {beta}</label>
                                <input
                                    type="range"
                                    min="0.1"
                                    max="10"
                                    step="0.1"
                                    value={beta}
                                    onChange={(e) => setBeta(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-cyan"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="glass-panel p-6">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <Info size={18} />
                            The "Kill Shot"
                        </h3>
                        <p className="text-sm text-gray-400 leading-relaxed">
                            Standard Physics predicts velocity should drop as <Latex>{'$1/\\sqrt{r}$'}</Latex> (Keplerian).
                            <br /><br />
                            Observations show flat curves. We achieve this by modifying the mass distribution, not by adding invisible Dark Matter.
                            <br /><br />
                            <strong>Target:</strong> <Latex>{'$R \\approx 15$ kpc, $\\beta \\approx 5$'}</Latex>.
                        </p>
                    </div>
                </div>

                {/* Main Chart */}
                <div className="lg:col-span-2 glass-panel p-6 min-h-[500px] flex flex-col">
                    <h3 className="text-xl font-bold mb-6">Orbital Velocity vs Radius</h3>

                    <div className="flex-1 w-full min-h-[400px]" style={{ height: 400 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                <XAxis
                                    dataKey="r"
                                    stroke="#666"
                                    label={{ value: 'Radius (kpc)', position: 'insideBottom', offset: -5, fill: '#666' }}
                                />
                                <YAxis
                                    stroke="#666"
                                    label={{ value: 'Velocity (km/s)', angle: -90, position: 'insideLeft', fill: '#666' }}
                                />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0a0a0a', borderColor: '#333', color: '#fff' }}
                                    itemStyle={{ color: '#fff' }}
                                    formatter={(value: number) => [`${value.toFixed(2)} km/s`, 'Velocity']}
                                />
                                <Legend />
                                <Line
                                    type="monotone"
                                    dataKey="v"
                                    name="Machian Velocity"
                                    stroke="#00f3ff"
                                    strokeWidth={3}
                                    dot={false}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* N-Body Simulation Section */}
            <NBodySimulation m0={m0} scaleLength={scaleLength} beta={beta} />
        </div>
    );
};

// Sub-component for N-Body Simulation to keep things clean
const NBodySimulation = ({ m0, scaleLength, beta }: { m0: number, scaleLength: number, beta: number }) => {
    const [isRunning, setIsRunning] = useState(false);
    const [nParticles, setNParticles] = useState(1000);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const wsRef = useRef<WebSocket | null>(null);

    const startSimulation = () => {
        if (wsRef.current) {
            wsRef.current.close();
        }

        setIsRunning(true);
        const ws = new WebSocket('ws://localhost:8000/ws/nbody');
        wsRef.current = ws;

        ws.onopen = () => {
            console.log('Connected to N-Body Simulation');
            ws.send(JSON.stringify({
                n_particles: nParticles,
                m0: m0,
                scale_length: scaleLength,
                beta: beta
            }));
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            drawFrame(data.x, data.y);
        };

        ws.onclose = () => {
            console.log('Disconnected from N-Body Simulation');
            setIsRunning(false);
        };
    };

    const stopSimulation = () => {
        if (wsRef.current) {
            wsRef.current.close();
            wsRef.current = null;
        }
        setIsRunning(false);
    };

    const drawFrame = (x: number[], y: number[]) => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = canvas.width;
        const height = canvas.height;
        const scale = 5; // Pixels per kpc
        const cx = width / 2;
        const cy = height / 2;

        // Fade effect for trails
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.fillRect(0, 0, width, height);

        ctx.fillStyle = '#00f3ff';
        for (let i = 0; i < x.length; i++) {
            const px = cx + x[i] * scale;
            const py = cy + y[i] * scale;

            if (px >= 0 && px < width && py >= 0 && py < height) {
                ctx.fillRect(px, py, 2, 2);
            }
        }
    };

    useEffect(() => {
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, []);

    return (
        <div className="glass-panel p-6">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold flex items-center gap-3">
                    <Zap className="text-yellow-400" />
                    N-Body Stability Test
                </h3>
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <label className="text-sm text-gray-400">Particles:</label>
                        <select
                            value={nParticles}
                            onChange={(e) => setNParticles(parseInt(e.target.value))}
                            className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-sm"
                            disabled={isRunning}
                        >
                            <option value="500">500</option>
                            <option value="1000">1000</option>
                            <option value="2000">2000</option>
                            <option value="5000">5000</option>
                        </select>
                    </div>
                    {!isRunning ? (
                        <button
                            onClick={startSimulation}
                            className="bg-accent-cyan text-black font-bold px-6 py-2 rounded hover:bg-cyan-400 transition-colors"
                        >
                            Start Simulation
                        </button>
                    ) : (
                        <button
                            onClick={stopSimulation}
                            className="bg-red-500 text-white font-bold px-6 py-2 rounded hover:bg-red-600 transition-colors"
                        >
                            Stop
                        </button>
                    )}
                </div>
            </div>

            <div className="relative w-full aspect-video bg-black rounded-lg overflow-hidden border border-gray-800">
                <canvas
                    ref={canvasRef}
                    width={800}
                    height={450}
                    className="w-full h-full object-contain"
                />
                {!isRunning && (
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <p className="text-gray-500">Ready to simulate</p>
                    </div>
                )}
            </div>
            <p className="mt-4 text-sm text-gray-400">
                Visualizing the stability of the galactic disk. If the "Inertia Reduction" hypothesis is correct,
                the galaxy should maintain its structure without Dark Matter.
            </p>
        </div>
    );
};

export default GalaxyRotation;
