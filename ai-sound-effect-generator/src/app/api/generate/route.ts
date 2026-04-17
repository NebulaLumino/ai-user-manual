import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

export async function POST(req: NextRequest) {
  try {
    const { description, context, type } = await req.json();

    const client = new OpenAI({
      baseURL: 'https://api.deepseek.com/v1',
      apiKey: process.env.OPENAI_API_KEY,
    });

    const prompt = `You are a professional sound designer and foley artist. Generate detailed sound effect specifications and creative suggestions for the following:

Sound Description: ${description}
Production Context: ${context}
Sound Type Preference: ${type}

Create a comprehensive sound design document that includes:
- Sound concept and creative vision
- Detailed layer breakdown (what sounds to combine)
- ${type === 'foley' ? 'Foley recording techniques and materials needed' : type === 'field' ? 'Field recording location suggestions and equipment tips' : type === 'synthesized' ? 'Synthesis approach (subtractive, FM, granular, etc.)' : 'Hybrid approach combining recorded and synthesized elements'}
- Technical specifications (frequency range, stereo width, dynamics)
- Reference timing and spatial placement
- Post-processing suggestions (EQ, compression, reverb, saturation)
- How to make it sound ${context === 'film' ? 'cinematic and impactful' : context === 'game' ? 'interactive and responsive to gameplay' : 'engaging and immersive'}
- Tips for avoiding common pitfalls
- Alternative approaches for budget or time constraints
- Surround/immersive audio considerations if relevant`;

    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are a professional sound designer with expertise in foley, sound effects creation, field recording, and sound synthesis for film, games, and media. You provide technically precise, creatively rich sound design briefs.' },
        { role: 'user', content: prompt },
      ],
      temperature: 0.8,
      max_tokens: 2000,
    });

    const output = completion.choices[0]?.message?.content || 'No output generated.';
    return NextResponse.json({ output });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
