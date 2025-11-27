import { useState, useEffect, useRef } from 'react';

const Lesson4_1 = () => {
    const [view, setView] = useState<'standard' | 'machian'>('standard');
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Animation constants
    const HORIZON_RADIUS = 60;
    const ACCRETION_RADIUS = 140;
    const GRAVITY = 0.008; // Extremely slow for cinematic feel
    const START_Y = -50;

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;

        // Animation State
        let astroY = START_Y;
        let astroVel = 0;
        let astroOpacity = 1;
        let astroScaleX = 1;
        let astroScaleY = 1;
        let phase = 'falling'; // falling, frozen, resetting
        let freezeTimer = 0;

        // Starfield (static)
        const stars = Array.from({ length: 100 }).map(() => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 1.5,
            opacity: Math.random()
        }));

        const reset = () => {
            astroY = START_Y;
            astroVel = 0;
            astroOpacity = 1;
            astroScaleX = 1;
            astroScaleY = 1;
            phase = 'falling';
            freezeTimer = 0;
        };

        const drawStars = () => {
            ctx.fillStyle = '#fff';
            stars.forEach(star => {
                ctx.globalAlpha = star.opacity;
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
                ctx.fill();
            });
            ctx.globalAlpha = 1;
        };

        const drawBlackHole = (cx: number, cy: number) => {
            // 1. Accretion Disk (Back)
            ctx.save();
            ctx.translate(cx, cy);
            ctx.scale(1, 0.3);

            const diskGradient = ctx.createRadialGradient(0, 0, HORIZON_RADIUS, 0, 0, ACCRETION_RADIUS);
            diskGradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
            diskGradient.addColorStop(0.4, 'rgba(147, 51, 234, 0.2)');
            diskGradient.addColorStop(0.7, 'rgba(59, 130, 246, 0.6)');
            diskGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

            ctx.fillStyle = diskGradient;
            ctx.beginPath();
            ctx.arc(0, 0, ACCRETION_RADIUS, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // 2. Event Horizon
            ctx.shadowBlur = 20;
            ctx.shadowColor = '#3b82f6';
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(cx, cy, HORIZON_RADIUS, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;

            // 3. Photon Ring
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.globalAlpha = 0.5;
            ctx.beginPath();
            ctx.arc(cx, cy, HORIZON_RADIUS + 2, 0, Math.PI * 2);
            ctx.stroke();
            ctx.globalAlpha = 1;
        };

        const drawAstronaut = (cx: number) => {
            if (astroOpacity <= 0) return;

            ctx.save();
            ctx.translate(cx, astroY);
            ctx.scale(astroScaleX, astroScaleY);
            ctx.globalAlpha = astroOpacity;

            const isHologram = phase === 'frozen';

            if (isHologram) {
                // Hologram Mode: Draw as a single unified "Data Strip"
                ctx.shadowBlur = 10;
                ctx.shadowColor = '#06b6d4';
                ctx.fillStyle = '#06b6d4';

                ctx.beginPath();
                ctx.rect(-8, -18, 16, 36);
                ctx.fill();
            } else {
                // Standard Mode: Detailed Astronaut

                // Body
                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.rect(-6, -10, 12, 20);
                ctx.fill();

                // Head
                ctx.beginPath();
                ctx.arc(0, -14, 8, 0, Math.PI * 2);
                ctx.fill();

                // Backpack
                ctx.fillStyle = '#ccc';
                ctx.beginPath();
                ctx.rect(-10, -12, 4, 16);
                ctx.fill();

                // Visor
                ctx.fillStyle = '#111';
                ctx.beginPath();
                ctx.ellipse(2, -14, 4, 3, 0, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.restore();
        };

        const update = () => {
            const width = canvas.width;
            const height = canvas.height;
            const cx = width / 2;
            const cy = height / 2;
            const horizonTop = cy - HORIZON_RADIUS;

            // Clear
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, width, height);

            drawStars();
            drawBlackHole(cx, cy);

            // Physics & Logic
            if (phase === 'falling') {
                astroVel += GRAVITY;

                // Cap max velocity
                if (astroVel > 1.5) astroVel = 1.5;

                // Machian Time Dilation: Slow down as we approach horizon
                if (view === 'machian') {
                    const distToHorizon = horizonTop - astroY;
                    if (distToHorizon < 150 && distToHorizon > 0) {
                        // Stronger braking as we get closer
                        const drag = 0.92 + (distToHorizon / 2000);
                        astroVel *= drag;
                    }
                }

                astroY += astroVel;

                // Check collision/crossing
                if (view === 'standard') {
                    // Standard: Fall INTO the hole (towards center)
                    if (astroY > horizonTop) {
                        // Position-based fading: Fully transparent after falling 60px past horizon
                        const depth = astroY - horizonTop;
                        astroOpacity = Math.max(0, 1 - depth / 60);

                        // Spaghettification
                        astroScaleY = 1 + depth / 100;
                        astroScaleX = Math.max(0.1, 1 - depth / 100);
                    }

                    if (astroOpacity <= 0) {
                        phase = 'resetting';
                        freezeTimer = 60;
                    }
                } else {
                    // Machian: Hit surface and freeze
                    if (astroY >= horizonTop - 0.5) {
                        astroY = horizonTop;
                        astroVel = 0;
                        phase = 'frozen';
                    }
                }
            } else if (phase === 'frozen') {
                // Machian Holographic Effect
                freezeTimer++;

                // Flatten onto the surface
                if (astroScaleY > 0.1) astroScaleY *= 0.9;

                // Spread out (become data)
                if (astroScaleX < 4) astroScaleX += 0.05; // Slower spread

                // Reset after a while
                if (freezeTimer > 180) { // Longer freeze time
                    astroOpacity -= 0.02;
                    if (astroOpacity <= 0) {
                        phase = 'resetting';
                        freezeTimer = 30;
                    }
                }
            } else if (phase === 'resetting') {
                freezeTimer--;
                if (freezeTimer <= 0) {
                    reset();
                }
            }

            drawAstronaut(cx);

            // Draw Label
            ctx.fillStyle = '#fff';
            ctx.font = '16px "Courier New", monospace';
            ctx.textAlign = 'center';
            const labelY = height - 40;

            if (view === 'standard') {
                ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
                ctx.fillText("STATUS: SUBJECT LOST (SPAGHETTIFICATION)", cx, labelY);
            } else {
                ctx.fillStyle = '#06b6d4';
                ctx.shadowBlur = 10;
                ctx.shadowColor = '#06b6d4';
                if (phase === 'frozen') {
                    ctx.fillText("STATUS: DATA ENCODED ON HORIZON", cx, labelY);
                } else {
                    ctx.fillText("STATUS: APPROACHING HORIZON...", cx, labelY);
                }
                ctx.shadowBlur = 0;
            }

            animationFrameId = requestAnimationFrame(update);
        };

        // Start
        update();

        return () => cancelAnimationFrame(animationFrameId);
    }, [view, START_Y]);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 4</span>
                    <span>/</span>
                    <span>LESSON 4.1</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-purple-400">
                    The Solid Hole
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    Why Black Holes aren't holes at all. They are the hard drives of the universe.
                </p>
            </header>

            {/* Section 1: The Paradox */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Information Paradox</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Stephen Hawking famously asked: <em>"If you throw a book into a Black Hole, is the information lost forever?"</em>
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        In standard General Relativity, the book crosses the Event Horizon and is crushed into a <strong>Singularity</strong> (a point of infinite density where physics breaks down). The information is gone.
                        This breaks the laws of Quantum Mechanics (Unitarity).
                    </p>
                </div>
            </section>

            {/* Section 2: The Solution */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. The Frozen Lake</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        In the Isothermal Machian Universe, the Event Horizon is not a point of no return. It is a <strong>Phase Transition</strong>.
                        Think of it like water freezing into ice.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        As you approach the horizon, the "Mass Scale" of the universe diverges. Time dilation becomes infinite.
                        To an outside observer, you don't fall in. You <strong>freeze</strong> on the surface.
                        Your 3D body becomes a 2D image on the horizon. This is the <strong>Holographic Principle</strong>.
                    </p>

                    <div className="flex flex-col items-center gap-6 p-6 bg-black/40 rounded-xl border border-white/10">
                        {/* Controls */}
                        <div className="flex gap-4">
                            <button
                                onClick={() => setView('standard')}
                                className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 border ${view === 'standard'
                                    ? 'bg-blue-600/20 border-blue-500 text-blue-200 shadow-[0_0_20px_rgba(37,99,235,0.3)]'
                                    : 'bg-white/5 border-transparent text-gray-400 hover:bg-white/10'
                                    }`}
                            >
                                Standard View (The Pit)
                            </button>
                            <button
                                onClick={() => setView('machian')}
                                className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 border ${view === 'machian'
                                    ? 'bg-cyan-600/20 border-cyan-500 text-cyan-200 shadow-[0_0_20px_rgba(6,182,212,0.3)]'
                                    : 'bg-white/5 border-transparent text-gray-400 hover:bg-white/10'
                                    }`}
                            >
                                Machian View (The Hard Drive)
                            </button>
                        </div>

                        {/* Canvas Container */}
                        <div className="relative w-full aspect-[2/1] bg-black rounded-lg overflow-hidden border border-white/10 shadow-2xl">
                            <canvas
                                ref={canvasRef}
                                width={800}
                                height={400}
                                className="w-full h-full object-contain"
                            />
                            {/* Overlay Gradient for depth */}
                            <div className="absolute inset-0 pointer-events-none bg-gradient-to-t from-black/50 via-transparent to-transparent"></div>
                        </div>

                        {/* Explanation Box */}
                        <div className={`w-full p-4 rounded-lg border transition-colors duration-500 ${view === 'standard'
                            ? 'bg-blue-900/10 border-blue-500/30'
                            : 'bg-cyan-900/10 border-cyan-500/30'
                            }`}>
                            <p className={`text-sm ${view === 'standard' ? 'text-blue-200' : 'text-cyan-200'}`}>
                                {view === 'standard'
                                    ? "In the Standard Model, the astronaut crosses the horizon without noticing anything special, but is eventually destroyed by tidal forces (spaghettification) near the singularity."
                                    : "In the Machian Model, the horizon is a physical surface. The astronaut hits it and spreads out, their information becoming encoded in the surface fluctuations (Holographic Principle)."
                                }
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Lesson4_1;
