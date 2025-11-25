import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import Lesson1_1 from './pages/Lesson1_1';
import Lesson1_2 from './pages/Lesson1_2';
import Lesson1_3 from './pages/Lesson1_3';
import Lesson1_4 from './pages/Lesson1_4';
import Lesson2_1 from './pages/Lesson2_1';
import Lesson2_2 from './pages/Lesson2_2';
import Lesson2_3 from './pages/Lesson2_3';
import Lesson2_4 from './pages/Lesson2_4';
import Lesson3_1 from './pages/Lesson3_1';
import Lesson3_2 from './pages/Lesson3_2';
import Lesson4_1 from './pages/Lesson4_1';
import Lesson4_2 from './pages/Lesson4_2';
import GalaxyRotation from './pages/GalaxyRotation';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/*" element={
          <div className="flex h-screen w-full bg-background text-white overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-y-auto p-8 relative">
              {/* Background Starfield */}
              <div className="absolute inset-0 z-0 pointer-events-none bg-[radial-gradient(circle_at_center,_#1a1a1a_0%,_#050505_100%)] opacity-50" />

              <div className="relative z-10 max-w-[1600px] mx-auto">
                <Routes>
                  <Route path="/station" element={<Dashboard />} />
                  <Route path="/lesson/1.1" element={<Lesson1_1 />} />
                  <Route path="/lesson/1.2" element={<Lesson1_2 />} />
                  <Route path="/lesson/1.3" element={<Lesson1_3 />} />
                  <Route path="/lesson/1.4" element={<Lesson1_4 />} />
                  <Route path="/lesson/2.1" element={<Lesson2_1 />} />
                  <Route path="/lesson/2.2" element={<Lesson2_2 />} />
                  <Route path="/lesson/2.3" element={<Lesson2_3 />} />
                  <Route path="/lesson/2.4" element={<Lesson2_4 />} />
                  <Route path="/lesson/3.1" element={<Lesson3_1 />} />
                  <Route path="/lesson/3.2" element={<Lesson3_2 />} />
                  <Route path="/lesson/4.1" element={<Lesson4_1 />} />
                  <Route path="/lesson/4.2" element={<Lesson4_2 />} />
                  <Route path="/galaxy-rotation" element={<GalaxyRotation />} />
                  {/* Redirects for old routes if needed, or just 404 implicitly */}
                  <Route path="*" element={<Navigate to="/station" replace />} />
                </Routes>
              </div>
            </main>
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;
