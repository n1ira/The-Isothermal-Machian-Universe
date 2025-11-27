import { useState, useEffect, useRef } from 'react';
import Latex from '../components/Latex';

const Lesson2_3 = () => {
    const [distance, setDistance] = useState(50);
    const [isMachian, setIsMachian] = useState(false);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Physics Constants
    const L0 = 10000; // Intrinsic Luminosity

    // Calculate Brightness
    // Standard: B = L / (4 * pi * d^2)
    // Machian: B = L / (4 * pi * d^2) * (1+z)^(-alpha)
    // For simplicity in this demo, we model the "Dimming" as an extra decay factor
    // In Machian frame, mass of source was lower in past -> less intrinsic luminosity?
    // Actually Paper B says: D_L = (1+z)^2 D_A * (1+z)^(alpha/2)
    // So D_L is LARGER than expected -> Dimmer.
    const getBrightness = (d: number, machian: boolean) => {
        // Avoid division by zero
        const r = Math.max(d, 10);
        let b = L0 / (r * r);

        if (machian) {
            // Simulating the extra dimming
            // As distance increases, redshift increases.
            // Let's say z ~ distance / 100
            const z = d / 200;
            // Dimming factor eta = (1+z)^(alpha/2). If alpha > 0, it's dimmer.
            // Let's pick a visible effect
            const dimmingFactor = Math.pow(1 + z, 2); // Strong dimming for visual
            b = b / dimmingFactor;
        }
        return b;
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;

        const draw = () => {
            const width = canvas.width;
            const height = canvas.height;
            const cy = height / 2;

            // Clear
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, width, height);

            // Draw Observer (Earth)
            ctx.fillStyle = '#00f3ff';
            ctx.beginPath();
            ctx.arc(50, cy, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#fff';
            ctx.font = '12px monospace';
            ctx.textAlign = 'center';
            ctx.fillText('EARTH', 50, cy + 25);

            // Draw Supernova
            // Map distance 0-100 slider to screen x
            const starX = 100 + (distance / 100) * (width - 150);

            // Calculate visual brightness (radius and opacity)
            const brightness = getBrightness(distance, isMachian);
            // Normalize for display
            const maxB = getBrightness(10, false);
            const intensity = Math.min(brightness / maxB, 1);

            // Glow
            const gradient = ctx.createRadialGradient(starX, cy, 5, starX, cy, 40);
            gradient.addColorStop(0, `rgba(255, 200, 50, ${intensity})`);
            gradient.addColorStop(1, 'rgba(255, 100, 50, 0)');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(starX, cy, 40, 0, Math.PI * 2);
            ctx.fill();

            // Star Core
            ctx.fillStyle = `rgba(255, 255, 255, ${intensity})`;
            ctx.beginPath();
            ctx.arc(starX, cy, 5, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#fff';
            ctx.fillText('SN Ia', starX, cy + 50);

            // Draw Light Rays
            ctx.strokeStyle = `rgba(255, 200, 50, ${intensity * 0.5})`;
            ctx.lineWidth = 2;
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(starX, cy);
            ctx.lineTo(50, cy);
            ctx.stroke();
            ctx.setLineDash([]);

            // Draw Graph Overlay (Mini)
            const graphH = 100;
            const graphW = 200;
            const graphX = width - graphW - 20;
            const graphY = 20;

            // Graph Background
            ctx.fillStyle = 'rgba(0,0,0,0.8)';
            ctx.fillRect(graphX, graphY, graphW, graphH);
            ctx.strokeStyle = '#333';
            ctx.strokeRect(graphX, graphY, graphW, graphH);

            // Plot Curves
            ctx.lineWidth = 2;

            // Standard Curve (Blue)
            ctx.strokeStyle = '#3b82f6';
            ctx.beginPath();
            for (let d = 0; d < 100; d++) {
                const x = graphX + (d / 100) * graphW;
                const b = getBrightness(10 + d, false); // shift to avoid infinity
                const y = graphY + graphH - (b / maxB) * graphH;
                if (d === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();

            // Machian Curve (Purple)
            if (isMachian) {
                ctx.strokeStyle = '#a855f7';
                ctx.beginPath();
                for (let d = 0; d < 100; d++) {
                    const x = graphX + (d / 100) * graphW;
                    const b = getBrightness(10 + d, true);
                    const y = graphY + graphH - (b / maxB) * graphH;
                    if (d === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                ctx.stroke();
            }

            // Current Point
            const currX = graphX + (distance / 100) * graphW;
            const currB = getBrightness(distance, isMachian);
            const currY = graphY + graphH - (currB / maxB) * graphH;

            ctx.fillStyle = '#fff';
            ctx.beginPath();
            ctx.arc(currX, currY, 4, 0, Math.PI * 2);
            ctx.fill();

            // Labels
            ctx.fillStyle = '#aaa';
            ctx.font = '10px monospace';
            ctx.fillText('Brightness vs Distance', graphX + 10, graphY + 15);

            animationFrameId = requestAnimationFrame(draw);
        };

        draw();

        return () => cancelAnimationFrame(animationFrameId);
    }, [distance, isMachian]);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 2</span>
                    <span>/</span>
                    <span>LESSON 2.3</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-purple-400">
                    The Dimming
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    Why the universe looks like it's accelerating, when it's actually just getting heavier.
                </p>
            </header>

            {/* Section 1: The Foggy Glasses */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Foggy Glasses</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Imagine you are looking at a streetlamp through a thick fog. It looks dimmer than it should, right?
                        If you didn't know about the fog, you might think the streetlamp is <strong>further away</strong> than it actually is.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        In 1998, astronomers looked at Type Ia Supernovae (Standard Candles) and found they were dimmer than expected.
                        They concluded: <em>"The universe must be expanding faster and faster, pushing them away!"</em>
                        They called this <strong>Dark Energy</strong>.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        But the Isothermal Machian Universe offers a different explanation: <strong>The Mass Evolution</strong>.
                    </p>
                </div>
            </section>

            {/* Section 2: Interactive Simulation */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. Etherington Violation</h2>
                <div className="glass-panel p-8 space-y-6">
                    <div className="flex flex-col gap-6">
                        <div className="flex items-center justify-between bg-black/20 p-4 rounded-lg">
                            <div className="space-y-2">
                                <label className="text-sm text-gray-400">Distance to Supernova</label>
                                <input
                                    type="range"
                                    min="0"
                                    max="100"
                                    value={distance}
                                    onChange={(e) => setDistance(parseInt(e.target.value))}
                                    className="w-64 accent-accent-cyan block"
                                />
                            </div>

                            <div className="flex items-center gap-4">
                                <span className={`text-sm ${!isMachian ? 'text-blue-400 font-bold' : 'text-gray-500'}`}>Standard View</span>
                                <button
                                    onClick={() => setIsMachian(!isMachian)}
                                    className={`w-14 h-8 rounded-full p-1 transition-colors duration-300 ${isMachian ? 'bg-purple-600' : 'bg-gray-600'}`}
                                >
                                    <div className={`w-6 h-6 rounded-full bg-white transition-transform duration-300 ${isMachian ? 'translate-x-6' : ''}`} />
                                </button>
                                <span className={`text-sm ${isMachian ? 'text-purple-400 font-bold' : 'text-gray-500'}`}>Machian View</span>
                            </div>
                        </div>

                        <div className="relative border border-white/10 rounded-lg overflow-hidden bg-black">
                            <canvas
                                ref={canvasRef}
                                width={800}
                                height={400}
                                className="w-full h-[400px]"
                            />
                        </div>
                    </div>

                    <div className="bg-purple-900/20 border-l-4 border-purple-500 p-4">
                        <p className="text-sm text-purple-200">
                            <strong>The "Aha!" Moment:</strong> In the Machian view, particle masses were lower in the past.
                            Lighter electrons emit less energetic photons.
                            So, looking back in time is like looking at a dimmer bulb.
                            The Supernovae aren't "accelerating away"—they are just physically dimmer than we thought!
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 3: The Math */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. Breaking the Law</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        In standard physics, there is a strict law called the <strong>Etherington Reciprocity Theorem</strong>:
                    </p>
                    <div className="bg-black/30 p-6 rounded-lg border border-white/10 text-center">
                        <Latex>{`$D_L = (1+z)^2 D_A$`}</Latex>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        This says Luminosity Distance (<Latex>{'$D_L$'}</Latex>) and Angular Diameter Distance (<Latex>{'$D_A$'}</Latex>) are locked together.
                        But in the Machian Universe, mass evolution breaks this link:
                    </p>
                    <div className="bg-black/30 p-6 rounded-lg border border-white/10 text-center">
                        <Latex>{`$D_L = (1+z)^2 D_A \\times (1+z)^{\\alpha/2}$`}</Latex>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        That extra factor <Latex>{`$(1+z)^{\\alpha/2}$`}</Latex> is the "Fog."
                        It allows us to fit the Supernova data (which measures <Latex>{'$D_L$'}</Latex>) without messing up the CMB data (which measures <Latex>{'$D_A$'}</Latex>).
                        This is how we solve the Hubble Tension.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Lesson2_3;
