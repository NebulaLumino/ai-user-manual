import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { description, format } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a generative music expert and algorithmic composition specialist.' },
        { role: 'user', content: `${format === 'history' ? 'Trace the history of algorithmic and generative music' : format === 'tools' ? 'Compare generative music tools and platforms' : format === 'future' ? 'Discuss future trends in generative AI music' : 'Provide a comprehensive overview'}:\n\nTopic: ${description}` }],
      temperature: 0.8, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
