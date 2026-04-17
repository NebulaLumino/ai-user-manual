'use client';
import { useState } from 'react';
export default function SoundDesign() {
  const [description, setDescription] = useState('');
  const [context, setContext] = useState('game');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    if (!description.trim()) return;
    setLoading(true); setOutput('');
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ description, context }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error: Failed to generate sound design guide.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="text-center mb-12"><div className="text-5xl mb-4">🎮🔊</div><h1 className="text-3xl font-bold text-white mb-2">AI in Sound Design</h1><p className="text-gray-400">Explore procedural audio, AI-generated sound effects, and game soundscapes</p></div>
        <div className="space-y-6 mb-8">
          <div><label className="block text-sm font-medium text-gray-300 mb-2">Sound Concept *</label><textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="e.g., How can AI generate footstep sounds that adapt to different game surfaces in real time?" rows={4} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500/60 focus:border-orange-500 transition resize-none" /></div>
          <div><label className="block text-sm font-medium text-gray-300 mb-2">Context</label>
            <select value={context} onChange={e => setContext(e.target.value)} className="w-full px-4 py-3 bg-gray-800/60 border border-gray-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-500/60 focus:border-orange-500 transition">
              <option value="game">Game Audio</option><option value="film">Film / Video</option><option value="interactive">Interactive Installations</option><option value="vr">VR / XR</option>
            </select></div>
          <button onClick={handleGenerate} disabled={loading || !description.trim()} className="w-full py-4 bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-500 hover:to-amber-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg shadow-orange-900/30">{loading ? '⏳ Designing...' : '✨ Design Sound'}</button>
        </div>
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">Sound Design Guide</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-orange-400 hover:text-orange-300 transition">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
