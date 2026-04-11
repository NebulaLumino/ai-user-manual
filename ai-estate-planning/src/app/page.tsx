"use client";
import { useState } from "react";
export default function Home() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    if (!input.trim()) return;
    setLoading(true); setOutput("");
    try {
      const res = await fetch("/api/generate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ prompt: input }) });
      const data = await res.json();
      setOutput(data.result || "No output received.");
    } catch { setOutput("Error generating response."); }
    finally { setLoading(false); }
  };
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold" style="color: hsl(215,45%,55%)">Estate Planning</h1>
          <p className="text-gray-400">Estate planning checklist generator</p>
        </div>
        <div className="bg-gray-800/60 border rounded-2xl p-6 space-y-4 shadow-xl" style="border-color: hsla(215,45%,55%, 0.3)">
          <label className="block text-sm font-medium text-gray-300">Enter your details</label>
          <textarea className="w-full h-40 bg-gray-900/80 border border-gray-700 rounded-xl p-4 text-white text-sm placeholder-gray-500 focus:outline-none resize-none"
            placeholder="Describe your financial situation, goals, and specific parameters..."
            value={input} onChange={(e) => setInput(e.target.value)} />
          <button onClick={handleGenerate} disabled={loading || !input.trim()}
            className="w-full text-white font-semibold py-3 rounded-xl transition-colors disabled:cursor-not-allowed disabled:opacity-50"
            style="background-color: hsl(215,45%,55%)">
            {loading ? "Generating..." : "Generate Analysis"}
          </button>
        </div>
        {output && (
          <div className="bg-gray-800/60 border rounded-2xl p-6" style="border-color: hsla(215,45%,55%, 0.3)">
            <h2 className="text-lg font-semibold mb-3" style="color: hsl(215,45%,55%)">Results</h2>
            <div className="prose prose-invert prose-sm max-w-none text-gray-300 whitespace-pre-wrap">{output}</div>
          </div>
        )}
      </div>
    </main>
  );
}
