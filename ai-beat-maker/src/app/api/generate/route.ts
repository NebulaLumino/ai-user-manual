import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { genre, bpm } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a professional beat maker and drum programmer with credits across hip-hop, trap, and electronic genres.' },
        { role: 'user', content: `Create a complete beat specification:\n\nGenre: ${genre}\nBPM: ${bpm}\n\nInclude:\n- BPM confirmation and time signature\n- Kick pattern (bar 1-4)\n- Snare/Clap pattern\n- Hi-hat pattern (closed and open)\n- 808 / bass pattern suggestion\n- Melodic element suggestion (keys, 808 bassline)\n- Full drum pattern in text notation (X = hit, - = rest)\n- Sample recommendations (specific one-shots and loops)\n- DAW workflow tips for ${genre}\n- Mix-down tips specific to this beat type\n- Reference tracks for feel and sonics` }],
      temperature: 0.85, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
