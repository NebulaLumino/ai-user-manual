'use client';
import { useState } from 'react';
export default function SoundscapeGenerator() {
  const [scene, setScene] = useState('forest');
  const [duration, setDuration] = useState('10');
  const [mood, setMood] = useState('peaceful');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    setLoading(true); setOutput('');
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scene, duration, mood }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error: Failed to generate soundscape.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12"><div className="text-5xl mb-4">🌿🔊</div><h1 className="text-3xl font-bold text-white mb-2">AI Soundscape Generator</h1><p className="text-gray-400">Generate ambient soundscapes for games, film, and focus sessions with layer descriptions</p></div>
        <div className="space-y-6 mb-8">
          <div className="grid grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Scene / Environment</label>
              <select value={scene} onChange={e => setScene(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-teal-500/60 focus:border-teal-500 transition">
                <option value="forest">Forest / Nature</option><option value="ocean">Ocean / Beach</option><option value="city">City / Urban</option><option value="space">Space / Cosmic</option><option value="rain">Rain / Storm</option><option value="fantasy">Fantasy / Magical</option><option value="underwater">Underwater</option><option value="mountain">Mountain / Wind</option>
              </select></div>
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Duration</label>
              <select value={duration} onChange={e => setDuration(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-teal-500/60 focus:border-teal-500 transition">
                <option value="5">5 minutes</option><option value="10">10 minutes</option><option value="20">20 minutes</option><option value="30">30 minutes</option><option value="60">1 hour</option>
              </select></div>
            <div><label className="block text-sm font-medium text-gray-300 mb-2">Mood</label>
              <select value={mood} onChange={e => setMood(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-teal-500/60 focus:border-teal-500 transition">
                <option value="peaceful">Peaceful</option><option value="mysterious">Mysterious</option><option value="tense">Tense / Ominous</option><option value="magical">Magical / Ethereal</option><option value="melancholic">Melancholic</option><option value="energizing">Energizing</option>
              </select></div>
          </div>
          <button onClick={handleGenerate} disabled={loading} className="w-full py-4 bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-500 hover:to-cyan-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-teal-900/30">{loading ? '⏳ Composing Soundscape...' : '✨ Generate Soundscape'}</button>
        </div>
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">Soundscape Design</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-teal-400 hover:text-teal-300 transition">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
