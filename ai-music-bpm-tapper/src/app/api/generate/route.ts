import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { bpm, suggestedKey } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a professional DJ with extensive knowledge of music theory and harmonic mixing.' },
        { role: 'user', content: `Provide DJ set suggestions for:\n\nDetected BPM: ${bpm}\nSuggested Key: ${suggestedKey}\n\nInclude:\n- 5-7 track recommendations harmonically mixed (Camelot-compatible keys)\n- Mix-in and mix-out points between tracks\n- Energy progression\n- Genre variations that work at this tempo\n- Tips for mixing in key at ${bpm} BPM\n- Sample DJ mix structure` }],
      temperature: 0.8, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
