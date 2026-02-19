import { ShieldCheck, Cpu } from 'lucide-react';

export default function Hero() {
    return (
        <section className="min-h-[80vh] flex flex-col justify-center items-center text-center px-6 relative overflow-hidden bg-slate-900">
            {/* Background Elements */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-blue-500/10 rounded-full blur-3xl -z-10 animate-pulse"></div>

            <div className="flex items-center gap-2 mb-6 px-4 py-1.5 rounded-full bg-slate-800/50 border border-slate-700 text-blue-400 text-sm font-medium">
                <Cpu className="w-4 h-4" />
                <span>Powered by Edge AI & Robust Regression</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-gradient-to-r from-white via-blue-100 to-blue-400 bg-clip-text text-transparent">
                RobustClaim AI
            </h1>

            <p className="text-xl md:text-2xl text-slate-400 max-w-2xl mb-8 leading-relaxed">
                Next-generation insurance prediction system engineered to withstand data anomalies.
                Robust Huber Loss modeling deployed on lightweight Arduino hardware.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
                <a href="#demo" className="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold transition-all shadow-lg shadow-blue-500/20 flex items-center justify-center gap-2">
                    Try Live Demo
                </a>
                <a href="#technical" className="px-8 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold border border-slate-700 transition-all flex items-center justify-center gap-2">
                    <ShieldCheck className="w-5 h-5" />
                    View Architecture
                </a>
            </div>
        </section>
    );
}
