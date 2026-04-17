import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { episode, platform } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a social media content strategist specializing in podcast promotion and short-form video content.' },
        { role: 'user', content: `Based on the following podcast episode, generate ${platform === 'tiktok' ? '3-5 TikTok clip ideas' : platform === 'instagram' ? '3-5 Instagram Reels ideas' : platform === 'youtube' ? '3-5 YouTube Shorts ideas' : '3-5 social media clip ideas'}:\n\nEpisode: ${episode}\nPlatform: ${platform}\n\nFor each clip include:\n- Exact timestamp suggestion (if available from description)\n- Hook text (first 3 seconds — the attention grabber)\n- Caption text (for subtitles/accessibility)\n- 2-3 key talking points to extract\n- Suggested CTA (call to action)\n- Hashtag recommendations (5-10)\n- Estimated clip duration\n\nFormat each clip with clear headers.` }],
      temperature: 0.8, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
