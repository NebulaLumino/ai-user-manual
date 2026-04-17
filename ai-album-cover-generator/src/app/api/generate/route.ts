import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

export async function POST(req: NextRequest) {
  try {
    const { description, genre, style } = await req.json();

    const client = new OpenAI({
      baseURL: 'https://api.deepseek.com/v1',
      apiKey: process.env.OPENAI_API_KEY,
    });

    const prompt = `You are a creative director and visual designer specializing in album artwork. Generate a comprehensive album cover design concept.

Music Description: ${description}
Genre: ${genre}
Visual Style: ${style}

Create a detailed design brief that includes:
- Concept overview (the visual story / metaphor)
- Color palette (5-7 specific colors with hex codes and emotional meaning)
- Typography suggestions (font styles, weights, placement)
- Imagery and illustration direction
- Layout and composition notes (front cover, back cover, spine)
- Mood board keywords for AI image generation tools
- Text elements to include (album title, artist name treatment)
- Reference artists/designers to look at
- Technical specs (dimensions, DPI, format for printing/CD/digital)
- Suggestions for cover variants or alternate versions
- Design tips for ensuring the cover works at small sizes (streaming thumbnails)`;

    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are an experienced creative director and visual artist with deep knowledge of album artwork trends across all music genres, from indie to major label releases.' },
        { role: 'user', content: prompt },
      ],
      temperature: 0.85,
      max_tokens: 2500,
    });

    const output = completion.choices[0]?.message?.content || 'No output generated.';
    return NextResponse.json({ output });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
