
import Latex from '../components/Latex';

const Lesson1_1 = () => {
    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 1</span>
                    <span>/</span>
                    <span>LESSON 1.1</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    The Illusion of Expansion
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    We are taught that the universe is expanding. But "expansion" is a relative term.
                    To measure change, you need a ruler. What if the ruler itself is changing?
                </p>
            </header>

            {/* Section 1: The Ruler Problem */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Ruler Problem</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        Imagine you are measuring a table. You say it is "2 meters long".
                        What you really mean is that the table is <strong>twice as long</strong> as your meter stick.
                    </p>
                    <div className="bg-black/30 p-4 rounded border border-white/10 text-center">
                        <Latex>{`$L_{table} = 2 \\times L_{meter\\_stick}$`}</Latex>
                        <p className="text-xs text-gray-500 mt-2">
                            (Where <Latex>{`$L$`}</Latex> stands for Length)
                        </p>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        Physics only deals in <strong>dimensionless ratios</strong>. We compare one physical thing to another.
                        If the table doubles in size, AND your meter stick doubles in size, the ratio is still 2.
                        You would perceive <strong>no change</strong>.
                    </p>

                    {/* Alice Analogy */}
                    <div className="bg-purple-900/20 border-l-4 border-purple-500 p-6 space-y-2">
                        <h3 className="text-purple-300 font-bold text-lg">The "Alice in Wonderland" Analogy</h3>
                        <p className="text-gray-300">
                            When Alice drinks the potion, she shrinks. But to her, the room looks like it's growing.
                            <br />
                            <strong>Question:</strong> Did the room get bigger, or did Alice get smaller?
                            <br />
                            <strong>Answer:</strong> It doesn't matter! Mathematically, they are the exact same thing.
                        </p>
                    </div>

                    <div className="bg-blue-900/20 border-l-4 border-blue-500 p-4">
                        <p className="text-sm text-blue-200">
                            <strong>Key Concept:</strong> Absolute size is meaningless. Only relative size matters.
                            This symmetry is called <strong>Global Weyl Invariance</strong>.
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 2: What is a Ruler? */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">2. What is our Cosmic Ruler?</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        In astronomy, our "ruler" is the <strong>atom</strong>. Specifically, the light emitted by atoms (like <strong>Hydrogen</strong>).
                        The size of a Hydrogen atom (the <strong>Bohr radius</strong> <Latex>{'$a_0$'}</Latex>) is determined by the <strong>mass of the electron</strong> (<Latex>{'$m_e$'}</Latex>), the <strong>electric charge</strong> (<Latex>{'$e$'}</Latex>), and the <strong>Planck Constant</strong> (<Latex>{'$\\hbar$'}</Latex>, representing the quantum scale).
                    </p>
                    <div className="flex justify-center py-4">
                        <div className="bg-black/40 px-8 py-4 rounded-lg border border-white/10">
                            <Latex>{`$a_0 = \\frac{\\hbar^2}{m_e e^2} \\propto \\frac{1}{m_e}$`}</Latex>
                        </div>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        Look at the equation closely. The size of the atom is <strong>inversely proportional</strong> to the mass of the electron.
                    </p>
                    <ul className="list-disc list-inside space-y-2 text-gray-300 ml-4">
                        <li>If the electron gets <strong>heavier</strong>, the atom gets <strong>smaller</strong> (the electron is pulled closer).</li>
                        <li>If the electron gets <strong>lighter</strong>, the atom gets <strong>larger</strong> (the electron drifts away).</li>
                    </ul>
                </div>
            </section>

            {/* Section 3: The Two Interpretations */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. The Redshift: Two Views</h2>
                <p className="text-gray-400">
                    We observe that light from distant galaxies is "redshifted" (the waves look longer).
                    There are two mathematically identical ways to explain this.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-4">
                    {/* View A: Standard */}
                    <div className="glass-panel p-6 border-t-4 border-t-accent-cyan space-y-4">
                        <h3 className="text-xl font-bold text-accent-cyan">View A: Expanding Space</h3>
                        <p className="text-sm text-gray-400 uppercase tracking-widest">Standard Model (ΛCDM)</p>
                        <div className="space-y-4 text-gray-300 text-sm">
                            <p>1. Atoms stay the same size forever (<Latex>{'$m_e$'}</Latex> is constant).</p>
                            <p>2. The empty space between galaxies stretches.</p>
                            <p>3. Light waves travelling through space get stretched.</p>
                            <p>4. <strong>Result:</strong> Old light looks redder.</p>
                        </div>
                    </div>

                    {/* View B: Machian */}
                    <div className="glass-panel p-6 border-t-4 border-t-accent-pink space-y-4">
                        <h3 className="text-xl font-bold text-accent-pink">View B: Evolving Mass</h3>
                        <p className="text-sm text-gray-400 uppercase tracking-widest">Machian Universe (IMU)</p>
                        <div className="space-y-4 text-gray-300 text-sm">
                            <p>1. Space is static (it doesn't move).</p>
                            <p>2. Particle masses are slowly <strong>decreasing</strong> (<Latex>{'$m_e \\downarrow$'}</Latex>).</p>
                            <p>3. Because mass drops, atoms are getting <strong>larger</strong> (<Latex>{'$a_0 \\uparrow$'}</Latex>).</p>
                            <p>4. <strong>Result:</strong> Ancient atoms were smaller and emitted "bluer" (shorter) light. Compared to our current "large" atoms, that old light looks red.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Section 4: The Equivalence */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">4. Why change the theory?</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        If both views explain the redshift, why bother changing?
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        Because the "Expanding Space" view requires <strong>Dark Energy</strong> to explain why the expansion is accelerating.
                        It requires <strong>Dark Matter</strong> to explain why galaxies spin fast.
                    </p>
                    <p className="text-gray-300 leading-relaxed">
                        The "Evolving Mass" view suggests these aren't new invisible substances. They are just side-effects of the mass changing.
                        If mass <Latex>{'$m(t)$'}</Latex> is the fundamental variable, we can derive "Dark Energy" as simply the rate at which mass is vanishing.
                    </p>
                    <div className="flex justify-center mt-6">
                        <div className="bg-white/5 p-6 rounded-lg text-center">
                            <p className="text-lg font-mono text-white mb-2">The Translation Dictionary</p>
                            <Latex>{`$a(t) \\iff \\frac{1}{m(t)}$`}</Latex>
                            <p className="text-xs text-gray-500 mt-2">Scale Factor (Expansion) is equivalent to Inverse Mass (Shrinking)</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Lesson1_1;
