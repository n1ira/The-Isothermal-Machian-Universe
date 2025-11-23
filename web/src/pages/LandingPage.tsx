import React from 'react';
import { Activity, Disc, Eye, Globe, Layers, Scale, Sparkles, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';
import Latex from '../components/Latex';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-[#050505] text-gray-200 font-sans selection:bg-cyan-500/30">
      {/* Header Section */}
      <header className="pt-16 pb-12 px-6 max-w-7xl mx-auto text-center">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white via-cyan-100 to-cyan-400">
          The Isothermal Machian Universe
        </h1>
        <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto font-light">
          A Unified Theory of Gravity, Cosmology, and Quantum Mechanics <br />
          <span className="text-cyan-400 font-semibold">Without Dark Matter or Dark Energy</span>
        </p>
      </header>

      {/* Main Grid Layout */}
      <main className="max-w-[1800px] mx-auto px-4 pb-20 grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* PROBLEM 1: COSMIC EXPANSION (Top Left) */}
        <div className="col-span-1 md:col-span-4 glass-panel p-6 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-colors group">
          <div className="flex items-center gap-3 mb-4 text-cyan-400">
            <Globe size={24} />
            <h2 className="text-lg font-bold tracking-widest uppercase">Problem 1: Cosmic Expansion</h2>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div className="bg-white/5 p-3 rounded-lg">
              <h3 className="text-xs text-gray-500 uppercase mb-1">Standard View (ΛCDM)</h3>
              <p>Expanding Space driven by mysterious "Dark Energy".</p>
            </div>
            <div className="bg-cyan-900/20 border border-cyan-500/30 p-3 rounded-lg">
              <h3 className="text-xs text-cyan-400 uppercase mb-1">IMU Solution</h3>
              <p>Static Space with <span className="text-white font-semibold">Evolving Mass</span> (<Latex>{'$m(t) \\propto t^{-1}$'}</Latex>).</p>
            </div>
          </div>
          
          <div className="text-sm text-gray-400">
            <strong className="text-white">Key Finding:</strong> Solves the "Early Galaxy Problem". Mature galaxies at <Latex>$z=10$</Latex> have had &gt;30 Gyr of atomic time to form, compared to the compressed &lt;500 Myr in ΛCDM.
          </div>
        </div>

        {/* CENTER PIECE: UNIFIED FIELD (Top Center - Spans 4 cols) */}
        <div className="col-span-1 md:col-span-4 row-span-2 bg-gradient-to-b from-gray-900 to-black rounded-2xl border border-cyan-500/50 p-8 flex flex-col items-center text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(0,243,255,0.15)_0%,_transparent_70%)] animate-pulse" />
          
          <Eye size={64} className="text-cyan-400 mb-6 relative z-10" />
          
          <h2 className="text-3xl font-bold text-white mb-2 relative z-10">ONE UNIFIED FIELD <Latex>$\phi$</Latex></h2>
          <p className="text-cyan-200/70 mb-8 relative z-10">A Universe Governed by One Scalar Field</p>
          
          <div className="flex-1 w-full grid grid-cols-2 gap-4 relative z-10">
            <div className="border-r border-white/10 pr-4 flex flex-col justify-center">
              <span className="text-xs uppercase tracking-widest text-gray-500 mb-2">Cosmic Scale</span>
              <span className="text-xl font-mono text-white"><Latex>{'$m(t) \\propto t^{-1}$'}</Latex></span>
              <p className="text-xs text-gray-400 mt-2">Evolving mass mimics expansion.</p>
            </div>
            <div className="pl-4 flex flex-col justify-center">
              <span className="text-xs uppercase tracking-widest text-gray-500 mb-2">Galactic Scale</span>
              <span className="text-xl font-mono text-white"><Latex>{'$m(r) \\propto e^{-r/R}$'}</Latex></span>
              <p className="text-xs text-gray-400 mt-2">Spatial gradient mimics dark matter.</p>
            </div>
          </div>
          
           <div className="mt-8 p-3 bg-white/5 rounded-lg font-mono text-xs text-cyan-300 break-all opacity-80">
             <Latex>{`$S = \\int d^4x\\sqrt{-g} \\left[ \\frac{R}{16\\pi G} - \\frac{1}{2}(\\partial\\phi)^2 - V(\\phi) - m(\\phi)\\bar{\\psi}\\psi + \\frac{\\lambda_\\gamma}{4}\\ln(\\frac{\\phi}{M_{pl}})F^2 \\right]$`}</Latex>
           </div>
        </div>

        {/* PROBLEM 2: GALAXY ROTATION (Top Right) */}
        <div className="col-span-1 md:col-span-4 glass-panel p-6 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-colors group">
          <div className="flex items-center gap-3 mb-4 text-cyan-400">
            <Activity size={24} />
            <h2 className="text-lg font-bold tracking-widest uppercase">Problem 2: Galaxy Rotation</h2>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div className="bg-white/5 p-3 rounded-lg">
              <h3 className="text-xs text-gray-500 uppercase mb-1">Standard View</h3>
              <p>Invisible "Dark Matter" halos provide extra gravity.</p>
            </div>
            <div className="bg-cyan-900/20 border border-cyan-500/30 p-3 rounded-lg">
              <h3 className="text-xs text-cyan-400 uppercase mb-1">IMU Solution</h3>
              <p><span className="text-white font-semibold">Gradient of Inertia</span>. Reduced mass allows high speeds.</p>
            </div>
          </div>
          
          <div className="text-sm text-gray-400">
            <strong className="text-white">Key Finding:</strong> Breaks Equivalence Principle. Ratio <Latex>$m_g/m_i$</Latex> grows with radius, naturally producing flat rotation curves without hidden mass.
          </div>
        </div>

        {/* PROBLEM 3: LENSING (Middle Left) */}
        <div className="col-span-1 md:col-span-4 glass-panel p-6 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-colors group">
          <div className="flex items-center gap-3 mb-4 text-cyan-400">
            <Scale size={24} />
            <h2 className="text-lg font-bold tracking-widest uppercase">Problem 3: Lensing</h2>
          </div>
          
           <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div className="bg-white/5 p-3 rounded-lg">
              <h3 className="text-xs text-gray-500 uppercase mb-1">Standard View</h3>
              <p>Light bends around Dark Matter clumps.</p>
            </div>
            <div className="bg-cyan-900/20 border border-cyan-500/30 p-3 rounded-lg">
              <h3 className="text-xs text-cyan-400 uppercase mb-1">IMU Solution</h3>
              <p><span className="text-white font-semibold">Refractive Vacuum</span>. Light bends due to <Latex>$\nabla \phi$</Latex>.</p>
            </div>
          </div>

          <div className="text-sm text-gray-400">
            <strong className="text-white">Key Finding:</strong> Explains the Bullet Cluster. The refractive index gradient follows the scalar field (which follows galaxies), appearing offset from the gas.
          </div>
        </div>

        {/* PROBLEM 4: COSMIC STRUCTURE (Middle Right) */}
        <div className="col-span-1 md:col-span-4 glass-panel p-6 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-colors group">
          <div className="flex items-center gap-3 mb-4 text-cyan-400">
            <Layers size={24} />
            <h2 className="text-lg font-bold tracking-widest uppercase">Problem 4: Structure & CMB</h2>
          </div>

           <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div className="bg-white/5 p-3 rounded-lg">
              <h3 className="text-xs text-gray-500 uppercase mb-1">Standard View</h3>
              <p>Baryons fall into Dark Matter potential wells.</p>
            </div>
            <div className="bg-cyan-900/20 border border-cyan-500/30 p-3 rounded-lg">
              <h3 className="text-xs text-cyan-400 uppercase mb-1">IMU Solution</h3>
              <p><span className="text-white font-semibold">"Fifth Force"</span> from scalar field creates wells.</p>
            </div>
          </div>

          <div className="text-sm text-gray-400">
            <strong className="text-white">Key Finding:</strong> Reproduces Acoustic Peaks. The theory is conformally dual to ΛCDM, producing the same CMB power spectrum.
          </div>
        </div>

        {/* PROBLEM 5: BLACK HOLES (Bottom Left - Wide) */}
        <div className="col-span-1 md:col-span-6 glass-panel p-6 rounded-2xl border border-white/10 hover:border-cyan-500/50 transition-colors group">
          <div className="flex items-center gap-3 mb-4 text-cyan-400">
            <Disc size={24} />
            <h2 className="text-lg font-bold tracking-widest uppercase">Problem 5: Black Hole Paradox</h2>
          </div>
          
          <div className="flex gap-6">
             <div className="flex-1 text-sm">
                <div className="mb-3">
                   <h3 className="text-xs text-gray-500 uppercase mb-1">Standard View</h3>
                   <p className="text-gray-300">Information destroyed at singularity or lost, violating Quantum Mechanics.</p>
                </div>
                <div>
                   <h3 className="text-xs text-cyan-400 uppercase mb-1">IMU Solution</h3>
                   <p className="text-gray-200">"Solid Time" Horizon. A phase transition where time dilation <Latex>{'$\\to \\infty$'}</Latex>.</p>
                </div>
             </div>
             <div className="w-px bg-white/10"></div>
             <div className="flex-1 text-sm text-gray-400 flex flex-col justify-center">
                <strong className="text-white block mb-2">
Key Finding:</strong>
Paradox Resolved. The horizon is a physical surface of frozen time. Information is holographically preserved on the 2D boundary.
             </div>
          </div>
        </div>

        {/* PREDICTION: SMOKING GUN (Bottom Right - Wide) */}
        <div className="col-span-1 md:col-span-6 bg-gradient-to-br from-cyan-900/20 to-transparent p-6 rounded-2xl border border-cyan-500/30 hover:border-cyan-400 transition-colors group relative overflow-hidden">
           <div className="absolute top-0 right-0 p-4 opacity-20">
              <Zap size={64} />
           </div>
          <div className="flex items-center gap-3 mb-4 text-white">
            <Sparkles size={24} className="text-yellow-400" />
            <h2 className="text-lg font-bold tracking-widest uppercase text-white">A Falsifiable Prediction: The Smoking Gun</h2>
          </div>
          
          <h3 className="text-2xl font-bold text-cyan-400 mb-2">Shapiro Time Delay Anomaly</h3>
          <p className="text-gray-300 mb-4 max-w-xl">
             Definitive test to distinguish theories. While deflection angles match, the integrated time delay differs significantly.
          </p>

          <div className="grid grid-cols-2 gap-8 mt-6">
             <div className="text-center">
                <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">Standard Model (ΛCDM)</div>
                <div className="text-3xl font-mono text-gray-400">~25 Days</div>
             </div>
             <div className="text-center relative">
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-cyan-500 text-black text-[10px] font-bold px-2 py-0.5 rounded-full">
                   PREDICTION
                </div>
                <div className="text-xs text-cyan-400 uppercase tracking-widest mb-1">Isothermal Machian</div>
                <div className="text-3xl font-mono text-white">~16 Days</div>
                <div className="text-xs text-cyan-300 mt-1">(37% Deficit)</div>
             </div>
          </div>
        </div>

        {/* COMPARISON TABLE (Full Width) */}
        <div className="col-span-1 md:col-span-12 mt-8">
           <h2 className="text-2xl font-bold text-center mb-8 tracking-widest text-gray-500">COMPARISON MATRIX</h2>
           <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                 <thead>
                    <tr className="border-b border-white/10 text-xs uppercase tracking-widest text-gray-500">
                       <th className="p-4">Observable</th>
                       <th className="p-4">Standard Model (ΛCDM)</th>
                       <th className="p-4 text-cyan-400">Isothermal Machian Universe (IMU)</th>
                    </tr>
                 </thead>
                 <tbody className="text-sm text-gray-300">
                    <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                       <td className="p-4 font-semibold text-white">Cosmic Redshift</td>
                       <td className="p-4">Dark Energy drives expansion of space</td>
                       <td className="p-4 text-cyan-100">Evolving mass scale ($m(t) \propto t^{-1}$) in static space</td>
                    </tr>
                    <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                       <td className="p-4 font-semibold text-white">Galaxy Rotation</td>
                       <td className="p-4">Invisible Dark Matter halos</td>
                       <td className="p-4 text-cyan-100">Scalar field creates inertial mass gradient</td>
                    </tr>
                    <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                       <td className="p-4 font-semibold text-white">Gravitational Lensing</td>
                       <td className="p-4">Light bends around Dark Matter mass</td>
                       <td className="p-4 text-cyan-100">Scalar field creates refractive index for light</td>
                    </tr>
                     <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                       <td className="p-4 font-semibold text-white">CMB Structure</td>
                       <td className="p-4">Baryons fall into Dark Matter wells</td>
                       <td className="p-4 text-cyan-100">"Fifth Force" from scalar field creates wells</td>
                    </tr>
                     <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                       <td className="p-4 font-semibold text-white">Age of Universe</td>
                       <td className="p-4">~13.8 Billion Years</td>
                       <td className="p-4 text-cyan-100">&gt; 26 Billion Years (in atomic time)</td>
                    </tr>
                 </tbody>
              </table>
           </div>
        </div>

         <div className="col-span-1 md:col-span-12 text-center mt-16">
            <Link to="/station" className="inline-flex items-center gap-3 bg-cyan-500 text-black px-8 py-4 rounded-full font-bold hover:bg-cyan-400 transition-all hover:scale-105 shadow-[0_0_20px_rgba(0,243,255,0.3)]">
               <Layers size={20} />
               ENTER RESEARCH STATION
            </Link>
         </div>

      </main>
    </div>
  );
};

export default LandingPage;
