'use client';

import { useState } from 'react';

export default function VocalRemover() {
  const [songDescription, setSongDescription] = useState('');
  const [quality, setQuality] = useState('high');
  const [outputFormat, setOutputFormat] = useState('stems');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!songDescription.trim()) return;
    setLoading(true);
    setOutput('');
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ songDescription, quality, outputFormat }),
      });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch {
      setOutput('Error: Failed to generate vocal removal guide.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <div className="text-5xl mb-4">🎤❌</div>
          <h1 className="text-3xl font-bold text-white mb-2">AI Vocal Remover Guide</h1>
          <p className="text-gray-400">Get step-by-step instructions for vocal isolation using AI audio separation tools</p>
        </div>

        <div className="space-y-6 mb-8">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Song / Track Description *</label>
            <textarea
              value={songDescription}
              onChange={(e) => setSongDescription(e.target.value)}
              placeholder="e.g., Pop song with heavy instrumentation, some reverb on vocals, stereo mix"
              rows={4}
              className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500/60 focus:border-yellow-500 transition resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Source Quality</label>
              <select
                value={quality}
                onChange={(e) => setQuality(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-yellow-500/60 focus:border-yellow-500 transition"
              >
                <option value="high">High (320kbps / WAV)</option>
                <option value="medium">Medium (128-256kbps)</option>
                <option value="low">Low (YouTube / low-res)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Desired Output</label>
              <select
                value={outputFormat}
                onChange={(e) => setOutputFormat(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-yellow-500/60 focus:border-yellow-500 transition"
              >
                <option value="stems">Instrumental Stems</option>
                <option value="vocals-only">Vocals Only (Acapella)</option>
                <option value="drums-only">Drums Only</option>
                <option value="bass-only">Bass Only</option>
                <option value="all">All Separated Stems</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !songDescription.trim()}
            className="w-full py-4 bg-gradient-to-r from-yellow-600 to-lime-600 hover:from-yellow-500 hover:to-lime-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-yellow-900/30"
          >
            {loading ? '⏳ Generating Guide...' : '✨ Get Vocal Removal Guide'}
          </button>
        </div>

        {output && (
          <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Vocal Removal Guide</h2>
              <button
                onClick={() => navigator.clipboard.writeText(output)}
                className="text-sm text-yellow-400 hover:text-yellow-300 transition"
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
