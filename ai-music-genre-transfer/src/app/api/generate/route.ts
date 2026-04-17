import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { description, targetGenre } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a music production specialist and genre transformation expert.' },
        { role: 'user', content: `Provide a comprehensive genre transfer plan:\n\nOriginal: ${description}\nTarget Genre: ${targetGenre}\n\nInclude:\n- Key harmonic/melodic changes needed\n- Instrumentation substitutions\n- Tempo and rhythm adjustments\n- Production techniques for ${targetGenre}\n- Reference tracks in ${targetGenre} that capture the essence\n- Specific EQ, compression, and effects changes\n- Texture and atmosphere modifications\n- AI tools suggestions for the transformation (Suno, Udio, LANDR, etc.)\n- Challenges and limitations of this specific transfer` }],
      temperature: 0.8, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
