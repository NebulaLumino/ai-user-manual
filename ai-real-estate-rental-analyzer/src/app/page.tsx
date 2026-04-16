'use client';

import { useState } from 'react';

function renderMarkdown(text: string) {
  const lines = text.split('\n');
  const elems: React.ReactNode[] = [];
  let inUl = false;
  let liBuffer: string[] = [];

  function flushUl() {
    if (liBuffer.length > 0) {
      elems.push(
        <ul key={'ul-' + elems.length} className="list-disc pl-5 space-y-1 my-3">
          {liBuffer.map((c, i) => <li key={i} className="text-slate-300">{c}</li>)}
        </ul>
      );
      liBuffer = [];
    }
    inUl = false;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) { elems.push(<br key={'br-' + i} />); flushUl(); continue; }
    if (line.startsWith('## ')) { flushUl(); elems.push(<h2 key={'h2-' + i} className="text-xl font-semibold text-amber-400 mt-4 mb-2">{line.slice(3)}</h2>); continue; }
    if (line.startsWith('# ')) { flushUl(); elems.push(<h1 key={'h1-' + i} className="text-2xl font-bold text-white mb-3">{line.slice(2)}</h1>); continue; }
    if (line.startsWith('- ') || line.startsWith('* ')) { inUl = true; liBuffer.push(line.slice(2)); continue; }
    if (inUl && !line.startsWith('- ') && !line.startsWith('* ')) { flushUl(); }
    elems.push(<p key={'p-' + i} className="text-slate-300 my-1">{line}</p>);
  }
  flushUl();
  return elems;
}

export default function Home() {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const data = new FormData(form);
    const prompt = `You are an expert financial advisor. {data.get('context') || 'Provide detailed financial analysis.'}`;
    setLoading(true);
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const json = await res.json();
      setResult(json.result || json.error || 'No response.');
    } catch (err: any) {
      setResult('Error: ' + err.message);
    }
    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white p-6">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 text-amber-400">Real Estate Rental Analyzer</h1>
          <p className="text-slate-400 text-lg">Analyze rental property investment: cap rate, cash flow, and ROI</p>
        </div>
        <form onSubmit={handleSubmit} className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-2xl p-6 mb-6 space-y-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-slate-300">Your Financial Situation</label>
            <textarea
              name="context"
              rows={5}
              className="bg-slate-800/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 resize-none"
              placeholder="Describe your financial situation and goals..."
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 rounded-xl font-semibold text-white transition-all ${loading ? 'bg-slate-700/60 cursor-not-allowed opacity-60' : 'bg-amber-600 hover:bg-amber-500 hover:shadow-lg hover:shadow-amber-500/20 cursor-pointer'}`}
          >
            {loading ? 'Analyzing...' : 'Get AI Analysis'}
          </button>
        </form>
        {result && (
          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-2xl p-6">
            <div className="text-slate-100">{renderMarkdown(result)}</div>
          </div>
        )}
      </div>
    </div>
  );
}
