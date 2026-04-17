import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { description, aspect } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are an intellectual property attorney specializing in music copyright, fair use doctrine, and AI training law.' },
        { role: 'user', content: `Explore music copyright law in the AI era ${aspect}:\n\nTopic: ${description}\n\nInclude legal frameworks, current cases, and practical guidance.` }],
      temperature: 0.7, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
