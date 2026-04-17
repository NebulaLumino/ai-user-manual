import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';
export async function POST(req: NextRequest) {
  try {
    const { task } = await req.json();
    const client = new OpenAI({ baseURL: 'https://api.deepseek.com/v1', apiKey: process.env.OPENAI_API_KEY });
    const taskGuides: Record<string, string> = {
      'podcast-edit': 'Standard podcast post-production workflow',
      'interview-edit': 'Interview-specific editing with cross-talk handling',
      'music-edit': 'Music track cleanup and arrangement editing',
      'video-sync': 'Video synchronization and audio sync workflow',
      'restoration': 'Audio restoration and noise reduction',
    };
    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'system', content: 'You are a professional audio engineer with expertise in podcast, music, and video post-production workflows.' },
        { role: 'user', content: `Create a comprehensive audio editing checklist for: ${taskGuides[task] || task}\n\nInclude:\n- Phase-by-phase workflow (step by step numbered list)\n- Essential software tools for each phase\n- Specific keyboard shortcuts (Adobe Audition, Logic, Pro Tools, Audacity)\n- Common mistakes to avoid\n- Estimated time per phase\n- Export settings for final delivery\n- Quality control checkpoints` }],
      temperature: 0.7, max_tokens: 2500,
    });
    return NextResponse.json({ output: completion.choices[0]?.message?.content || 'No output generated.' });
  } catch (error: unknown) {
    return NextResponse.json({ error: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 });
  }
}
