import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { description, aspect } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a voice synthesis and neural TTS expert with deep knowledge of WaveNet, voice cloning, and real-time voice conversion.' },
        { role: 'user', content: `Explore voice synthesis ${aspect}:\n\nTopic: ${description}\n\nInclude technical depth, real examples, and practical insights.` }],
      temperature: 0.8, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
