'use client';
import { useState } from 'react';

export default function Home() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleGenerate(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setOutput('');
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: input }),
    });
    const data = await res.json();
    setOutput(data.result || data.error || 'No response');
    setLoading(false);
  }

  return (
    <div className='min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col'>
      <div className='flex-1 flex flex-col items-center justify-center px-6 py-16'>
        <div className='w-full max-w-2xl'>
          <h1 className='text-3xl font-bold mb-2' style={{ color: 'hsl(145,70%,50%)' }}>Figure Caption Writer</h1>
          <p className='text-gray-400 mb-8'>Enter your input below.</p>
          <form onSubmit={handleGenerate} className='space-y-4'>
            <textarea
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder='Enter your input...'
              className='w-full bg-gray-800 border border-gray-700 rounded-lg p-4 text-white placeholder-gray-500 resize-none focus:outline-none focus:border-emerald-500'
              rows={6}
            />
            <button
              type='submit'
              disabled={loading}
              className='px-6 py-3 rounded-lg font-semibold text-white disabled:opacity-50'
              style={{ backgroundColor: 'hsl(145,70%,50%)' }}
            >
              {loading ? 'Generating...' : 'Generate'}
            </button>
          </form>
          {output && (
            <div className='mt-6 p-4 bg-gray-800 border border-gray-700 rounded-lg'>
              <pre className='whitespace-pre-wrap text-sm text-gray-200'>{output}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
