import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

export async function POST(req: NextRequest) {
  try {
    const { description } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are a professional music transcriber and music reader. Given a text description of audio, produce a detailed transcription in musical notation-style format.' },
        { role: 'user', content: `Based on the following audio description, produce a detailed music transcription:\n\n${description}\n\nInclude:\n- Tempo/BPM estimate\n- Time signature\n- Key signature\n- Chord progression (chord symbols and roman numerals)\n- Melody notes (staff-style or ASCII notation)\n- Rhythmic notation\n- Dynamics and expression markings\n- Instrumentation mapping\n- Structural sections (intro, verse, chorus, etc.)\n\nNote: This is an AI-assisted transcription based on your description. For real audio, use tools like Anthem or Audapolis.` },
      ],
      temperature: 0.7, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
