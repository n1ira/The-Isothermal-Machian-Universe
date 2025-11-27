import { useEffect, useRef } from 'react';
import Latex from '../components/Latex';

const Lesson3_1 = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Physics Constants
    // In Machian Universe, GWs decay as 1/r * (1+z)
    // EM waves decay as 1/r
    // Actually, Paper C says D_L_GW = D_L_EM / (1+z).
    // Luminosity Distance D_L is related to Flux F by F = L / (4*pi*D_L^2).
    // So if D_L_GW is SMALLER, the Flux is HIGHER (Brighter).
    // So GWs are BRIGHTER than Light at high redshift.

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;
        let t = 0;

        const draw = () => {
            t += 0.5;
            const width = canvas.width;
            const height = canvas.height;
            const cy = height / 2;
            const sourceX = 100;

            // Clear
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, width, height);

            // Draw Source (Black Hole Merger)
            ctx.fillStyle = '#fff';
            ctx.beginPath();
            ctx.arc(sourceX, cy, 10, 0, Math.PI * 2);
            ctx.fill();

            // Draw Spiral Effect
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.beginPath();
            const spiralR = 20 + Math.sin(t * 0.1) * 5;
            ctx.arc(sourceX, cy, spiralR, t * 0.2, t * 0.2 + Math.PI * 1.5);
            ctx.stroke();

            // Draw Waves
            // We draw "packets" moving to the right
            // Top Half: Light (EM)
            // Bottom Half: Gravity (GW)

            const speed = 2;
            const wavelength = 40;

            // Draw EM Waves (Top)
            ctx.strokeStyle = '#00f3ff'; // Cyan
            ctx.lineWidth = 2;
            ctx.beginPath();
            for (let x = sourceX; x < width; x++) {
                const dist = x - sourceX;
                const phase = (dist - t * speed) / wavelength;

                // Amplitude decays as 1/r
                const amp = 30 * (100 / (dist + 100));

                const y = cy - 80 + Math.sin(phase * Math.PI * 2) * amp;
                if (x === sourceX) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();

            // Label EM
            ctx.fillStyle = '#00f3ff';
            ctx.font = '12px monospace';
            ctx.fillText('ELECTROMAGNETIC WAVE (LIGHT)', sourceX, cy - 130);
            ctx.fillText('Decays as 1/r', width - 100, cy - 130);

            // Draw GW Waves (Bottom)
            ctx.strokeStyle = '#a855f7'; // Purple
            ctx.lineWidth = 2;
            ctx.beginPath();
            for (let x = sourceX; x < width; x++) {
                const dist = x - sourceX;
                const phase = (dist - t * speed) / wavelength;

                // Redshift z increases with distance
                const z = dist / 400;

                // Machian Amplitude:
                // D_L_GW = D_L_EM / (1+z)
                // Flux ~ 1/D_L^2 ~ (1+z)^2 / D_L_EM^2
                // Amplitude ~ sqrt(Flux) ~ (1+z) / D_L_EM
                // So Amplitude decays as (1+z)/r
                // It decays SLOWER than 1/r. It stays stronger.

                const amp = 30 * (100 / (dist + 100)) * (1 + z);

                const y = cy + 80 + Math.sin(phase * Math.PI * 2) * amp;
                if (x === sourceX) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();

            // Label GW
            ctx.fillStyle = '#a855f7';
            ctx.fillText('GRAVITATIONAL WAVE (GRAVITY)', sourceX, cy + 140);
            ctx.fillText('Decays as (1+z)/r', width - 120, cy + 140);
            ctx.fillText('(Anti-Friction)', width - 120, cy + 155);

            // Draw Divider
            ctx.strokeStyle = '#333';
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(0, cy);
            ctx.lineTo(width, cy);
            ctx.stroke();
            ctx.setLineDash([]);

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
                    <span>MODULE 3</span>
                    <span>/</span>
                    <span>LESSON 3.1</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-purple-400">
                    The Smoking Gun
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    How to prove the theory wrong using the ripples of spacetime itself.
                </p>
            </header>

            {/* Section 1: The Submarine Analogy */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Submarine</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Imagine a submarine deep underwater. It turns on a bright light and bangs a drum.
                    </p>
                    <ul className="list-disc list-inside space-y-2 text-gray-300 ml-4">
                        <li>The <strong>Light</strong> travels through the water, but it gets absorbed and scattered quickly. It struggles to travel.</li>
                        <li>The <strong>Sound</strong> (Sonar) travels through the water incredibly well. It can be heard for hundreds of miles.</li>
                    </ul>
                    <p className="text-gray-300 leading-relaxed">
                        In the Isothermal Machian Universe, something similar happens to Gravity.
                        Because the "Mass Scale" of the universe is changing, the "medium" of spacetime feels different to Light vs. Gravity.
                    </p>
                </div>
            </section>

            {/* Section 2: The Simulation */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. Anti-Friction</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Standard Einstein Gravity says Light and Gravity should fade away at the exact same rate (<Latex>{'$1/r$'}</Latex>).
                        <br />
                        But in our theory, Gravity experiences <strong>Anti-Friction</strong>. It gets a boost from the evolving mass scale.
                    </p>

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
                            <strong>The Prediction:</strong> If we look at a distant Black Hole merger with <strong>LISA</strong> (Laser Interferometer Space Antenna, a future space-based gravity detector), it should appear <strong>brighter</strong> (closer) than the galaxy it lives in.
                            <br />
                            Specifically: <Latex>{`$D_L^{GW} = \\frac{D_L^{EM}}{1+z}$`}</Latex>.
                            <br />
                            (Where <Latex>{`$D_L^{GW}$`}</Latex> is the distance measured by Gravity, and <Latex>{`$D_L^{EM}$`}</Latex> is the distance measured by Light)
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 3: The Kill Shot */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. The Kill Shot</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        This is what we call a "Kill Shot" prediction. Most modified gravity theories try to hide their differences.
                        The Isothermal Machian Universe screams its difference here.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        If LISA launches in 2035 and finds that Gravity and Light fade at the same rate, <strong>this theory is dead</strong>.
                        But if it finds this specific deviation, it will be the first evidence that the fundamental constants of nature are evolving.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Lesson3_1;
