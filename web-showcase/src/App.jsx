import Hero from './components/Hero';
import Demo from './components/Demo';
import Technical from './components/Technical';
import Hardware from './components/Hardware';

function App() {
  return (
    <div className="bg-slate-900 min-h-screen text-slate-50 font-sans selection:bg-blue-500/30">
      <Hero />
      <Demo />
      <Technical />
      <Hardware />

      <footer className="py-8 text-center text-slate-600 text-sm bg-slate-950 border-t border-slate-900">
        <p>&copy; 2026 RobustClaim AI Project by Aryan</p>
      </footer>
    </div>
  );
}

export default App;
