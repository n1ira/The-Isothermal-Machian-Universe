import { useEffect, useState } from 'react';
import { checkHealth } from '../api/client';
import { Activity, Cpu, Database, Zap } from 'lucide-react';

const Dashboard = () => {
    const [status, setStatus] = useState<{ status: string; gpu_acceleration: boolean } | null>(null);

    useEffect(() => {
        checkHealth().then(setStatus);
    }, []);

    const stats = [
        { label: 'Physics Engine', value: status ? 'ACTIVE' : 'OFFLINE', icon: Activity, color: 'text-green-400' },
        { label: 'GPU Acceleration', value: status?.gpu_acceleration ? 'ENABLED' : 'DISABLED', icon: Zap, color: status?.gpu_acceleration ? 'text-yellow-400' : 'text-gray-500' },
        { label: 'Active Simulations', value: '3', icon: Cpu, color: 'text-accent-cyan' },
        { label: 'Data Points', value: '1.2M', icon: Database, color: 'text-accent-pink' },
    ];

    return (
        <div className="space-y-8 animate-fade-in">
            <header>
                <h2 className="text-4xl font-bold mb-2">Command Center</h2>
                <p className="text-gray-400">Overview of the Isothermal Machian Universe simulation status.</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat) => (
                    <div key={stat.label} className="glass-panel p-6 flex items-center justify-between hover:border-accent-cyan/50 transition-colors group">
                        <div>
                            <p className="text-sm text-gray-500 font-mono mb-1">{stat.label}</p>
                            <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
                        </div>
                        <div className={`p-3 rounded-full bg-white/5 group-hover:bg-white/10 transition-colors ${stat.color}`}>
                            <stat.icon size={24} />
                        </div>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="glass-panel p-8">
                    <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <span className="w-1 h-6 bg-accent-cyan rounded-full" />
                        System Status
                    </h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center border-b border-white/5 pb-2">
                            <span className="text-gray-400">Backend API</span>
                            <span className={status ? "text-green-400" : "text-red-400"}>
                                {status ? "CONNECTED (Port 8000)" : "DISCONNECTED"}
                            </span>
                        </div>
                        <div className="flex justify-between items-center border-b border-white/5 pb-2">
                            <span className="text-gray-400">Frontend</span>
                            <span className="text-green-400">ONLINE (Vite)</span>
                        </div>
                        <div className="flex justify-between items-center border-b border-white/5 pb-2">
                            <span className="text-gray-400">Database</span>
                            <span className="text-gray-500">N/A (In-Memory)</span>
                        </div>
                    </div>
                </div>

                <div className="glass-panel p-8 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-32 bg-accent-pink/10 blur-[100px] rounded-full pointer-events-none" />
                    <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <button className="p-4 rounded-lg bg-white/5 hover:bg-accent-cyan/20 hover:text-accent-cyan transition-all text-left border border-transparent hover:border-accent-cyan/30">
                            <span className="block font-bold mb-1">Run Diagnostics</span>
                            <span className="text-xs text-gray-500">Check system integrity</span>
                        </button>
                        <button className="p-4 rounded-lg bg-white/5 hover:bg-accent-pink/20 hover:text-accent-pink transition-all text-left border border-transparent hover:border-accent-pink/30">
                            <span className="block font-bold mb-1">Reset Simulation</span>
                            <span className="text-xs text-gray-500">Clear all states</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
