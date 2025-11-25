import { useState, useEffect, useRef } from 'react';
import Latex from '../components/Latex';

const Lesson4_2 = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [cycleCount, setCycleCount] = useState(0);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;
        let t = 0;

        const draw = () => {
            t += 1;
            const width = canvas.width;
            const height = canvas.height;
            const cy = height / 2;

            // Clear
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, width, height);

            // Draw Grid
            ctx.strokeStyle = '#222';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, cy);
            ctx.lineTo(width, cy);
            ctx.stroke();

            // Draw The Cycle (Mass vs Time)
            // We simulate the "Machian Potential" V(phi) = 1/phi^3 + phi^2
            // This creates a bounce.
            // Let's just draw a nice cyclic curve.
            // Mass m(t) ~ |sin(t)| + epsilon

            ctx.strokeStyle = '#a855f7';
            ctx.lineWidth = 3;
            ctx.beginPath();

            const period = 200;
            const amplitude = 100;

            // Draw the full history curve
            for (let x = 0; x < width; x++) {
                // Map x to time relative to current t
                // We want the curve to scroll left
                const timeX = t + (x - width / 2);

                // Cyclic function with a "Bounce" (sharp turn at bottom)
                // Use a cycloid-like shape or just abs(sin)
                const phase = timeX / period;
                const yVal = Math.abs(Math.sin(phase * Math.PI));
                // Add "singularity avoidance" (epsilon)
                const m = yVal * amplitude + 10;

                const y = height - m - 50; // Invert so high mass is up? 
                // Actually, in Machian, Big Bang is Low Mass (m->0).
                // So let's put Low Mass at the bottom.

                if (x === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();

            // Draw "Current Time" Marker
            const cx = width / 2;
            const cPhase = t / period;
            const cYVal = Math.abs(Math.sin(cPhase * Math.PI));
            const cM = cYVal * amplitude + 10;
            const cyPos = height - cM - 50;

            // Detect Bounce
            // Bounce happens when m is minimal (near 0)
            const isBouncing = cM < 15;

            if (isBouncing) {
                // FLASH! (Big Bang)
                ctx.fillStyle = `rgba(255, 255, 255, ${Math.random()})`;
                ctx.beginPath();
                ctx.arc(cx, cyPos, 20 + Math.random() * 20, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#fff';
                ctx.font = '20px font-bold';
                ctx.textAlign = 'center';
                ctx.fillText("BIG BANG (BOUNCE)", cx, cyPos - 50);

                // Update cycle count roughly once per bounce
                if (Math.floor(t) % period === 0) {
                    setCycleCount(c => c + 1);
                }
            } else {
                // Normal Evolution
                ctx.fillStyle = '#00f3ff';
                ctx.beginPath();
                ctx.arc(cx, cyPos, 8, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#aaa';
                ctx.font = '12px monospace';
                ctx.textAlign = 'center';
                ctx.fillText("Present Day", cx, cyPos - 20);
            }

            // Labels
            ctx.fillStyle = '#aaa';
            ctx.font = '12px monospace';
            ctx.textAlign = 'left';
            ctx.fillText("Mass of Universe", 10, 20);
            ctx.textAlign = 'right';
            ctx.fillText("Time ->", width - 10, cy + 20);

            animationFrameId = requestAnimationFrame(draw);
        };

        draw();
        return () => cancelAnimationFrame(animationFrameId);
    }, []);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 4</span>
                    <span>/</span>
                    <span>LESSON 4.2</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-purple-400">
                    The Eternal Bounce
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    The universe didn't begin, and it won't end. It breathes.
                </p>
            </header>

            {/* Section 1: The Phoenix */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Phoenix</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Standard cosmology says the universe began with a Singularity (Big Bang) and will end in a Heat Death (Big Freeze).
                        It's a one-way trip to nothingness.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        The Isothermal Machian Universe is different. Because mass evolves, the universe undergoes <strong>Cycles</strong>.
                        Like a Phoenix, it burns up and is reborn from its own ashes.
                    </p>
                </div>
            </section>

            {/* Section 2: The Simulation */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. The Heartbeat of Eternity</h2>
                <div className="glass-panel p-8 space-y-6">
                    <div className="relative border border-white/10 rounded-lg overflow-hidden bg-black">
                        <canvas
                            ref={canvasRef}
                            width={800}
                            height={400}
                            className="w-full h-[400px]"
                        />
                    </div>

                    <div className="flex justify-center">
                        <div className="bg-purple-900/30 px-6 py-2 rounded-full border border-purple-500/50 text-purple-300 font-mono">
                            Cycles Observed: {cycleCount}
                        </div>
                    </div>

                    <div className="bg-purple-900/20 border-l-4 border-purple-500 p-4">
                        <p className="text-sm text-purple-200">
                            <strong>The Bounce:</strong> When the mass of the universe drops near zero, the "Vacuum Energy" drives a rapid expansion (Inflation).
                            Then, the mass starts to grow again.
                            <br /><br />
                            <strong>The Clean Slate:</strong> At the bounce, <Latex>{`$m \\to 0$`}</Latex>. Particles lose their mass and identity.
                            This wipes the "memory" (Entropy) of the previous universe, giving us a fresh start every time.
                        </p>
                    </div>
                </div>
            </section>

            {/* Conclusion */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">Conclusion</h2>
                <div className="glass-panel p-8 space-y-6 bg-gradient-to-br from-white/5 to-accent-cyan/5">
                    <p className="text-xl text-white font-bold">
                        You have completed the course.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        We started with a simple idea: <strong>"What if the ruler is shrinking?"</strong>
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        From this single seed (Scale Invariance), we derived:
                    </p>
                    <ul className="list-disc list-inside space-y-2 text-gray-300 ml-4">
                        <li>Why the universe <em>looks</em> like it's expanding (Redshift).</li>
                        <li>Why galaxies spin too fast (Modified Inertia).</li>
                        <li>Why Supernovae look too dim (Etherington Violation).</li>
                        <li>Why Black Holes preserve information (Holography).</li>
                        <li>Why the universe exists at all (Cyclic Cosmology).</li>
                    </ul>
                    <p className="text-gray-300 leading-relaxed mt-4">
                        Welcome to the Isothermal Machian Universe.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Lesson4_2;
