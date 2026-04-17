import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { description, context } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a sound design expert specializing in procedural audio, game soundscapes, and AI-generated sound effects.' },
        { role: 'user', content: `Provide a comprehensive sound design exploration:\n\nTopic: ${description}\nContext: ${context}\n\nInclude:\n- Key concepts and techniques\n- AI tools and approaches relevant to ${context}\n- Real-world examples and case studies\n- Implementation tips for ${context} sound design\n- Technical considerations (FMOD, Wwise, etc.)\n- Future of AI sound design in ${context}` }],
      temperature: 0.8, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
