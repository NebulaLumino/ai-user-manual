import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
function getClient() { const apiKey = process.env.OPENAI_API_KEY; if (!apiKey) throw new Error("Missing OPENAI_API_KEY"); return new OpenAI({ apiKey, baseURL: "https://api.deepseek.com/v1" }); }
export async function POST(req: NextRequest) {
  try {
    const { prompt } = await req.json();
    const completion = await getClient().chat.completions.create({
      model: "deepseek-chat",
      messages: [{ role: "system", content: "You are a personal finance advisor specializing in emergency planning. Help users build and maintain emergency funds: 1) Target fund size based on expenses and risk factors, 2) Monthly savings roadmap to reach goal, 3) Best account types for emergency funds (HYSA vs money market), 4) Trigger conditions for using the fund, 5) Replenishment strategy after use. Include specific savings targets and timeline." }, { role: "user", content: prompt }],
      temperature: 0.7, max_tokens: 2000,
    });
    return NextResponse.json({ result: completion.choices[0].message.content });
  } catch (err: any) { return NextResponse.json({ error: err.message }, { status: 500 }); }
}
