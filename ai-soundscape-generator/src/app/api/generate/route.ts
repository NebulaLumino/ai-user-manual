import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { scene, duration, mood } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a professional sound designer specializing in ambient, game, and film soundscapes.' },
        { role: 'user', content: `Design a ${duration}-minute ambient soundscape:\n\nScene: ${scene}\nMood: ${mood}\nDuration: ${duration} minutes\n\nInclude:\n- Sound design concept and narrative arc\n- Layer breakdown (foreground, midground, background elements)\n- Suggested sources for each layer (field recording, synthesis, sample libraries)\n- How the soundscape evolves over ${duration} minutes (dynamic arc)\n- Reverb and spatialization settings\n- EQ and filtering suggestions\n- Tools and plugins to use ( Ableton Live, Kontakt, Max/MSP, etc.)\n- Specific techniques for creating the ${scene} atmosphere\n- Tips for making it loop seamlessly or transition naturally` }],
      temperature: 0.8, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
