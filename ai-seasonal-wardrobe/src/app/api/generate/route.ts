import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://api.deepseek.com/v1",
});

export async function POST(req: NextRequest) {
  try {
    const { currentWardrobe, seasonalClimate, storageSpace, budget, styleGoals } = await req.json();

    const prompt = `You are an expert personal stylist and wardrobe consultant specializing in seasonal transitions.

Generate a comprehensive seasonal wardrobe transition plan based on:

- **Current Wardrobe State:** ${currentWardrobe || "Not specified"}
- **Seasonal Climate:** ${seasonalClimate || "Not specified"}
- **Storage Space Available:** ${storageSpace || "Not specified"}
- **Budget for Additions:** ${budget || "Not specified"}
- **Style Evolution Goals:** ${styleGoals || "Not specified"}

Please generate a detailed report with the following sections:

# 🌡️ Climate Assessment
Analyze the seasonal climate and how it should influence wardrobe choices.

# 📦 Items to Pack Away
List specific items from the current wardrobe that should be stored for the season. Include fabric care tips and storage recommendations.

# 👗 Items to Add
Recommend specific new pieces to acquire for the season. Include budget tier suggestions.

# 🛒 Transition Shopping List
A prioritized shopping list with specific item types, approximate price ranges, and where to shop (luxury/mid-range/budget).

# 🗄️ Storage Solutions
Organizational tips for packing away off-season clothes. Include container recommendations and space-saving techniques.

# ✨ Fresh Styling Combinations
New outfit combinations to create from existing pieces that feel seasonally appropriate.

# 💝 Donation & Consignment Plan
Which current items to donate, consign, or recycle. Include estimated resale value where relevant.

# 🎯 Style Evolution Roadmap
How this seasonal transition moves toward the stated style goals.

Be specific, practical, and actionable. Include real fabric names, brand examples, and exact organization steps.`;

    const completion = await client.chat.completions.create({
      model: "deepseek-chat",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.7,
      max_tokens: 2000,
    });

    const result = completion.choices[0]?.message?.content || "No output generated.";
    return NextResponse.json({ result });
  } catch (error: unknown) {
    console.error("Error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Generation failed" },
      { status: 500 }
    );
  }
}
