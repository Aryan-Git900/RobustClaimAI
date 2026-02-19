import { useState, useEffect } from 'react';
import { Cpu, RotateCcw } from 'lucide-react';

// --- ARDUINO CONSTANTS (Same as Firmware) ---
const INTERCEPT = 3080.80;
const WEIGHT_AGE = 251.85;
const WEIGHT_BMI = 310.85;
const WEIGHT_CHILDREN = 458.22;

const ROWS = 4;
const COLS = 4;
const KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
];

// LCD State Machine
const STATE = {
    WELCOME: 0,
    WAIT_START: 1,
    INPUT_AGE: 2,
    INPUT_BMI: 3,
    INPUT_CHILDREN: 4,
    PREDICT: 5,
    RESULT: 6
};

export default function Demo() {
    // System State
    const [currentState, setCurrentState] = useState(STATE.WELCOME);
    const [lcdLine1, setLcdLine1] = useState("Robust Claim AI");
    const [lcdLine2, setLcdLine2] = useState("");
    const [inputBuffer, setInputBuffer] = useState("");

    // Data Storage
    const [data, setData] = useState({ age: 0, bmi: 0, children: 0 });

    // Blinking cursor effect
    const [showCursor, setShowCursor] = useState(true);
    useEffect(() => {
        const interval = setInterval(() => setShowCursor(prev => !prev), 500);
        return () => clearInterval(interval);
    }, []);

    // --- STATE MACHINE LOGIC (Matches C++ loop()) ---

    // Reset/Welcome
    useEffect(() => {
        if (currentState === STATE.WELCOME) {
            setLcdLine1("Robust Claim AI");
            setLcdLine2("");
            setTimeout(() => {
                setLcdLine1("Press A to Start");
                setCurrentState(STATE.WAIT_START);
            }, 2000);
        }
    }, [currentState]);

    const handleKey = (key) => {
        // Play sound (optional, maybe later)

        switch (currentState) {
            case STATE.WAIT_START:
                if (key === 'A') {
                    setCurrentState(STATE.INPUT_AGE);
                    setInputBuffer("");
                    setLcdLine1("Enter Age:");
                    setLcdLine2("");
                }
                break;

            case STATE.INPUT_AGE:
                handleInput(key, "age", STATE.INPUT_BMI, "Enter BMI:");
                break;

            case STATE.INPUT_BMI:
                handleInput(key, "bmi", STATE.INPUT_CHILDREN, "Ent. Children:");
                break;

            case STATE.INPUT_CHILDREN:
                handleInput(key, "children", STATE.PREDICT, "");
                break;

            case STATE.RESULT:
                if (key === 'D') {
                    setCurrentState(STATE.WELCOME);
                }
                break;

            default:
                break;
        }
    };

    const handleInput = (key, field, nextState, nextPrompt) => {
        if (key >= '0' && key <= '9') {
            const newBuffer = inputBuffer + key;
            if (newBuffer.length <= 16) { // Max chars per line
                setInputBuffer(newBuffer);
                setLcdLine2(newBuffer);
            }
        } else if (key === '#') { // Enter
            if (inputBuffer.length > 0) {
                // Save Value
                setData(prev => ({ ...prev, [field]: parseFloat(inputBuffer) }));

                // Transition
                setInputBuffer("");
                if (nextState === STATE.PREDICT) {
                    // predict(parseFloat(inputBuffer)); // REMOVED (undefined)
                    // Better to call predict with the combined data + current input
                    // Actually, let's use a helper for prediction transition
                    runPrediction({ ...data, [field]: parseFloat(inputBuffer) });
                } else {
                    setCurrentState(nextState);
                    setLcdLine1(nextPrompt);
                    setLcdLine2("");
                }
            }
        } else if (key === '*') { // Backspace
            setInputBuffer("");
            setLcdLine2("");
        }
    };

    const runPrediction = (finalData) => {
        setCurrentState(STATE.PREDICT);
        setLcdLine1("Predicting...");
        setLcdLine2("");

        // Simulate delay
        setTimeout(() => {
            const pred = INTERCEPT +
                (WEIGHT_AGE * finalData.age) +
                (WEIGHT_BMI * finalData.bmi) +
                (WEIGHT_CHILDREN * finalData.children);

            setLcdLine1("Claims: $");
            setLcdLine2(pred.toFixed(2));

            // Allow Reset after a moment
            setTimeout(() => {
                // Show "Press D" hint momentarily or just stay on result
                // Real C++ code shows result, then waits for D.
                // We can maybe toggle the display or just leave it. 
                // Let's alternate line 2
                let toggle = false;
                const resultInterval = setInterval(() => {
                    if (currentState !== STATE.RESULT) { // If user pressed D, stop
                        clearInterval(resultInterval);
                        return;
                    }
                    toggle = !toggle;
                    // But wait, we can't capture state change in interval easily.
                    // Let's just assume user knows D is reset or show it eventually.
                }, 2000);

                // Let's just update state to RESULT so D works
                setCurrentState(STATE.RESULT);
            }, 1000);

        }, 1500);
    };

    return (
        <section id="demo" className="py-20 px-6 bg-slate-900 border-t border-slate-800">
            <div className="max-w-4xl mx-auto flex flex-col items-center">

                <div className="flex items-center gap-3 mb-10">
                    <Cpu className="w-8 h-8 text-emerald-500" />
                    <h2 className="text-3xl font-bold">Virtual Hardware Demo</h2>
                </div>

                {/* ARDUINO BOARD SIMULATION */}
                <div className="bg-emerald-900/20 p-8 rounded-3xl border-4 border-emerald-800/50 shadow-2xl relative">
                    {/* PCB Screw Holes */}
                    <div className="absolute top-4 left-4 w-4 h-4 rounded-full bg-slate-800 border border-slate-600"></div>
                    <div className="absolute top-4 right-4 w-4 h-4 rounded-full bg-slate-800 border border-slate-600"></div>
                    <div className="absolute bottom-4 left-4 w-4 h-4 rounded-full bg-slate-800 border border-slate-600"></div>
                    <div className="absolute bottom-4 right-4 w-4 h-4 rounded-full bg-slate-800 border border-slate-600"></div>

                    <div className="flex flex-col md:flex-row gap-12 items-center">

                        {/* LCD SCREEN */}
                        <div className="bg-slate-800 p-4 rounded-lg shadow-inner border-2 border-slate-700 w-full md:w-80">
                            <div className="bg-[#9ea751] h-32 w-full rounded border-4 border-[#5f6332] shadow-[inset_0_0_20px_rgba(0,0,0,0.5)] flex flex-col justify-center px-4 relative overflow-hidden">
                                {/* Scanlines */}
                                <div className="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%)] bg-[length:100%_4px] pointer-events-none"></div>

                                <p className="font-['VT323'] text-3xl text-slate-900 leading-none tracking-widest uppercase truncate relative z-10">
                                    {lcdLine1}
                                </p>
                                <p className="font-['VT323'] text-3xl text-slate-900 leading-none tracking-widest uppercase truncate min-h-[1.5rem] relative z-10">
                                    {lcdLine2}{showCursor && (currentState !== STATE.PREDICT && currentState !== STATE.RESULT) ? '_' : ''}
                                </p>
                            </div>
                            <div className="mt-2 text-center text-xs text-slate-500 uppercase tracking-widest">LCD 1602 Module</div>
                        </div>

                        {/* KEYPAD */}
                        <div className="bg-slate-800 p-1 rounded-xl shadow-xl w-64">
                            <div className="grid grid-cols-4 gap-2 bg-slate-900 p-4 rounded-lg border border-slate-700">
                                {KEYS.map((row, rIndex) => (
                                    row.map((key, cIndex) => (
                                        <button
                                            key={`${rIndex}-${cIndex}`}
                                            onClick={() => handleKey(key)}
                                            className={`
                                        h-12 w-12 rounded-lg font-bold text-lg shadow-[0_4px_0_rgb(0,0,0)] active:shadow-none active:translate-y-1 transition-all
                                        ${['A', 'B', 'C', 'D'].includes(key) ? 'bg-red-600 hover:bg-red-500 text-white shadow-red-900' :
                                                    ['#', '*'].includes(key) ? 'bg-slate-600 hover:bg-slate-500 text-white shadow-slate-800' :
                                                        'bg-slate-200 hover:bg-white text-slate-900 shadow-slate-400'}
                                    `}
                                        >
                                            {key}
                                        </button>
                                    ))
                                ))}
                            </div>
                            <div className="mt-2 text-center text-xs text-slate-500 uppercase tracking-widest">4x4 Matrix Keypad</div>
                        </div>
                    </div>

                    {/* Instructions */}
                    <div className="mt-8 pt-6 border-t border-emerald-800/30 text-emerald-400/60 text-sm font-mono flex items-start gap-4">
                        <div className="flex-1">
                            <h4 className="uppercase tracking-widest mb-2 text-emerald-400">Controls</h4>
                            <ul className="space-y-1">
                                <li>[A] Start / Next Step</li>
                                <li>[0-9] Enter Numbers</li>
                                <li>[#] Confirm Input</li>
                                <li>[*] Clear / Backspace</li>
                                <li>[D] Reset System</li>
                            </ul>
                        </div>
                        <div className="flex-1">
                            <h4 className="uppercase tracking-widest mb-2 text-emerald-400">Status</h4>
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                                <span>Power ON</span>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
        </section>
    );
}
