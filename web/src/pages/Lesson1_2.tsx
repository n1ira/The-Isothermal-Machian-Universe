
import Latex from '../components/Latex';

const Lesson1_2 = () => {
    return (
        <div className="space-y-12 animate-fade-in max-w-4xl mx-auto pb-20">
            {/* Header */}
            <header className="space-y-6 border-b border-white/10 pb-8">
                <div className="flex items-center gap-2 text-accent-cyan font-mono text-sm">
                    <span>MODULE 1</span>
                    <span>/</span>
                    <span>LESSON 1.2</span>
                </div>
                <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    Reading the Code of the Universe
                </h1>
                <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                    Physics isn't written in words; it's written in Lagrangians.
                    Let's dissect the single equation that generates the entire Isothermal Machian Universe.
                </p>
            </header>

            {/* Section 1: The Action Principle */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">1. The Action Principle</h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        The universe is lazy. It always chooses the path that minimizes a quantity called the <strong>Action</strong> (<Latex>{'$S$'}</Latex>).
                        Think of the Action as a "Score" or "Cost" for a particular history of the universe. Nature wants to pay the lowest cost possible.
                    </p>
                    <div className="bg-black/40 p-8 rounded-xl border border-white/10 overflow-x-auto text-center">
                        <Latex>
                            {`$S = \\int d^4x \\sqrt{-g} \\left[ \\frac{M_{pl}^2}{2} R - \\frac{1}{2}(\\partial \\phi)^2 - V_{eff}(\\phi) \\right]$`}
                        </Latex>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        This looks scary, but it has four distinct parts. Let's break them down.
                    </p>
                </div>
            </section>

            {/* Section 2: The Stage */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">
                    2. The Stage: <Latex>{`$\\int d^4x \\sqrt{-g}$`}</Latex>
                </h2>
                <div className="glass-panel p-8 space-y-4">
                    <div className="flex items-start gap-4">
                        <div className="p-3 bg-blue-500/20 rounded text-blue-300 font-mono text-xl">A</div>
                        <div>
                            <h3 className="text-xl font-bold text-white mb-2">Summing Everything Up</h3>
                            <p className="text-gray-300">
                                <Latex>{`$\\int$`}</Latex> is the symbol for "Sum".
                                <br />
                                <Latex>{`$d^4x$`}</Latex> represents a tiny chunk of spacetime (3 dimensions of space + 1 dimension of time).
                                <br />
                                Together, <Latex>{`$\\int d^4x$`}</Latex> means "Sum up every tiny chunk of space and time in the universe".
                            </p>
                        </div>
                    </div>
                    <div className="w-full h-px bg-white/5 my-4" />
                    <div className="flex items-start gap-4">
                        <div className="p-3 bg-purple-500/20 rounded text-purple-300 font-mono text-xl">B</div>
                        <div>
                            <h3 className="text-xl font-bold text-white mb-2">
                                The Volume Element (<Latex>{`$\\sqrt{-g}$`}</Latex>)
                            </h3>
                            <p className="text-gray-300">
                                Space can stretch and curve. A coordinate box of "1x1x1" might actually be huge or tiny depending on gravity.
                                <Latex>{`$\\sqrt{-g}$`}</Latex> is the correction factor that tells us the <strong>actual physical volume</strong> of a chunk of spacetime.
                                <br /><br />
                                <span className="text-sm text-gray-400">
                                    <strong>Why the minus sign?</strong> In relativity, time is treated differently from space (it has a negative sign in the math).
                                    This makes the determinant <Latex>{`$g$`}</Latex> negative. We add the minus sign to make it positive before taking the square root.
                                </span>
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Section 3: The Actors */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">3. The Actors</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="glass-panel p-6 space-y-4 border-t-4 border-t-white">
                        <h3 className="text-xl font-bold text-white">Gravity (<Latex>{`$R$`}</Latex>)</h3>
                        <div className="h-20 flex items-center justify-center bg-black/20 rounded">
                            <Latex>{`$\\frac{M_{pl}^2}{2} R$`}</Latex>
                        </div>
                        <p className="text-sm text-gray-300">
                            <Latex>{`$R$`}</Latex> is the <strong>Ricci Scalar</strong>. It measures how curved space is at a point.
                            <br /><br />
                            <Latex>{`$M_{pl}$`}</Latex> is the <strong>Planck Mass</strong>. It represents the "stiffness" of spacetime.
                            A large <Latex>{`$M_{pl}$`}</Latex> means space is very stiff and hard to bend.
                            <br /><br />
                            This term says: "Spacetime resists being curved." It costs energy to bend space. This is standard Einstein Gravity.
                        </p>
                    </div>

                    <div className="glass-panel p-6 space-y-4 border-t-4 border-t-accent-pink">
                        <h3 className="text-xl font-bold text-accent-pink">The Field (<Latex>{`$\\phi$`}</Latex>)</h3>
                        <div className="h-20 flex items-center justify-center bg-black/20 rounded">
                            <Latex>{`$-\\frac{1}{2}(\\partial \\phi)^2$`}</Latex>
                        </div>
                        <p className="text-sm text-gray-300">
                            This is the <strong>Kinetic Term</strong>. <Latex>{`$\\partial \\phi$`}</Latex> is the gradient (slope) of the field.
                            <br /><br />
                            This term says: "The field hates changing quickly." It wants to be smooth. If it changes rapidly in space or time, it costs energy.
                        </p>
                    </div>
                </div>
            </section>

            {/* Section 4: The Script */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">4. The Script: <Latex>{`$V_{eff}(\\phi)$`}</Latex></h2>
                <div className="glass-panel p-8 space-y-6">
                    <p className="text-gray-300 leading-relaxed">
                        The Potential <Latex>{`$V(\\phi)$`}</Latex> is the engine of the theory. It tells the field <Latex>{`$\\phi$`}</Latex> what value it "wants" to have.
                        Imagine a ball rolling down a hill. The shape of the hill is <Latex>{`$V(\\phi)$`}</Latex>.
                    </p>
                    <div className="bg-black/30 p-6 rounded-lg border border-white/10 text-center">
                        <Latex>{`$V_{eff}(\\phi) = \\frac{\\lambda}{4}\\phi^4 - \\frac{\\mu^2}{2}\\phi^2$`}</Latex>
                        <div className="mt-4 text-left text-sm text-gray-400 space-y-2">
                            <p>
                                <strong className="text-white">1. The Quartic Term (<Latex>{`$\\frac{\\lambda}{4}\\phi^4$`}</Latex>):</strong> This pushes the ball <strong>up</strong> at the edges. It keeps the field from running away to infinity. <Latex>{`$\\lambda$`}</Latex> (Lambda) controls how steep the walls are.
                            </p>
                            <p>
                                <strong className="text-white">2. The Quadratic Term (<Latex>{`$-\\frac{\\mu^2}{2}\\phi^2$`}</Latex>):</strong> This pushes the ball <strong>down</strong> in the center. It creates the "hill" at zero. <Latex>{`$\\mu$`}</Latex> (Mu) controls how unstable the center is.
                            </p>
                        </div>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        This specific shape (a "Mexican Hat" or "Double Well") is crucial.
                    </p>
                    <ul className="list-disc list-inside space-y-2 text-gray-300 ml-4">
                        <li>At high energy (Early Universe), the ball sits at the top (<Latex>{`$\\phi=0$`}</Latex>).</li>
                        <li>As the universe cools, the ball rolls down to the bottom.</li>
                        <li><strong>The rolling of the ball IS the flow of time.</strong></li>
                    </ul>
                </div>
            </section>

            {/* Section 5: The Interaction */}
            <section className="space-y-6">
                <h2 className="text-3xl font-bold text-white">5. The Interaction</h2>
                <div className="glass-panel p-8 space-y-6 bg-gradient-to-br from-white/5 to-accent-cyan/5">
                    <p className="text-gray-300 leading-relaxed">
                        The equation above describes the field living in spacetime. But how does it touch <strong>us</strong> (matter)?
                        That's the final piece of the puzzle:
                    </p>
                    <div className="text-center py-4">
                        <Latex>{`$m_{atom} \\propto \\phi$`}</Latex>
                    </div>
                    <p className="text-gray-300 leading-relaxed">
                        The mass of every atom in your body is determined by the value of <Latex>{`$\\phi$`}</Latex>.
                        As <Latex>{`$\\phi$`}</Latex> rolls down the hill (Section 4), your mass changes.
                        This change in mass changes the size of atoms (Lesson 1.1), creating the illusion of a redshifting universe.
                    </p>
                </div>
            </section >
        </div >
    );
};

export default Lesson1_2;
