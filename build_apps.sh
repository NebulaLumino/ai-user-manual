#!/bin/bash
set -e

WORKDIR="/Users/nebulalumino/.openclaw/workspace"

# App definitions: name | hsl-color | title | prompt-system-content
declare -A APPS=(
  ["ai-fire-calculator"]="145°,60%,45%|FIRE Calculator 🌱|FIRE calculation engine with Monte Carlo summary"
  ["ai-options-greeks"]="220°,60%,55%|Options Greeks 📈|Options Greeks visualizer (Delta/Gamma/Theta/Vega/Rho)"
  ["ai-dividend-growth"]="85°,65%,50%|Dividend Growth 📈|Dividend growth portfolio builder"
  ["ai-real-estate-roi"]="45°,70%,55%|Real Estate ROI 🏠|Real estate ROI calculator"
  ["ai-tax-loss-harvest"]="0°,65%,50%|Tax Loss Harvest 🔴|Tax loss harvesting optimizer"
  ["ai-emergency-fund"]="175°,55%,45%|Emergency Fund 🛟|Emergency fund planner"
  ["ai-debt-payoff"]="335°,55%,55%|Debt Payoff 🌹|Debt snowball/avalanche optimizer"
  ["ai-factor-investing"]="255°,55%,55%|Factor Investing 🟣|Factor investing portfolio builder"
  ["ai-retirement-projection"]="200°,45%,45%|Retirement Projection 💎|Retirement savings projection"
  ["ai-black-scholes"]="185°,60%,55%|Black-Scholes 🔮|Black-Scholes option pricer"
  ["ai-risk-tolerance"]="25°,70%,55%|Risk Tolerance 🎯|Risk tolerance quiz & profile builder"
  ["ai-net-worth"]="125°,55%,45%|Net Worth Tracker 💎|Net worth tracker generator"
  ["ai-behavioral-finance"]="305°,60%,60%|Behavioral Finance 🧠|Behavioral finance bias detector"
  ["ai-dca-strategist"]="75°,60%,50%|DCA Strategist 📊|Dollar cost averaging strategist"
  ["ai-etf-screener"]="165°,55%,45%|ETF Screener 🔍|ETF screener & comparator"
  ["ai-charitable-giving"]="340°,55%,55%|Charitable Giving 💝|Charitable giving optimizer (DAF vs QCD)"
  ["ai-estate-planning"]="215°,45%,55%|Estate Planning 📋|Estate planning checklist generator"
  ["ai-cash-flow-forecast"]="0°,60%,50%|Cash Flow Forecast 💰|Small business cash flow forecaster"
  ["ai-pe-ratio"]="235°,55%,55%|P/E Analyzer 📊|P/E ratio & valuation analyzer"
)

SYSTEM_PROMPTS=(
  "FIRE calculation engine with Monte Carlo summary"
  "Options Greeks visualizer (Delta/Gamma/Theta/Vega/Rho)"
  "Dividend growth portfolio builder"
  "Real estate ROI calculator"
  "Tax loss harvesting optimizer"
  "Emergency fund planner"
  "Debt snowball/avalanche optimizer"
  "Factor investing portfolio builder"
  "Retirement savings projection"
  "Black-Scholes option pricer"
  "Risk tolerance quiz & profile builder"
  "Net worth tracker generator"
  "Behavioral finance bias detector"
  "Dollar cost averaging strategist"
  "ETF screener & comparator"
  "Charitable giving optimizer (DAF vs QCD)"
  "Estate planning checklist generator"
  "Small business cash flow forecaster"
  "P/E ratio & valuation analyzer"
)

APP_NAMES=(
  "ai-fire-calculator"
  "ai-options-greeks"
  "ai-dividend-growth"
  "ai-real-estate-roi"
  "ai-tax-loss-harvest"
  "ai-emergency-fund"
  "ai-debt-payoff"
  "ai-factor-investing"
  "ai-retirement-projection"
  "ai-black-scholes"
  "ai-risk-tolerance"
  "ai-net-worth"
  "ai-behavioral-finance"
  "ai-dca-strategist"
  "ai-etf-screener"
  "ai-charitable-giving"
  "ai-estate-planning"
  "ai-cash-flow-forecast"
  "ai-pe-ratio"
)

