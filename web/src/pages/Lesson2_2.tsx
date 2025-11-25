import { useState, useEffect, useRef } from 'react';
import Latex from '../components/Latex';

const Lesson2_2 = () => {
    const [frame, setFrame] = useState<'einstein' | 'machian'>('einstein');
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;
        let time = 0;

        const draw = () => {
            time += 0.005;
            const width = canvas.width;
            const height = canvas.height;

            // Clear
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, width, height);

            // Center
            const cx = width / 2;
            const cy = height / 2;

            // Simulation Parameters
            // We want to show "Expansion" vs "Shrinking"
            // Scale Factor a(t) = 1 + time
            const scaleFactor = 1 + (time % 2); // Loop every 2 units of expansion

            let gridScale = 50;
            let atomSize = 20;
            let galaxyDist = 100;

            if (frame === 'einstein') {
                // Einstein Frame: Space Expands, Atoms Fixed
                gridScale = 50 * scaleFactor;
                galaxyDist = 100 * scaleFactor;
                atomSize = 20; // Fixed
            } else {
                // Machian Frame: Space Static, Atoms Shrink
                // To look identical (conformal), relative ratios must match.
                // Ratio = GalaxyDist / AtomSize
                // Einstein: (100 * a) / 20 = 5a
                // Machian: 100 / (20 / a) = 5a
                gridScale = 50; // Fixed
                galaxyDist = 100; // Fixed
                atomSize = 20 / scaleFactor; // Shrinking
            }

            // Draw Grid
            ctx.strokeStyle = '#222';
            ctx.lineWidth = 1;

            if (frame === 'einstein') {
                // Expanding Grid
                // We just draw lines that move away from center
                ctx.beginPath();
                // Vertical lines
                for (let i = -5; i <= 5; i++) {
                    const x = cx + i * gridScale;
                    ctx.moveTo(x, 0);
                    ctx.lineTo(x, height);
                }
                // Horizontal lines
                for (let i = -5; i <= 5; i++) {
                    const y = cy + i * gridScale;
                    ctx.moveTo(0, y);
                    ctx.lineTo(width, y);
                }
                ctx.stroke();
            } else {
                // Static Grid
                const step = 50;
                ctx.beginPath();
                for (let i = -10; i <= 10; i++) {
                    ctx.moveTo(cx + i * step, 0);
                    ctx.lineTo(cx + i * step, height);
                    ctx.moveTo(0, cy + i * step);
                    ctx.lineTo(width, cy + i * step);
                }
                ctx.stroke();
            }

            // Draw Galaxies
            const drawGalaxy = (x: number, y: number) => {
                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.arc(x, y, 4, 0, Math.PI * 2);
                ctx.fill();
                // Spiral arms hint
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.arc(x, y, 8, 0, Math.PI * 2);
                ctx.stroke();
            };

            // 4 Galaxies moving away from center
            drawGalaxy(cx - galaxyDist, cy - galaxyDist);
            drawGalaxy(cx + galaxyDist, cy - galaxyDist);
            drawGalaxy(cx - galaxyDist, cy + galaxyDist);
            drawGalaxy(cx + galaxyDist, cy + galaxyDist);

            // Draw "The Ruler" (Atom)
            // Draw it in the center for visibility
            ctx.fillStyle = '#00f3ff'; // Cyan
            ctx.beginPath();
            ctx.arc(cx, cy, atomSize, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#000';
            ctx.font = '10px monospace';
            ctx.textAlign = 'center';
            ctx.fillText('ATOM', cx, cy + 3);

            // Draw Light Wave
            const waveY = height - 50;
            ctx.strokeStyle = '#ff0055'; // Pink
            ctx.lineWidth = 2;
            ctx.beginPath();

            let lambda = 20;
            if (frame === 'einstein') {
                lambda = 20 * scaleFactor;
            } else {
                lambda = 20; // Fixed in static space
            }

            for (let x = 0; x < width; x++) {
                const y = waveY + Math.sin(x / lambda * Math.PI * 2) * 10;
                if (x === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();

            ctx.fillStyle = '#ff0055';
            ctx.fillText('PHOTON', width / 2, waveY + 25);

            animationFrameId = requestAnimationFrame(draw);
        };

        draw();

        return () => cancelAnimationFrame(animationFrameId);
    }, [frame]);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 2</span>
                    <span>/</span>
                    <span>LESSON 2.2</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-purple-400">
                    The Magic Trick
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    Cosmic Duality: How to make the universe expand without moving a single inch.
                </p>
            </header>

            {/* Section 1: The Funhouse Mirror */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Funhouse Mirror</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        In the previous lesson, we saw that the "Ruler" (Atom) and the "Table" (Universe) are linked.
                        We can describe the history of the universe in two mathematically equivalent ways (Frames).
                        Neither is "more true" than the other—they are just different coordinate systems.
                    </p>

                    <div className="flex justify-center gap-4 p-4 bg-black/20 rounded-lg">
                        <button
                            onClick={() => setFrame('einstein')}
                            className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 ${frame === 'einstein'
                                ? 'bg-blue-600 text-white shadow-[0_0_20px_rgba(37,99,235,0.4)]'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10'
                                }`}
                        >
                            Einstein Frame (Standard)
                        </button>
                        <button
                            onClick={() => setFrame('machian')}
                            className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 ${frame === 'machian'
                                ? 'bg-purple-600 text-white shadow-[0_0_20px_rgba(147,51,234,0.4)]'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10'
                                }`}
                        >
                            Machian Frame (Static)
                        </button>
                    </div>

                    <div className="relative border border-white/10 rounded-lg overflow-hidden bg-black">
                        <canvas
                            ref={canvasRef}
                            width={800}
                            height={400}
                            className="w-full h-[400px]"
                        />
                        <div className="absolute top-4 left-4 space-y-2">
                            <div className="bg-black/50 backdrop-blur px-3 py-1 rounded border border-white/10 text-xs text-white">
                                <span className="text-gray-400">Space:</span> {frame === 'einstein' ? 'Expanding' : 'Static'}
                            </div>
                            <div className="bg-black/50 backdrop-blur px-3 py-1 rounded border border-white/10 text-xs text-white">
                                <span className="text-gray-400">Atoms:</span> {frame === 'einstein' ? 'Fixed Size' : 'Shrinking'}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Section 2: The Math */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. The Transformation</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        We can transform between these frames using a <strong>Conformal Transformation</strong>.
                        Think of this like changing the projection of a map (e.g., from a Globe to a flat Mercator map).
                        The physical Earth is the same, but the distances on the map look different.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        We change our definition of length by a factor <Latex>{'$\\Omega$'}</Latex> (Omega), which acts as the "Scaling Factor".
                    </p>
                    <div className="bg-black/30 p-6 rounded-lg border border-white/10 text-center">
                        <Latex>{`$\\tilde{g}_{\\mu\\nu} = \\Omega^2 g_{\\mu\\nu}$`}</Latex>
                        <p className="text-xs text-gray-500 mt-2">
                            (Where <Latex>{`$g$`}</Latex> is the Metric Tensor, the mathematical ruler that defines distance. The symbols <Latex>{`$\\mu\\nu$`}</Latex> just mean "in all directions of space and time".)
                        </p>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        In the <strong>Einstein Frame</strong> (<Latex>{'$\\tilde{g}$'}</Latex>), gravity looks standard, but we need "Dark Energy" to push the expansion.
                        <br />
                        In the <strong>Machian Frame</strong> (<Latex>{'$g$'}</Latex>), space is static, but mass evolves.
                    </p>
                    <div className="bg-purple-900/20 border-l-4 border-purple-500 p-4">
                        <p className="text-sm text-purple-200">
                            <strong>Why do this?</strong> Because in the Machian Frame, the physics of the "Dark Sector" becomes visible.
                            What looks like "Dark Energy" in one frame is just the "Mass Evolution" in the other.
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 3: The Advantage */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. Why the Machian Frame wins</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        While the frames are mathematically dual for the <strong>background</strong> (the shape of the universe), they are NOT identical for everything.
                        <br /><br />
                        As we saw in Lesson 2.1, the <strong>Luminosity Distance</strong> breaks the duality.
                        By working in the Machian Frame, we can naturally explain why Supernovae look dimmer (mass evolution) without needing to invent a new "Dark Energy" fluid.
                        We also get the "Dark Matter" effects for free from the scalar field gradients.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Lesson2_2;
