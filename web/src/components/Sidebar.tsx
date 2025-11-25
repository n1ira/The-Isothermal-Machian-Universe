import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Atom, Orbit, Activity } from 'lucide-react';

const Sidebar = () => {
    const navItems = [
        { path: '/station', icon: LayoutDashboard, label: 'Station' },
        { path: '/lesson/1.1', icon: Atom, label: '1.1 Scale Invariance' },
        { path: '/lesson/1.2', icon: Orbit, label: '1.2 Master Equation' },
        { path: '/lesson/1.3', icon: Orbit, label: '1.3 Dark Matter' },
        { path: '/lesson/1.4', icon: Activity, label: '1.4 Galactic Carousel' },
        { path: '/lesson/2.1', icon: Activity, label: '2.1 The Crisis' },
        { path: '/lesson/2.2', icon: Orbit, label: '2.2 Cosmic Duality' },
        { path: '/lesson/2.3', icon: Activity, label: '2.3 The Dimming' },
        { path: '/lesson/2.4', icon: Orbit, label: '2.4 Solving the Puzzle' },
        { path: '/lesson/3.1', icon: Activity, label: '3.1 The Smoking Gun' },
        { path: '/lesson/3.2', icon: Orbit, label: '3.2 Impossible Galaxies' },
        { path: '/lesson/4.1', icon: Activity, label: '4.1 The Solid Hole' },
        { path: '/lesson/4.2', icon: Orbit, label: '4.2 The Eternal Bounce' },
    ];

    return (
        <aside className="w-64 h-full bg-background border-r border-border flex flex-col p-6 z-20 relative">
            <div className="mb-10">
                <h1 className="text-2xl font-bold neon-text tracking-tighter">MACHIAN</h1>
                <p className="text-xs text-gray-500 tracking-widest mt-1">RESEARCH STATION</p>
            </div>

            <nav className="flex-1 space-y-2">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 group ${isActive
                                ? 'bg-surface border border-accent-cyan/30 text-accent-cyan shadow-[0_0_15px_rgba(0,243,255,0.1)]'
                                : 'text-gray-400 hover:text-white hover:bg-white/5'
                            }`
                        }
                    >
                        <item.icon size={20} className="group-hover:scale-110 transition-transform" />
                        <span className="font-mono text-sm">{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            <div className="mt-auto pt-6 border-t border-border">
                <div className="flex items-center gap-3 text-gray-500 text-xs">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    <span>SYSTEM ONLINE</span>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
