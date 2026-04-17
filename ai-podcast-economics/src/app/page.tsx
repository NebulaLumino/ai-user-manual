'use client';
import { useState } from 'react';
export default function PodcastEconomics() {
  const [description, setDescription] = useState('');
  const [aspect, setAspect] = useState('overview');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    if (!description.trim()) return;
    setLoading(true); setOutput('');
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ description, aspect }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error: Failed to generate content.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12"><div className="text-5xl mb-4">💰🎙️</div><h1 className="text-3xl font-bold text-white mb-2">Podcast Economics Explorer</h1><p className="text-gray-400">Explore podcast sponsorships, CPM models, listener behavior, and growth strategies</p></div>
        <div className="space-y-6 mb-8">
          <div><label className="block text-sm font-medium text-gray-300 mb-2">Topic *</label><input type="text" value={description} onChange={e => setDescription(e.target.value)} placeholder="e.g., How much do podcasters earn per listener at 10,000 downloads per episode?" className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/60 focus:border-emerald-500 transition" /></div>
          <div><label className="block text-sm font-medium text-gray-300 mb-2">Aspect</label>
            <select value={aspect} onChange={e => setAspect(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/60 focus:border-emerald-500 transition">
              <option value="overview">Economics Overview</option><option value="sponsorships">Sponsorship Models</option><option value="growth">Growth Strategies</option><option value="monetization">Monetization Pathways</option>
            </select></div>
          <button onClick={handleGenerate} disabled={loading || !description.trim()} className="w-full py-4 bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-500 hover:to-green-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-emerald-900/30">{loading ? '⏳ Generating...' : '✨ Explore Podcast Economics'}</button>
        </div>
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">Output</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-emerald-400 hover:text-emerald-300 transition">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
