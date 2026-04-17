import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

export async function POST(req: NextRequest) {
  try {
    const { songDescription, quality, outputFormat } = await req.json();

    const client = new OpenAI({
      baseURL: 'https://api.deepseek.com/v1',
      apiKey: process.env.OPENAI_API_KEY,
    });

    const prompt = `You are an expert audio separation specialist. Provide detailed, step-by-step instructions for removing/isolating vocals from a music track using AI audio separation tools.

Song/Track Description: ${songDescription}
Source Quality: ${quality}
Desired Output: ${outputFormat}

Create a comprehensive guide that includes:
- Recommended AI separation tools ranked by quality for this use case
  (Demucs v4, Spleeter, UVR5, LALAL.AI, Moises, Lalal.ai, etc.)
- Step-by-step instructions for the top 2 recommended tools
- File format requirements (WAV vs MP3, bitrate considerations)
- How to handle the specific challenges of this track (based on description)
- Pre-processing steps (normalizing, converting format)
- Post-processing to improve stem quality (EQ adjustments, reverb reduction)
- How to handle bleed/crosstalk in the separated stems
- Volume balancing the stems for best results
- Common pitfalls and how to avoid them
- Export settings for the final output
- Tips for getting the cleanest possible ${outputFormat} result`;

    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are an audio engineering specialist with deep expertise in AI-powered audio source separation, stem extraction, and music production workflows.' },
        { role: 'user', content: prompt },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    });

    const output = completion.choices[0]?.message?.content || 'No output generated.';
    return NextResponse.json({ output });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
