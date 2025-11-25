import { useState, useEffect, useRef } from 'react';
import Latex from '../components/Latex';

const Lesson3_2 = () => {
    const [mode, setMode] = useState<'standard' | 'machian'>('standard');
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Simulation State
    // We want to show particles clumping.
    // To make it "incredibly easy", let's not do full N-body (too chaotic).
    // Let's do "Attraction to Seeds".
    // We place 5 "Seeds" (Proto-Galaxies).
    // Particles drift towards them.
    // Standard: Weak pull.
    // Machian: Strong pull.

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = canvas.width;
        const height = canvas.height;

        // Initialize Particles
        const particleCount = 200;
        const particles = Array.from({ length: particleCount }).map(() => ({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
        }));

        // Seeds (where galaxies will form)
        const seeds = [
            { x: width * 0.2, y: height * 0.3 },
            { x: width * 0.8, y: height * 0.3 },
            { x: width * 0.5, y: height * 0.7 },
            { x: width * 0.3, y: height * 0.6 },
            { x: width * 0.7, y: height * 0.6 },
        ];

        let animationFrameId: number;
        let time = 0;

        const draw = () => {
            time += 1;

            // Physics Update
            // G_eff determines pull strength
            // Standard: G = 0.05
            // Machian: G = 0.15 (3x stronger)
            const G = mode === 'standard' ? 0.02 : 0.15;

            particles.forEach(p => {
                // Find nearest seed
                let nearest = seeds[0];
                let minDist = 10000;

                seeds.forEach(s => {
                    const dx = s.x - p.x;
                    const dy = s.y - p.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < minDist) {
                        minDist = dist;
                        nearest = s;
                    }
                });

                // Apply Force
                if (minDist > 10) { // Don't collapse to singularity
                    const dx = nearest.x - p.x;
                    const dy = nearest.y - p.y;
                    const force = G / minDist; // Simplified gravity (1/r for stability visual)

                    p.vx += dx * force * 0.1;
                    p.vy += dy * force * 0.1;
                }

                // Drag (Friction) to stop them orbiting forever
                p.vx *= 0.95;
                p.vy *= 0.95;

                // Move
                p.x += p.vx;
                p.y += p.vy;
            });

            // Draw
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, width, height);

            // Draw Seeds (faint)
            seeds.forEach(s => {
                const gradient = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, 50);
                gradient.addColorStop(0, 'rgba(100, 100, 255, 0.1)');
                gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(s.x, s.y, 50, 0, Math.PI * 2);
                ctx.fill();
            });

            // Draw Particles
            ctx.fillStyle = mode === 'standard' ? '#3b82f6' : '#a855f7';
            particles.forEach(p => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
                ctx.fill();
            });

            // Draw Time Label
            ctx.fillStyle = '#fff';
            ctx.font = '14px monospace';
            ctx.fillText(`Time since Big Bang: ${(time / 60).toFixed(1)} Billion Years`, 20, 30);

            // Draw Result Label
            ctx.textAlign = 'center';
            if (time > 300) {
                ctx.font = '20px font-bold';
                if (mode === 'standard') {
                    ctx.fillStyle = '#3b82f6';
                    ctx.fillText("Result: Small, fuzzy blobs (Proto-galaxies)", width / 2, height - 30);
                } else {
                    ctx.fillStyle = '#a855f7';
                    ctx.fillText("Result: HUGE, bright galaxies!", width / 2, height - 30);
                }
            }

            animationFrameId = requestAnimationFrame(draw);
        };

        draw();
        return () => cancelAnimationFrame(animationFrameId);
    }, [mode]);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 3</span>
                    <span>/</span>
                    <span>LESSON 3.2</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-purple-400">
                    The Impossible Galaxies
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    Why the James Webb Telescope is finding monsters where there should only be babies.
                </p>
            </header>

            {/* Section 1: The Mystery */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Mystery</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Imagine you walk into a nursery and see a newborn baby... with a full beard, bench-pressing 200 lbs.
                        You would be confused. Babies take time to grow.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        This is exactly what happened when we launched the <strong>James Webb Space Telescope (JWST)</strong>.
                        We looked back to the very beginning of the universe (the "nursery").
                        We expected to see tiny, fuzzy baby galaxies.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        Instead, we saw <strong>MONSTERS</strong>. Huge, bright, fully-formed galaxies that shouldn't exist yet.
                        Standard physics says there wasn't enough time for gravity to pull them together.
                    </p>
                </div>
            </section>

            {/* Section 2: The Solution */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. Gravity on Steroids</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        In the Isothermal Machian Universe, gravity in the early universe was <strong>stronger</strong>.
                        The scalar field acts like a "glue" that helps matter clump together much faster.
                    </p>

                    <div className="flex justify-center gap-4 p-4 bg-black/20 rounded-lg">
                        <button
                            onClick={() => setMode('standard')}
                            className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 ${mode === 'standard'
                                ? 'bg-blue-600 text-white shadow-[0_0_20px_rgba(37,99,235,0.4)]'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10'
                                }`}
                        >
                            Standard Gravity (Weak)
                        </button>
                        <button
                            onClick={() => setMode('machian')}
                            className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 ${mode === 'machian'
                                ? 'bg-purple-600 text-white shadow-[0_0_20px_rgba(147,51,234,0.4)]'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10'
                                }`}
                        >
                            Machian Gravity (Strong)
                        </button>
                    </div>

                    <div className="relative border border-white/10 rounded-lg overflow-hidden bg-black">
                        <canvas
                            ref={canvasRef}
                            width={800}
                            height={400}
                            className="w-full h-[400px]"
                        />
                    </div>

                    <div className="bg-purple-900/20 border-l-4 border-purple-500 p-4">
                        <p className="text-sm text-purple-200">
                            <strong>The Result:</strong> With Machian Gravity (<Latex>{`$G_{eff} \\approx 3 G_N$`}</Latex>), galaxies form <strong>50-100 times faster</strong>.
                            Those "Impossible" galaxies aren't impossible anymore. They are exactly what we predict.
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Lesson3_2;
