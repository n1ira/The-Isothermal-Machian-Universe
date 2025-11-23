import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Cosmology from './pages/Cosmology';
import GalaxyRotation from './pages/GalaxyRotation';
import BlackHole from './pages/BlackHole';

function App() {
  return (
    <Router>
      <div className="flex h-screen w-full bg-background text-white overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8 relative">
          {/* Background Starfield (Optional, can be added later) */}
          <div className="absolute inset-0 z-0 pointer-events-none bg-[radial-gradient(circle_at_center,_#1a1a1a_0%,_#050505_100%)] opacity-50" />

          <div className="relative z-10 max-w-[1600px] mx-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/cosmology" element={<Cosmology />} />
              <Route path="/galaxy" element={<GalaxyRotation />} />
              <Route path="/black-hole" element={<BlackHole />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
