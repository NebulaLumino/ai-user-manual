import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
function getClient() { const apiKey = process.env.OPENAI_API_KEY; if (!apiKey) throw new Error("Missing OPENAI_API_KEY"); return new OpenAI({ apiKey, baseURL: "https://api.deepseek.com/v1" }); }
export async function POST(req: NextRequest) {
  try {
    const { prompt } = await req.json();
    const completion = await getClient().chat.completions.create({
      model: "deepseek-chat",
      messages: [{ role: "system", content: "You are an estate planning attorney and financial advisor. Generate a comprehensive estate planning checklist: 1) Will and testament review, 2) Beneficiary designations audit, 3) Power of attorney setup, 4) Healthcare directives, 5) Trust strategies (revocable vs irrevocable), 6) Estate tax minimization, 7) Digital asset planning. Include state-specific considerations and priority ordering." }, { role: "user", content: prompt }],
      temperature: 0.7, max_tokens: 2000,
    });
    return NextResponse.json({ result: completion.choices[0].message.content });
  } catch (err: any) { return NextResponse.json({ error: err.message }, { status: 500 }); }
}
