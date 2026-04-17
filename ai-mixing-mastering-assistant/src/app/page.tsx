'use client';

import { useState } from 'react';

export default function MixingMasteringAssistant() {
  const [genre, setGenre] = useState('electronic');
  const [stage, setStage] = useState('mixing');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setOutput('');
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ genre, stage }),
      });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch {
      setOutput('Error: Failed to generate checklist.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <div className="text-5xl mb-4">🎚️</div>
          <h1 className="text-3xl font-bold text-white mb-2">AI Mixing & Mastering Assistant</h1>
          <p className="text-gray-400">Get mixing and mastering checklists with EQ, compression, and loudness targets</p>
        </div>

        <div className="space-y-6 mb-8">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Genre</label>
              <select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-amber-500/60 focus:border-amber-500 transition"
              >
                <option value="electronic">Electronic / EDM</option>
                <option value="rock">Rock / Metal</option>
                <option value="hip-hop">Hip-Hop / Trap</option>
                <option value="pop">Pop</option>
                <option value="jazz">Jazz / Acoustic</option>
                <option value="classical">Classical / Orchestral</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Stage</label>
              <select
                value={stage}
                onChange={(e) => setStage(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-amber-500/60 focus:border-amber-500 transition"
              >
                <option value="mixing">Mixing</option>
                <option value="mastering">Mastering</option>
                <option value="full">Full Mix + Master Workflow</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full py-4 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-amber-900/30"
          >
            {loading ? '⏳ Generating Checklist...' : '✨ Get Mix/Master Checklist'}
          </button>
        </div>

        {output && (
          <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Production Checklist</h2>
              <button
                onClick={() => navigator.clipboard.writeText(output)}
                className="text-sm text-amber-400 hover:text-amber-300 transition"
              >
                📋 Copy
              </button>
            </div>
            <pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