HSL_COLORS=(
  "145°,60%,45%"
  "220°,60%,55%"
  "85°,65%,50%"
  "45°,70%,55%"
  "0°,65%,50%"
  "175°,55%,45%"
  "335°,55%,55%"
  "255°,55%,55%"
  "200°,45%,45%"
  "185°,60%,55%"
  "25°,70%,55%"
  "125°,55%,45%"
  "305°,60%,60%"
  "75°,60%,50%"
  "165°,55%,45%"
  "340°,55%,55%"
  "215°,45%,55%"
  "0°,60%,50%"
  "235°,55%,55%"
)

INDEX=0
for APP in "${APP_NAMES[@]}"; do
  INDEX=$((INDEX+1))
  echo "=== Building app $INDEX: $APP ==="
  
  cd "$WORKDIR"
  
  # Create Next.js app
  npx create-next-app@latest "$APP" --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-turbopack --yes 2>&1 | tail -5
  
  APP_DIR="$WORKDIR/$APP"
  
  # Write page.tsx
  HSL="${HSL_COLORS[$INDEX-1]}"
  COLOR_NAME=$(echo "$APP" | sed 's/ai-//' | sed 's/-/ /g')
  TITLE="${APP_NAMES[$INDEX-1]}"
  
  cat > "$APP_DIR/src/app/page.tsx" << 'PAGEOF'
"use client";
import { useState } from "react";
export default function Home() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const handleGenerate = async () => {
    if (!input.trim()) return;
    setLoading(true); setOutput("");
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });
      const data = await res.json();
      setOutput(data.result || "No output received.");
    } catch { setOutput("Error generating response."); }
    finally { setLoading(false); }
  };
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-green-400">APP_TITLE</h1>
          <p className="text-gray-400">APP_DESC</p>
        </div>
        <div className="bg-gray-800/60 border border-green-500/30 rounded-2xl p-6 space-y-4 shadow-xl shadow-green-900/20">
          <label className="block text-sm font-medium text-gray-300">Enter your details</label>
          <textarea className="w-full h-40 bg-gray-900/80 border border-gray-700 rounded-xl p-4 text-white text-sm placeholder-gray-500 focus:outline-none focus:border-green-500 resize-none"
            placeholder="Describe your financial situation, goals, and any specific parameters..."
            value={input} onChange={(e) => setInput(e.target.value)} />
          <button onClick={handleGenerate} disabled={loading || !input.trim()}
            className="w-full bg-green-600 hover:bg-green-500 disabled:bg-green-800 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition-colors">
            {loading ? "Generating..." : "Generate Analysis"}
          </button>
        </div>
        {output && (
          <div className="bg-gray-800/60 border border-green-500/30 rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-green-300 mb-3">Results</h2>
            <div className="prose prose-invert prose-sm max-w-none text-gray-300 whitespace-pre-wrap">{output}</div>
          </div>
        )}
      </div>
    </main>
  );
}
PAGEOF
  
  # Write API route
  mkdir -p "$APP_DIR/src/app/api/generate"
  cat > "$APP_DIR/src/app/api/generate/route.ts" << 'ROUTEOF'
import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
function getClient() {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error("Missing OPENAI_API_KEY");
  return new OpenAI({ apiKey, baseURL: "https://api.deepseek.com/v1" });
}
export async function POST(req: NextRequest) {
  try {
    const { prompt } = await req.json();
    const client = getClient();
    const completion = await client.chat.completions.create({
      model: "deepseek-chat",
      messages: [
        { role: "system", content: "SYSTEM_PROMPT_PLACEHOLDER" },
        { role: "user", content: prompt }
      ],
      temperature: 0.7, max_tokens: 2000,
    });
    return NextResponse.json({ result: completion.choices[0].message.content });
  } catch (err: any) { return NextResponse.json({ error: err.message }, { status: 500 }); }
}
ROUTEOF
  
  # Install openai
  cd "$APP_DIR" && npm install openai 2>&1 | tail -3
  
  # Build
  npm run build 2>&1 | tail -10
  
  # Git commit & push
  cd "$APP_DIR" && git init && git add -A && git commit -m "feat: initial commit" 2>&1 | tail -3
  gh repo create NebulaLumino/"$APP" --public --source=. --push 2>&1 | tail -3
  
  # Cleanup
  rm -rf "$APP_DIR/node_modules" "$APP_DIR/.next"
  echo "=== Done: $APP ==="
  echo ""
done

echo "ALL APPS BUILT!"
