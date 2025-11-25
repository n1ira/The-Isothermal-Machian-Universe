import { useEffect, useRef, useState } from 'react';
import Latex from '../components/Latex';

const Lesson1_4 = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [dmHalo, setDmHalo] = useState(0); // 0 to 1
    const [scalarGradient, setScalarGradient] = useState(0); // 0 to 1
    const [activeMode, setActiveMode] = useState<'dm' | 'machian'>('dm');

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = canvas.width;
        const height = canvas.height;
        const padding = 40;

        const draw = () => {
            // Clear
            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, width, height);

            // Draw Axes
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(padding, padding);
            ctx.lineTo(padding, height - padding); // Y axis
            ctx.lineTo(width - padding, height - padding); // X axis
            ctx.stroke();

            // Labels
            ctx.fillStyle = '#666';
            ctx.font = '12px monospace';
            ctx.fillText('Velocity (v)', padding + 10, padding + 10);
            ctx.fillText('Distance (r)', width - 100, height - 20);

            // Plot Function
            const plot = (color: string, fn: (r: number) => number, label: string) => {
                ctx.strokeStyle = color;
                ctx.lineWidth = 3;
                ctx.beginPath();
                let first = true;
                for (let x = 0; x < width - 2 * padding; x += 5) {
                    const r = x / (width - 2 * padding) * 10; // r goes from 0 to 10
                    if (r < 0.1) continue; // Avoid singularity

                    const v = fn(r);

                    // Map to canvas coords
                    // Max v expected is around 2-3
                    const plotX = padding + x;
                    const plotY = (height - padding) - (v / 2.5) * (height - 2 * padding);

                    if (first) {
                        ctx.moveTo(plotX, plotY);
                        first = false;
                    } else {
                        ctx.lineTo(plotX, plotY);
                    }
                }
                ctx.stroke();

                // Legend
                ctx.fillStyle = color;
                ctx.fillText(label, width - 150, padding + (label === 'Newtonian' ? 20 : 40));
            };

            // 1. Newtonian (Baryonic only)
            // v = sqrt(GM/r). Let GM = 1.
            // But we need a disk model, not point mass. 
            // Simple approx: v rises linearly then falls as 1/sqrt(r).
            // Let's use v^2 = M(r)/r. 
            // M(r) = r^3 for r < 1 (solid sphere/disk core), M(r) = 1 for r > 1.
            const vNewton = (r: number) => {
                if (r < 1) return Math.sqrt(r * r); // v ~ r
                return Math.sqrt(1 / r);
            };

            plot('#444', vNewton, 'Newtonian');

            // 2. Modified Curve
            const vModified = (r: number) => {
                let v2_newton = 0;
                if (r < 1) v2_newton = r * r;
                else v2_newton = 1 / r;

                let boost = 1;

                if (activeMode === 'dm') {
                    // Dark Matter Halo: M_halo(r) ~ r (Isothermal sphere)
                    // v^2 = (M_baryon + M_halo) / r
                    // M_halo = c * r^2 (so density ~ 1/r^2, mass ~ r) -> v^2 ~ const
                    // Let's say M_halo(r) = dmHalo * r
                    const v2_halo = dmHalo * 1.5; // Constant contribution
                    // Smooth transition
                    const transition = 1 - Math.exp(-r);
                    boost = (v2_newton + v2_halo * transition) / v2_newton;
                } else {
                    // Machian: Modified Inertia
                    // v^2 = v_newton^2 * (m_grav / m_inertial)
                    // m_inertial ~ r^-alpha
                    // Let alpha = scalarGradient
                    // So boost factor is r^alpha
                    // We clamp r at 1 for the core to avoid divergence
                    const factor = r > 1 ? Math.pow(r, scalarGradient * 0.8) : 1;
                    boost = factor;
                }

                return Math.sqrt(v2_newton * boost);
            };

            plot(activeMode === 'dm' ? '#ff00ff' : '#00f3ff', vModified, activeMode === 'dm' ? 'Dark Matter' : 'Machian Gravity');
        };

        draw();

    }, [dmHalo, scalarGradient, activeMode]);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 1</span>
                    <span>/</span>
                    <span>LESSON 1.4</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    The Galactic Carousel
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    Galaxies are spinning so fast they should tear themselves apart.
                    Is there invisible glue holding them together? Or are the laws of motion wrong?
                </p>
            </header>

            {/* Section 1: The Mystery */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Impossible Spin</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Imagine a merry-go-round. If you spin it too fast, the kids on the edge will fly off.
                        Gravity is the force holding stars in a galaxy. But when we measure the speed of stars, we find a problem:
                    </p>
                    <div className="bg-red-500/10 border-l-4 border-red-500 p-4">
                        <p className="text-sm text-red-200">
                            <strong>The Observation:</strong> Stars on the edge of galaxies are moving just as fast as stars in the center.
                            According to Newton's laws, they should be flying away into deep space.
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 2: The Two Solutions */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. Two Ways to Fix It</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Dark Matter */}
                    <div
                        className={`glass-panel p-6 space-y-4 cursor-pointer transition-all duration-300 ${activeMode === 'dm' ? 'border-accent-pink ring-1 ring-accent-pink' : 'opacity-60 hover:opacity-100'}`}
                        onClick={() => setActiveMode('dm')}
                    >
                        <h3 className="text-xl font-bold text-accent-pink">Option A: Dark Matter</h3>
                        <p className="text-gray-300 text-sm">
                            <strong>"There is more gravity."</strong>
                            <br /><br />
                            We assume there is a huge halo of invisible matter surrounding the galaxy.
                            More mass = More Gravity = Faster spin is possible.
                        </p>
                    </div>

                    {/* Machian */}
                    <div
                        className={`glass-panel p-6 space-y-4 cursor-pointer transition-all duration-300 ${activeMode === 'machian' ? 'border-accent-cyan ring-1 ring-accent-cyan' : 'opacity-60 hover:opacity-100'}`}
                        onClick={() => setActiveMode('machian')}
                    >
                        <h3 className="text-xl font-bold text-accent-cyan">Option B: Machian Gravity</h3>
                        <p className="text-gray-300 text-sm">
                            <strong>"Inertia is different."</strong>
                            <br /><br />
                            We assume the stars are harder to push (heavier inertial mass) as you go further out.
                            Heavier Inertia = Less Centrifugal Force = You don't need as much gravity.
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 3: The Simulation */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. Interactive Simulation</h2>
                <div className="glass-panel p-6 space-y-6">
                    <canvas
                        ref={canvasRef}
                        width={800}
                        height={400}
                        className="w-full h-[400px] bg-black rounded-lg border border-white/5"
                    />

                    <div className="space-y-4">
                        {activeMode === 'dm' ? (
                            <div>
                                <div className="flex justify-between text-sm mb-2">
                                    <span className="text-accent-pink">Dark Matter Halo Mass</span>
                                    <span>{Math.round(dmHalo * 100)}%</span>
                                </div>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={dmHalo}
                                    onChange={(e) => setDmHalo(parseFloat(e.target.value))}
                                    className="w-full accent-accent-pink"
                                />
                                <p className="text-xs text-gray-500 mt-2">
                                    Adding invisible mass keeps the velocity high at large distances.
                                </p>
                            </div>
                        ) : (
                            <div>
                                <div className="flex justify-between text-sm mb-2">
                                    <span className="text-accent-cyan">Scalar Field Gradient (Inertia Boost)</span>
                                    <span>{Math.round(scalarGradient * 100)}%</span>
                                </div>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={scalarGradient}
                                    onChange={(e) => setScalarGradient(parseFloat(e.target.value))}
                                    className="w-full accent-accent-cyan"
                                />
                                <p className="text-xs text-gray-500 mt-2">
                                    Increasing the scalar gradient makes outer stars "heavier" (inertially), so they don't fly off even with weak gravity.
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </section>

            {/* Section 4: The Sticky Floor Analogy */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">4. The Sticky Floor Analogy</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Imagine you are on a merry-go-round. It's spinning fast. You have to hold on tight to the bar so you don't fly off.
                        Usually, the faster it spins, the harder you have to hold on.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        Now, imagine the floor of the merry-go-round gets <strong>stickier</strong> as you go further out.
                        The friction (inertia) holds you in place.
                    </p>
                    <div className="bg-black/30 p-6 rounded-lg border border-white/10 text-center">
                        <Latex>{`$\\frac{G M m_{grav}}{r^2} = \\frac{m_{inertial} v^2}{r}$`}</Latex>
                        <p className="text-xs text-gray-500 mt-2">
                            (Where <Latex>{'$G$'}</Latex> is Gravity, <Latex>{'$M$'}</Latex> is Galaxy Mass, <Latex>{'$v$'}</Latex> is Velocity, <Latex>{'$r$'}</Latex> is Distance)
                        </p>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        In the Machian Universe, the scalar field acts like this "sticky floor".
                        It increases your <strong>Inertial Mass</strong> (<Latex>{'$m_{inertial}$'}</Latex>) as you go further out, making it harder for the centrifugal force to fling you away.
                        <br /><br />
                        Because you are "stickier" (heavier inertia), you don't need as much gravity to hold you in.
                        This explains why stars can orbit so fast without flying off, even without Dark Matter.
                    </p>
                </div>
            </section>

            {/* Section 5: Tully-Fisher */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">5. The Tully-Fisher Relation</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        This model predicts a very specific relationship between the mass of a galaxy and its rotation speed.
                        It's called the Tully-Fisher relation:
                    </p>
                    <div className="bg-accent-cyan/10 p-6 rounded-lg border border-accent-cyan/30 text-center">
                        <Latex>{`$v^4 \\propto M_{baryon}$`}</Latex>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        This relation is observed in nature to be incredibly tight. Dark Matter models struggle to explain why it's so perfect (since DM halos could be any size).
                        In the Machian model, it comes directly from the math of the scalar field.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Lesson1_4;
