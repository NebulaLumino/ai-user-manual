'use client';
import { useState } from 'react';
export default function MusicBPMTapper() {
  const [taps, setTaps] = useState<number[]>([]);
  const [bpm, setBpm] = useState<number | null>(null);
  const [suggestedKey, setSuggestedKey] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const handleTap = () => {
    const now = Date.now();
    const newTaps = [...taps, now];
    if (newTaps.length > 1) {
      const intervals: number[] = [];
      for (let i = 1; i < newTaps.length; i++) intervals.push(newTaps[i] - newTaps[i-1]);
      const avgMs = intervals.reduce((a, b) => a + b, 0) / intervals.length;
      const calcBpm = Math.round(60000 / avgMs);
      if (calcBpm >= 40 && calcBpm <= 220) { setBpm(calcBpm); const keys = ['4B','11B','6B','1B','8B','3B','10B','5B','12B','7B','2B','9B','4A','11A','6A','1A','8A','3A','10A','5A','12A','7A','2A','9A']; setSuggestedKey(keys[calcBpm % 24] || '8B'); }
    }
    setTaps(newTaps.slice(-20));
  };
  const handleReset = () => { setTaps([]); setBpm(null); setSuggestedKey(''); };
  const handleSuggest = async () => {
    if (!bpm) return;
    setLoading(true);
    try {
      const res = await fetch('/api/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ bpm, suggestedKey }) });
      const data = await res.json();
      setOutput(data.output || data.error || 'No response generated.');
    } catch { setOutput('Error.'); }
    setLoading(false);
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black text-white">
      <div className="max-w-2xl mx-auto px-6 py-16 text-center">
        <div className="text-5xl mb-4">🎵⏱️</div><h1 className="text-3xl font-bold text-white mb-2">AI BPM Tapper</h1><p className="text-gray-400 mb-12">Tap to the beat to find BPM and compatible keys</p>
        <div className="mb-8"><div className="text-7xl font-bold text-cyan-400 font-mono mb-4">{bpm ? `${bpm} BPM` : '— BPM'}</div>{suggestedKey && <div className="text-xl text-gray-400 mb-2">Suggested Key: <span className="text-cyan-400 font-bold">{suggestedKey}</span></div>}<div className="text-sm text-gray-500">{taps.length} taps</div></div>
        <div className="flex gap-4 justify-center mb-12">
          <button onClick={handleTap} className="px-16 py-6 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-2xl text-2xl shadow-lg shadow-cyan-900/40 transition-all active:scale-95">TAP</button>
          <button onClick={handleReset} className="px-8 py-6 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-2xl transition">Reset</button>
        </div>
        {bpm && <button onClick={handleSuggest} disabled={loading} className="w-full py-4 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-lg mb-6 shadow-lg shadow-amber-900/30">{loading ? '⏳ Getting Suggestions...' : '✨ Get DJ Set Suggestions'}</button>}
        {output && <div className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6 text-left"><div className="flex items-center justify-between mb-4"><h2 className="text-lg font-semibold text-white">DJ Suggestions</h2><button onClick={() => navigator.clipboard.writeText(output)} className="text-sm text-amber-400 hover:text-amber-300">📋 Copy</button></div><pre className="whitespace-pre-wrap text-gray-300 text-sm font-mono bg-gray-900/50 rounded-xl p-4 border border-gray-700/50 overflow-x-auto">{output}</pre></div>}
      </div>
    </div>
  );
}
