'use client';
import { useState } from 'react';
export default function MusicSampleFinder() {
  const [genre, setGenre] = useState('lo-fi');
  const [mood, setMood] = useState('chill');
  const [tempo, setTempo] = useState('90-100');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    setLoading(true); setOutput('');
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ genre, mood, tempo }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error: Failed to find samples.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12"><div className="text-5xl mb-4">🔍🎵</div><h1 className="text-3xl font-bold text-white mb-2">AI Music Sample Finder</h1><p className="text-gray-400">Get sample pack recommendations based on genre, mood, and tempo</p></div>
        <div className="space-y-6 mb-8">
          <div className="grid grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Genre</label>
              <select value={genre} onChange={e => setGenre(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-pink-500/60 focus:border-pink-500 transition">
                <option value="lo-fi">Lo-Fi / Chillhop</option><option value="hip-hop">Hip-Hop / Trap</option><option value="house">House / Techno</option><option value="orchestral">Orchestral / Cinematic</option><option value="world">World / Organic</option><option value="electronic">Electronic / Synthwave</option>
              </select></div>
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Mood</label>
              <select value={mood} onChange={e => setMood(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-pink-500/60 focus:border-pink-500 transition">
                <option value="chill">Chill / Relaxed</option><option value="dark">Dark / Moody</option><option value="uplifting">Uplifting / Bright</option><option value="epic">Epic / Dramatic</option><option value="nostalgic">Nostalgic / Vintage</option><option value="energetic">Energetic / Aggressive</option>
              </select></div>
            <div><label className="block text-sm font-medium text-gray-300 mb-2">BPM Range</label>
              <select value={tempo} onChange={e => setTempo(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-pink-500/60 focus:border-pink-500 transition">
                <option value="60-80">60-80 (Slow / Deep)</option><option value="80-95">80-95 (Mid-Tempo)</option><option value="90-100">90-100 (Lo-Fi)</option><option value="120-130">120-130 (House)</option><option value="140+">140+ (Trap / DnB)</option>
              </select></div>
          </div>
          <button onClick={handleGenerate} disabled={loading} className="w-full py-4 bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-500 hover:to-rose-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-pink-900/30">{loading ? '⏳ Finding Samples...' : '✨ Find Samples'}</button>
        </div>
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">Sample Recommendations</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-pink-400 hover:text-pink-300 transition">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
