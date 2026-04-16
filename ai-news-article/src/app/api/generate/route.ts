import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { topic, articleType, tone, length } = await req.json();

    const systemPrompt = "You are an expert journalist and news article writer. Generate a professional, well-structured news article.";

    const userPrompt = `Write a ${tone || "informative"} ${articleType || "news"} article about: ${topic}.\nLength: ${length || "medium"}. Include headline, subheadline, byline, lead paragraph, body sections, and closing.`;

    // Dynamic import to avoid build-time credential check
    const OpenAI = (await import("openai")).default;
    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
      baseURL: "https://api.deepseek.com/v1",
    });

    const completion = await getClient().chat.completions.create({
      model: "deepseek-chat",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      max_tokens: 1500,
      temperature: 0.7,
    });

    const article = completion.choices[0]?.message?.content || "No article generated.";
    return NextResponse.json({ article });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
