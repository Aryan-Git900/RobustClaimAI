import { Code, Server } from 'lucide-react';

const arduinoSnippet = `
// Hardcoded Model on Arduino
const float INTERCEPT       = 4040.12;
const float WEIGHT_AGE      = 237.32;
const float WEIGHT_BMI      = 267.54;
const float WEIGHT_CHILDREN = 433.82;

void loop() {
  // Real-time inference
  float prediction = INTERCEPT + 
                    (WEIGHT_AGE * age) + 
                    (WEIGHT_BMI * bmi) + 
                    (WEIGHT_CHILDREN * children);
                    
  lcd.print(prediction);
}
`;

export default function Hardware() {
    return (
        <section className="py-20 px-6 bg-slate-900 border-t border-slate-800">
            <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-12 items-center">
                <div>
                    <div className="flex items-center gap-3 mb-6">
                        <Server className="w-8 h-8 text-emerald-500" />
                        <h2 className="text-3xl font-bold">Edge Deployment</h2>
                    </div>
                    <p className="text-slate-400 mb-6 leading-relaxed">
                        The trained model is deployed directly onto an Arduino microcontroller.
                        By hardcoding the learned coefficients, we achieve <span className="text-white font-medium">O(1) inference time</span> with minimal memory footprint.
                    </p>
                    <ul className="space-y-4 mb-8">
                        <li className="flex items-start gap-3">
                            <div className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">1</div>
                            <span className="text-slate-300">Offline inference (No internet required)</span>
                        </li>
                        <li className="flex items-start gap-3">
                            <div className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">2</div>
                            <span className="text-slate-300">Low power consumption (~50mA)</span>
                        </li>
                        <li className="flex items-start gap-3">
                            <div className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">3</div>
                            <span className="text-slate-300">Instant results on LCD display</span>
                        </li>
                    </ul>
                </div>

                <div className="bg-slate-950 rounded-xl border border-slate-800 overflow-hidden shadow-2xl">
                    <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border-b border-slate-800">
                        <Code className="w-4 h-4 text-slate-500" />
                        <span className="text-xs text-slate-500 font-mono">insurance_predictor.ino</span>
                    </div>
                    <pre className="p-4 overflow-x-auto text-sm font-mono text-emerald-400">
                        <code>{arduinoSnippet}</code>
                    </pre>
                </div>
            </div>
        </section>
    );
}
