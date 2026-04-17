'use client';
import { useState } from 'react';
export default function MusicGenreTransfer() {
  const [description, setDescription] = useState('');
  const [targetGenre, setTargetGenre] = useState('jazz');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    if (!description.trim()) return;
    setLoading(true); setOutput('');
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ description, targetGenre }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error: Failed to generate transfer guide.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12"><div className="text-5xl mb-4">🎛️🔄</div><h1 className="text-3xl font-bold text-white mb-2">AI Music Genre Transfer</h1><p className="text-gray-400">Get AI music genre transfer suggestions with reference tracks and style notes</p></div>
        <div className="space-y-6 mb-8">
          <div><label className="block text-sm font-medium text-gray-300 mb-2">Original Music Description *</label><textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="e.g., A mid-tempo lo-fi track with vinyl crackle, Rhodes chord stabs, and a boom-bap drum pattern" rows={4} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500/60 focus:border-violet-500 transition resize-none" /></div>
          <div><label className="block text-sm font-medium text-gray-300 mb-2">Target Genre</label>
            <select value={targetGenre} onChange={e => setTargetGenre(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500/60 focus:border-violet-500 transition">
              <option value="jazz">Jazz</option><option value="classical">Classical</option><option value="electronic">Electronic / EDM</option><option value="orchestral">Orchestral / Cinematic</option><option value="rock">Rock</option><option value="synthwave">Synthwave</option><option value="afrobeats">Afrobeats</option><option value="bossa-nova">Bossa Nova</option>
            </select></div>
          <button onClick={handleGenerate} disabled={loading || !description.trim()} className="w-full py-4 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-violet-900/30">{loading ? '⏳ Generating Transfer Guide...' : '✨ Generate Transfer Guide'}</button>
        </div>
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">Genre Transfer Guide</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-violet-400 hover:text-violet-300 transition">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
