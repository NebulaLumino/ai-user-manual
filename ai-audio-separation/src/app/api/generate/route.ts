import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { description } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are an audio source separation expert with deep knowledge of AI models like Demucs, Spleeter, UVR5, and audio engineering.' },
        { role: 'user', content: `Provide a comprehensive guide on AI audio source separation:\n\nGoal: ${description}\n\nInclude:\n- Best AI separation tools ranked by quality (Demucs v4, Spleeter, LALAL.AI, Moises, UVR5)\n- Which tool is best for this specific goal\n- Step-by-step workflow\n- Quality considerations and limitations\n- Post-processing tips to improve results\n- File format requirements\n- Ethical/legal considerations for using separated stems\n- Tips for the specific audio type described` }],
      temperature: 0.7, max_tokens: 2000,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
