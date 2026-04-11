import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
function getClient() { const apiKey = process.env.OPENAI_API_KEY; if (!apiKey) throw new Error("Missing OPENAI_API_KEY"); return new OpenAI({ apiKey, baseURL: "https://api.deepseek.com/v1" }); }
export async function POST(req: NextRequest) {
  try {
    const { prompt } = await req.json();
    const completion = await getClient().chat.completions.create({
      model: "deepseek-chat",
      messages: [{ role: "system", content: "You are a philanthropic giving strategist. Optimize charitable giving: 1) DAF (Donor Advised Fund) vs QCD (Qualified Charitable Distribution) comparison, 2) Tax deduction optimization, 3) Asset donation strategy (appreciated securities vs cash), 4) Giving circles and impact assessment, 5) Multi-year giving plan. Include dollar-specific recommendations and tax savings calculations." }, { role: "user", content: prompt }],
      temperature: 0.7, max_tokens: 2000,
    });
    return NextResponse.json({ result: completion.choices[0].message.content });
  } catch (err: any) { return NextResponse.json({ error: err.message }, { status: 500 }); }
}
