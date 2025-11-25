import { useEffect, useRef } from 'react';
import Latex from '../components/Latex';

const Lesson1_3 = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const particles: { x: number; y: number; vx: number; vy: number; type: 'normal' | 'dark' }[] = [];
        const numParticles = 100;

        // Initialize particles
        for (let i = 0; i < numParticles; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                type: Math.random() > 0.5 ? 'normal' : 'dark'
            });
        }

        const animate = () => {
            if (!canvas || !ctx) return;
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            particles.forEach(p => {
                // Update position
                p.x += p.vx;
                p.y += p.vy;

                // Bounce off walls
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

                // Draw
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.type === 'normal' ? 3 : 4, 0, Math.PI * 2);

                if (p.type === 'normal') {
                    ctx.fillStyle = '#00f3ff'; // Cyan for normal matter
                    ctx.shadowBlur = 5;
                    ctx.shadowColor = '#00f3ff';
                } else {
                    ctx.fillStyle = '#ff00ff'; // Pink for "Dark Matter" (Scalar Field)
                    ctx.shadowBlur = 0; // Dark matter doesn't glow the same way? Or maybe it does in our viz
                    ctx.shadowColor = 'transparent';
                }
                ctx.fill();

                // Interaction: "Dark" particles clump (Mimetic behavior simulation - simplified)
                // In a real simulation, we'd use gravity. Here, let's just make them attracted to the center slightly
                if (p.type === 'dark') {
                    const dx = canvas.width / 2 - p.x;
                    const dy = canvas.height / 2 - p.y;
                    p.vx += dx * 0.0001;
                    p.vy += dy * 0.0001;
                    // Damping (Mimetic constraint c_s = 0 implies it's "dust", so it loses random velocity)
                    p.vx *= 0.99;
                    p.vy *= 0.99;
                }
            });

            requestAnimationFrame(animate);
        };

        animate();
    }, []);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 1</span>
                    <span>/</span>
                    <span>LESSON 1.3</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    The Ghost in the Machine
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    We can't find Dark Matter particles. Maybe that's because they aren't particles at all.
                    They are the shadow of the scalar field.
                </p>
            </header>

            {/* Section 1: The Problem */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Missing Mass</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        When we look at the universe, we see that galaxies spin too fast and light bends too much.
                        It's as if there is <strong>5 times more mass</strong> than we can see.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        Scientists call this "Dark Matter" and have spent 40 years looking for the particle (like WIMPs or Axions, which are theoretical ghost-like particles).
                        They haven't found it.
                    </p>
                    <div className="bg-red-500/10 border-l-4 border-red-500 p-4">
                        <p className="text-sm text-red-200">
                            <strong>The IMU Proposal:</strong> Dark Matter is not a new particle. It is a <strong>gravitational effect</strong> caused by the scalar field <Latex>{'$\\phi$'}</Latex>.
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 2: The Shadow Analogy */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. The Shadow Analogy</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="glass-panel p-6 space-y-4">
                        <h3 className="text-xl font-bold text-white">The Object</h3>
                        <p className="text-gray-300">
                            Imagine you are walking in the sun. You have a physical body (Baryonic Matter, like protons and neutrons).
                            You can touch it, and it interacts with light.
                        </p>
                    </div>
                    <div className="glass-panel p-6 space-y-4 border border-accent-pink/30">
                        <h3 className="text-xl font-bold text-accent-pink">The Shadow</h3>
                        <p className="text-gray-300">
                            Attached to you is a shadow. It moves with you. It has a "size" (shape).
                            But you can't touch it. Light passes right through it.
                        </p>
                    </div>
                </div>
                <div className="glass-panel p-8">
                    <p className="text-gray-300 leading-relaxed">
                        In the Isothermal Machian Universe, the scalar field <Latex>{'$\\phi$'}</Latex> is always attached to matter (via the coupling <Latex>{'$m \\propto \\phi$'}</Latex>).
                        But under certain conditions, the field can "clump" on its own, creating a gravitational shadow even where there is no matter.
                    </p>
                </div>
            </section>

            {/* Section 3: Mimetic Gravity Simulation */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. Visualizing the "Ghost"</h2>
                <div className="glass-panel p-4 relative overflow-hidden">
                    <div className="absolute top-4 right-4 z-10 space-y-2 text-right">
                        <div className="flex items-center justify-end gap-2">
                            <span className="text-xs text-accent-cyan font-mono">NORMAL MATTER</span>
                            <div className="w-3 h-3 rounded-full bg-accent-cyan shadow-[0_0_10px_#00f3ff]" />
                        </div>
                        <div className="flex items-center justify-end gap-2">
                            <span className="text-xs text-accent-pink font-mono">SCALAR FIELD (DM)</span>
                            <div className="w-3 h-3 rounded-full bg-accent-pink" />
                        </div>
                    </div>
                    <canvas
                        ref={canvasRef}
                        width={800}
                        height={400}
                        className="w-full h-[400px] bg-black rounded-lg border border-white/5"
                    />
                    <p className="text-xs text-gray-500 mt-2 text-center">
                        Simulation: Normal matter bounces randomly (Pressure). The Scalar Field clumps in the center (Zero Pressure).
                    </p>
                </div>
            </section>

            {/* Section 4: The Mimetic Constraint */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">4. The Mathematics of Dust</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        How do we make a field behave like "dust" (Dark Matter)?
                        We force it to move at the speed of light in the field space, which effectively kills its pressure.
                    </p>
                    <div className="bg-black/40 p-6 rounded-lg border border-white/10 text-center">
                        <Latex>{`$c_s^2 \\to 0$`}</Latex>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        This is called the <strong>Mimetic Constraint</strong>.
                        It forces the scalar field to have zero sound speed (<Latex>{'$c_s = 0$'}</Latex>).
                        A fluid with zero sound speed cannot support pressure waves—it just collapses under gravity.
                        This is exactly how Cold Dark Matter behaves.
                    </p>
                    <div className="bg-white/5 p-4 rounded border-l-4 border-accent-pink">
                        <p className="text-sm text-gray-300">
                            <strong>Result:</strong> We get the <em>behavior</em> of Dark Matter (clumping, lensing) without needing a new particle.
                            It's just the scalar field acting like a "stiff" fluid.
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Lesson1_3;
