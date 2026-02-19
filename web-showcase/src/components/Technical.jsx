import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Simulate the comparison data for visualization
const data = Array.from({ length: 20 }, (_, i) => {
    const x = i * 5;
    const true_val = 2 * x + 10;
    // OLS gets pulled by outliers (simulated)
    const ols_pred = 2.5 * x + 5;
    // Huber stays closer to true trend
    const huber_pred = 2.1 * x + 9;

    return {
        name: x,
        "Standard OLS": ols_pred,
        "Robust Huber": huber_pred,
        "True Trend": true_val
    };
});

// Export the component as default
export default function Technical() {
    return (
        <section id="technical" className="py-20 px-6 bg-slate-950">
            <div className="max-w-6xl mx-auto">
                <div className="mb-12 text-center">
                    <h2 className="text-3xl font-bold mb-4">Why Robust Regression?</h2>
                    <p className="text-slate-400 max-w-2xl mx-auto">
                        Traditional Linear Regression (OLS) minimizes Mean Squared Error, which heavily penalizes large errors.
                        This makes it sensitive to outliers (like fraudulent claims).
                        Our <span className="text-blue-400 font-semibold">Huber Loss</span> model is linear for small errors but linear (not quadratic) for large errors,
                        making it robust against anomalies.
                    </p>
                </div>

                <div className="bg-slate-900 p-6 md:p-8 rounded-2xl border border-slate-800 shadow-xl">
                    <div className="h-[400px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                                <XAxis dataKey="name" stroke="#64748b" label={{ value: 'Input Feature (e.g., BMI)', position: 'insideBottom', offset: -5 }} />
                                <YAxis stroke="#64748b" label={{ value: 'Claim Amount', angle: -90, position: 'insideLeft' }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }}
                                />
                                <Legend />
                                <Line type="monotone" dataKey="True Trend" stroke="#94a3b8" strokeDasharray="5 5" dot={false} strokeWidth={2} />
                                <Line type="monotone" dataKey="Standard OLS" stroke="#ef4444" strokeWidth={2} />
                                <Line type="monotone" dataKey="Robust Huber" stroke="#3b82f6" strokeWidth={3} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                    <p className="text-center text-sm text-slate-500 mt-4">
                        Visualization: OLS (Red) gets pulled away by outliers, while Huber (Blue) sticks to the true trend.
                    </p>
                </div>
            </div>
        </section>
    );
}
