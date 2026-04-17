import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

export async function POST(req: NextRequest) {
  try {
    const { genre, stage } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are a professional mixing and mastering engineer with platinum credits across multiple genres.' },
        { role: 'user', content: `Create a detailed mixing and mastering checklist for:\n\nGenre: ${genre}\nStage: ${stage}\n\n${stage === 'mixing' || stage === 'full' ? '## MIXING CHECKLIST\n\nInclude:\n- Reference track selection (2-3 suggested reference tracks for ${genre})\n- Signal chain setup\n- EQ checklist (frequency hunting per instrument)\n- Compression settings per track group\n- Reverb and delay send setup\n- Stereo field placement\n- Volume automation\n- Group bus processing\n- Final mix checks (mono compatibility, translation test)\n' : ''}\n\n${stage === 'mastering' || stage === 'full' ? '## MASTERING CHECKLIST\n\nInclude:\n- LUFS loudness target for ${genre} on streaming platforms\n- EQ adjustments (corrective)\n- Compression/limiting strategy\n- Stereo width optimization\n- Harmonic saturation suggestions\n- Dithering and sample rate\n- Codec comparison check\n' : ''}\n\nProvide specific Hz values, dB targets, and plugin suggestions where possible.` },
      ],
      temperature: 0.7, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
