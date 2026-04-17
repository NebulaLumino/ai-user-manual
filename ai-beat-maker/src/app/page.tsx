'use client';
import { useState } from 'react';
export default function BeatMaker() {
  const [genre, setGenre] = useState('hip-hop');
  const [bpm, setBpm] = useState('90');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    setLoading(true); setOutput('');
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ genre, bpm }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error: Failed to generate beat.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12"><div className="text-5xl mb-4">🥁🎤</div><h1 className="text-3xl font-bold text-white mb-2">AI Beat Maker</h1><p className="text-gray-400">Generate beat patterns and rhythm ideas across hip-hop, trap, house, and more</p></div>
        <div className="space-y-6 mb-8">
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Genre</label>
              <select value={genre} onChange={e => setGenre(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-500/60 focus:border-orange-500 transition">
                <option value="hip-hop">Hip-Hop</option><option value="trap">Trap</option><option value="boom-bap">Boom Bap</option><option value="drill">Drill</option><option value="house">House</option><option value="phonk">Phonk</option><option value="jazz-hip-hop">Jazz Hip-Hop</option><option value="lo-fi">Lo-Fi</option>
              </select></div>
            <div><label className="block text-sm font-medium text-gray-300 mb-2">BPM</label>
              <select value={bpm} onChange={e => setBpm(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-500/60 focus:border-orange-500 transition">
                <option value="60">60 (Slow / Melodic)</option><option value="75">75 (Lo-Fi / Chill)</option><option value="85">85 (Boom Bap)</option><option value="90">90 (Classic Hip-Hop)</option><option value="100">100 (Trap / Modern)</option><option value="140">140 (Phonk / DnB)</option>
              </select></div>
          </div>
          <button onClick={handleGenerate} disabled={loading} className="w-full py-4 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-orange-900/30">{loading ? '⏳ Making Beat...' : '✨ Make a Beat'}</button>
        </div>
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">Beat Pattern</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-orange-400 hover:text-orange-300 transition">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
