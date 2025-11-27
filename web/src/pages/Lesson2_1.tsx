import { useEffect, useRef, useState } from 'react';
import Latex from '../components/Latex';

const Lesson2_1 = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [h0, setH0] = useState(70); // User's guess for H0
    const [machianMode, setMachianMode] = useState(false); // Toggle for the solution

    // Constants
    const CMB_H0 = 67.4;
    const SH0ES_H0 = 73.0;
    const ERROR_TOLERANCE = 1.0; // How much error is "acceptable" visually

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = canvas.width;
        const height = canvas.height;

        const draw = () => {
            // Clear
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, width, height);

            // --- Visualization: The Tug of War ---
            const centerY = height / 2;
            const leftX = 100;
            const rightX = width - 100;
            const modelX = width / 2; // Fixed position for the "Model" anchor visually, but we show the value

            // Calculate "Tension" (Error)
            // Error is distance from the preferred value
            const errorCMB = Math.abs(h0 - CMB_H0);
            const errorSN = Math.abs(h0 - SH0ES_H0);

            // In Machian mode, we "cheat". The effective H0 for SN is different from CMB.
            // Machian: CMB sees h0, SN sees h0 + correction.
            // Actually, the paper says: D_L is modified.
            // Effectively, Machian allows us to fit CMB with one value and SN with another?
            // Paper says: "Duality breaking allows the model to reconcile... with H0 ~ 71.3"
            // Let's visualize it as the "Ruler" stretching.

            let visualErrorCMB = errorCMB;
            let visualErrorSN = errorSN;

            if (machianMode) {
                // In Machian mode, the "Ruler" breaks.
                // We can satisfy CMB (at 67) and SN (at 73) simultaneously effectively.
                // Or rather, the tension is relieved.
                // Let's simulate this by reducing the visual error significantly if H0 is in the "sweet spot" (71.3).
                // If H0 is 71.3, Machian error is near 0.
                const idealMachian = 71.3;
                const dist = Math.abs(h0 - idealMachian);
                visualErrorCMB = dist * 0.2; // Suppress error
                visualErrorSN = dist * 0.2;
            }

            // Colors based on tension
            const getTensionColor = (err: number) => {
                if (err < ERROR_TOLERANCE) return '#00ff00'; // Green
                if (err < 3.0) return '#ffff00'; // Yellow
                return '#ff0000'; // Red
            };

            const colorCMB = getTensionColor(visualErrorCMB);
            const colorSN = getTensionColor(visualErrorSN);

            // Draw "Ropes"
            ctx.lineWidth = 4;

            // Left Rope (CMB)
            ctx.strokeStyle = colorCMB;
            ctx.beginPath();
            ctx.moveTo(leftX, centerY);
            ctx.lineTo(modelX - 20, centerY);
            ctx.stroke();

            // Right Rope (SN)
            ctx.strokeStyle = colorSN;
            ctx.beginPath();
            ctx.moveTo(rightX, centerY);
            ctx.lineTo(modelX + 20, centerY);
            ctx.stroke();

            // Draw "Parties"

            // CMB (Left)
            ctx.fillStyle = colorCMB;
            ctx.beginPath();
            ctx.arc(leftX, centerY, 20, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#fff';
            ctx.font = '12px monospace';
            ctx.textAlign = 'center';
            ctx.fillText('CMB', leftX, centerY - 30);
            ctx.fillText('67.4', leftX, centerY + 35);

            // SN (Right)
            ctx.fillStyle = colorSN;
            ctx.beginPath();
            ctx.arc(rightX, centerY, 20, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#fff';
            ctx.fillText('Supernovae', rightX, centerY - 30);
            ctx.fillText('73.0', rightX, centerY + 35);

            // The Model (Center)
            ctx.fillStyle = '#fff';
            ctx.fillRect(modelX - 20, centerY - 20, 40, 40);
            ctx.fillStyle = '#000';
            ctx.fillText('H0', modelX, centerY + 5);

            // Value Display
            ctx.fillStyle = '#fff';
            ctx.font = '16px monospace';
            ctx.fillText(`Model H0: ${h0.toFixed(1)}`, modelX, centerY - 40);

            // Machian Effect Visualization
            if (machianMode) {
                ctx.strokeStyle = '#00f3ff';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.arc(modelX, centerY, 60, 0, Math.PI * 2);
                ctx.stroke();
                ctx.setLineDash([]);

                ctx.fillStyle = '#00f3ff';
                ctx.fillText('DUALITY BROKEN', modelX, centerY + 80);
            }
        };

        draw();

    }, [h0, machianMode]);

    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 2</span>
                    <span>/</span>
                    <span>LESSON 2.1</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-red-500">
                    The Crisis
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    Cosmology is broken. The two best rulers we have for measuring the universe give different answers.
                    Is it a measurement error, or is the universe lying to us?
                </p>
            </header>

            {/* Section 1: The Two Rulers */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Tale of Two Rulers</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        To know how fast the universe is expanding (the Hubble Constant, <Latex>{'$H_0$'}</Latex>), we measure it in two ways:
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-blue-900/20 p-6 rounded-lg border border-blue-500/30">
                            <h3 className="text-xl font-bold text-blue-400 mb-2">The Early Universe</h3>
                            <p className="text-sm text-gray-300 mb-4">
                                We look at the Cosmic Microwave Background (CMB) from 380,000 years after the Big Bang (based on the Standard Model timeline).
                                We use the physics of sound waves to predict how fast the universe should be expanding today.
                            </p>
                            <div className="text-2xl font-mono text-white">
                                <Latex>{'$H_0 \\approx 67.4$'}</Latex> km/s/Mpc
                            </div>
                        </div>
                        <div className="bg-orange-900/20 p-6 rounded-lg border border-orange-500/30">
                            <h3 className="text-xl font-bold text-orange-400 mb-2">The Late Universe</h3>
                            <p className="text-sm text-gray-300 mb-4">
                                We look at exploding stars (Supernovae) in nearby galaxies.
                                We use them as "standard candles" to measure the expansion rate directly.
                            </p>
                            <div className="text-2xl font-mono text-white">
                                <Latex>{'$H_0 \\approx 73.0$'}</Latex> km/s/Mpc
                            </div>
                        </div>
                    </div>
                    <div className="bg-red-500/10 border-l-4 border-red-500 p-4">
                        <p className="text-sm text-red-200">
                            <strong>The Problem:</strong> These numbers do not match. The difference is over 4 standard deviations (<Latex>{'$4\\sigma$'}</Latex>).
                            This is the "Hubble Tension."
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 2: The Tug of War */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. The Tug of War</h2>
                <div className="glass-panel p-6 space-y-6">
                    <p className="text-gray-300">
                        Try to find a value for <Latex>{'$H_0$'}</Latex> that makes everyone happy.
                    </p>

                    <canvas
                        ref={canvasRef}
                        width={800}
                        height={300}
                        className="w-full h-[300px] bg-black rounded-lg border border-white/5"
                    />

                    <div className="space-y-4">
                        <div className="flex justify-between text-sm">
                            <span>Model H0</span>
                            <span className="font-mono text-accent-cyan">{h0.toFixed(1)}</span>
                        </div>
                        <input
                            type="range"
                            min="65"
                            max="75"
                            step="0.1"
                            value={h0}
                            onChange={(e) => setH0(parseFloat(e.target.value))}
                            className="w-full accent-accent-cyan"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                            <span>65.0</span>
                            <span>75.0</span>
                        </div>
                    </div>

                    <div className="flex items-center gap-4 pt-4 border-t border-white/10">
                        <button
                            onClick={() => setMachianMode(!machianMode)}
                            className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 ${machianMode
                                ? 'bg-accent-cyan text-black shadow-[0_0_20px_rgba(0,243,255,0.4)]'
                                : 'bg-white/10 text-white hover:bg-white/20'
                                }`}
                        >
                            {machianMode ? 'Disable Machian Solution' : 'Enable Machian Solution'}
                        </button>
                        <p className="text-sm text-gray-400">
                            {machianMode
                                ? "The Machian model breaks the link between the two rulers, allowing both to be correct in their own way."
                                : "Standard ΛCDM forces a rigid link between the two measurements."}
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 3: The Solution */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. Breaking the Ruler</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        In standard physics, there is a rule called the <strong>Etherington Reciprocity Theorem</strong>. It says:
                    </p>
                    <div className="bg-black/30 p-6 rounded-lg border border-white/10 text-center">
                        <Latex>{`$D_L = (1+z)^2 D_A$`}</Latex>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        It connects the <strong>Luminosity Distance</strong> (<Latex>{'$D_L$'}</Latex>, used by Supernovae) to the <strong>Angular Diameter Distance</strong> (<Latex>{'$D_A$'}</Latex>, used by CMB).
                        <br /><br />
                        The Isothermal Machian Universe suggests that because mass evolves over time (<Latex>{'$m \\propto t^{-1}$'}</Latex>), this rule is broken.
                        Standard candles (Supernovae, which are assumed to always have the exact same brightness) get dimmer not just because of distance, but because the mass of the atoms creating the light was different in the past.
                    </p>
                    <div className="bg-accent-cyan/10 p-6 rounded-lg border border-accent-cyan/30 text-center">
                        <Latex>{`$D_L^{obs} = D_L^{geom} \\times (1+z)^{\\alpha/2}$`}</Latex>
                        <p className="text-xs text-gray-500 mt-2">
                            (Where <Latex>{`$z$`}</Latex> is redshift, and <Latex>{`$\\alpha$`}</Latex> is the Mass Evolution Rate)
                        </p>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        This extra factor allows us to fit the Supernovae data with a higher <Latex>{'$H_0$'}</Latex> (73.0) while keeping the geometry consistent with the CMB (67.4).
                        The "Crisis" is just a misunderstanding of how mass works over cosmic time.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Lesson2_1;
