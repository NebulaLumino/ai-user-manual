'use client';
import { useState } from 'react';
export default function MusicPlaylistCurator() {
  const [theme, setTheme] = useState('');
  const [vibe, setVibe] = useState('focused');
  const [length, setLength] = useState('medium');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    if (!theme.trim()) return;
    setLoading(true); setOutput('');
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ theme, vibe, length }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error: Failed to generate playlist.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12"><div className="text-5xl mb-4">📋🎶</div><h1 className="text-3xl font-bold text-white mb-2">AI Music Playlist Curator</h1><p className="text-gray-400">Generate themed playlists with track descriptions, BPM ranges, and key info</p></div>
        <div className="space-y-6 mb-8">
          <div><label className="block text-sm font-medium text-gray-300 mb-2">Playlist Theme / Occasion *</label><input type="text" value={theme} onChange={e => setTheme(e.target.value)} placeholder="e.g., Late night coding sessions, rainy day reading, summer road trip" className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-pink-500/60 focus:border-pink-500 transition" /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Vibe</label>
              <select value={vibe} onChange={e => setVibe(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-pink-500/60 focus:border-pink-500 transition">
                <option value="focused">Focus / Work</option><option value="chill">Chill / Relaxed</option><option value="energizing">Energizing / Workout</option><option value="romantic">Romantic / Date Night</option><option value="nostalgic">Nostalgic / Throwback</option><option value="adventurous">Adventurous / Travel</option>
              </select></div>
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Playlist Length</label>
              <select value={length} onChange={e => setLength(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-pink-500/60 focus:border-pink-500 transition">
                <option value="short">Short (10-15 tracks)</option><option value="medium">Medium (20-30 tracks)</option><option value="long">Long (40-50 tracks)</option><option value="epic">Epic (50+ tracks)</option>
              </select></div>
          </div>
          <button onClick={handleGenerate} disabled={loading || !theme.trim()} className="w-full py-4 bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-500 hover:to-rose-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-pink-900/30">{loading ? '⏳ Curating Playlist...' : '✨ Curate Playlist'}</button>
        </div>
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">Curated Playlist</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-pink-400 hover:text-pink-300 transition">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
