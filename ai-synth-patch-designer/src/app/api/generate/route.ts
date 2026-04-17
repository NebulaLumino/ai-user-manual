import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { description, synth } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: `You are a professional sound designer and synthesizer expert. Provide detailed, implementable patch designs for ${synth} and similar synths.` },
        { role: 'user', content: `Design a synthesizer patch:\n\nSound: ${description}\nTarget Synth: ${synth}\n\nInclude:\n- OSCILLATORS: Waveform selection, octave, detune, mix\n- FILTER: Cutoff frequency, resonance, filter type, envelope modulation amount\n- AMPLITUDE ENVELOPE: ADSR settings with rationale\n- FILTER ENVELOPE: ADSR with modulation routing\n- MODULATION: LFO settings, assignments, macro assignments\n- EFFECTS: Suggested onboard or external effects\n- PERFORMANCE TIPS: Macros, aftertouch, mod wheel uses\n- Quick tips for recreating this in ${synth === 'serum' ? 'Xfer Serum' : synth === 'analog' ? 'any analog/subtractive synth' : synth} specifically` }],
      temperature: 0.8, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
