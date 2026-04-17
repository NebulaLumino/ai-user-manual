import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { theme, vibe, length } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const trackCount = length === 'short' ? 12 : length === 'medium' ? 25 : length === 'long' ? 45 : 55;
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a music curator and playlist producer with deep knowledge of music across all genres and eras.' },
        { role: 'user', content: `Curate a playlist:\n\nTheme: ${theme}\nVibe: ${vibe}\nLength: ${length} (${trackCount} tracks)\n\nInclude:\n- Playlist name and description\n- Flow narrative (how the playlist moves emotionally)\n- ${trackCount} tracks with: artist name, song title, release year\n- Balanced across eras and subgenres\n- BPM range indicator for the whole playlist\n- Musical key/mood diversity\n- Streaming platform compatibility notes\n- Suggested listening contexts\n- Hidden gems alongside obvious hits\n\nMix known and obscure tracks. Think like a professional DJ/curator.` }],
      temperature: 0.8, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
