import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { genre, mood, tempo } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a sample pack curator and music producer with deep knowledge of sound libraries across all genres.' },
        { role: 'user', content: `Find sample recommendations:\n\nGenre: ${genre}\nMood: ${mood}\nBPM: ${tempo}\n\nInclude:\n- 10 recommended sample packs (name + where to find them)\n- For each pack: type of content, quality rating, price tier\n- Specific one-shot recommendations (kicks, snares, hi-hats, percussion)\n- Loop recommendations (melodic loops, textural loops)\n- Serum/Wavetable suggestions\n- Free vs paid options balanced\n- Where to source ethically (to avoid copyright issues)\n- Tips for layering and processing samples` }],
      temperature: 0.8, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
