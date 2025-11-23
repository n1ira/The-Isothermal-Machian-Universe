import { useEffect, useState } from 'react';
import { fetchLookbackTime, type LookbackData } from '../api/client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Clock, Info } from 'lucide-react';
import Latex from '../components/Latex';

const Cosmology = () => {
    const [data, setData] = useState<LookbackData[]>([]);
    const [maxZ, setMaxZ] = useState(15);
    const [showFuture, setShowFuture] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            const minZ = showFuture ? -1.0 : 0;
            const result = await fetchLookbackTime(minZ, maxZ);
            setData(result);
        };
        loadData();
    }, [maxZ, showFuture]);

    const hasSingularity = data.some(d => d.z < 0 && d.machian_gyr === null);

    return (
        <div className="space-y-8 animate-fade-in">
            <header>
                <h2 className="text-4xl font-bold mb-2 flex items-center gap-3">
                    <Clock className="text-accent-cyan" size={40} />
                    Cosmology: The Age Crisis
                </h2>
                <p className="text-gray-400 max-w-2xl">
                    Simulating the age of the universe under the Isothermal Machian framework.
                    By allowing mass to evolve (<Latex>{'$m \\propto 1+z$'}</Latex>), we resolve the JWST "impossible early galaxy" problem.
                </p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Controls & Stats */}
                <div className="space-y-6">
                    <div className="glass-panel p-6">
                        <h3 className="text-lg font-bold mb-4 text-accent-cyan">Simulation Parameters</h3>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Max Redshift (z): {maxZ}</label>
                                <input
                                    type="range"
                                    min="1"
                                    max="20"
                                    step="0.5"
                                    value={maxZ}
                                    onChange={(e) => setMaxZ(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-cyan"
                                />
                            </div>

                            <div className="flex items-center gap-3 pt-4 border-t border-gray-800">
                                <input
                                    type="checkbox"
                                    id="futureMode"
                                    checked={showFuture}
                                    onChange={(e) => setShowFuture(e.target.checked)}
                                    className="w-5 h-5 accent-accent-pink rounded cursor-pointer"
                                />
                                <label htmlFor="futureMode" className="text-sm text-gray-300 cursor-pointer select-none">
                                    Show Future Evolution (<span className="text-accent-pink">Blue Screen of Death</span>)
                                </label>
                            </div>
                        </div>
                    </div>

                    <div className="glass-panel p-6">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <Info size={18} />
                            Key Insight
                        </h3>
                        <p className="text-sm text-gray-400 leading-relaxed">
                            In the Standard Model (<Latex>{'$\\Lambda$CDM'}</Latex>), the universe is only ~500 Myr old at <Latex>{'$z=10$'}</Latex>.
                            <br /><br />
                            In the <span className="text-accent-cyan font-bold">Machian Model</span>, clocks ticked faster in the past (due to lower mass), making the universe effectively <span className="text-accent-pink font-bold">older</span> at high redshift.
                        </p>
                    </div>

                    {hasSingularity && (
                        <div className="glass-panel p-6 border-accent-pink bg-red-900/20">
                            <h3 className="text-lg font-bold mb-2 text-accent-pink flex items-center gap-2">
                                ⚠️ SINGULARITY DETECTED
                            </h3>
                            <p className="text-sm text-gray-300">
                                At <Latex>{'$z \\approx -1$'}</Latex>, mass becomes infinite. Time stops. The universe enters the "Solid State" globally.
                            </p>
                        </div>
                    )}
                </div>

                {/* Main Chart */}
                <div className="lg:col-span-2 glass-panel p-6 min-h-[500px] flex flex-col">
                    <h3 className="text-xl font-bold mb-6">Lookback Time vs Redshift</h3>

                    <div className="flex-1 w-full h-full min-h-[400px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                <XAxis
                                    dataKey="z"
                                    stroke="#666"
                                    label={{ value: 'Redshift (z)', position: 'insideBottom', offset: -5, fill: '#666' }}
                                    domain={[showFuture ? -1 : 0, 'auto']}
                                />
                                <YAxis
                                    stroke="#666"
                                    label={{ value: 'Lookback Time (Gyr)', angle: -90, position: 'insideLeft', fill: '#666' }}
                                />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0a0a0a', borderColor: '#333', color: '#fff' }}
                                    itemStyle={{ color: '#fff' }}
                                    labelFormatter={(label) => `z = ${Number(label).toFixed(2)}`}
                                />
                                <Legend />
                                <Line
                                    type="monotone"
                                    dataKey="machian_gyr"
                                    name="Machian (Static)"
                                    stroke="#00f3ff"
                                    strokeWidth={3}
                                    dot={false}
                                    connectNulls={false}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="lcdm_gyr"
                                    name="Standard LCDM"
                                    stroke="#ff4444"
                                    strokeWidth={2}
                                    strokeDasharray="5 5"
                                    dot={false}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Cosmology;
