#!/bin/bash
set -e
WORKDIR="/Users/nebulalumino/.openclaw/workspace"
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"

build_app() {
  local idx=$1
  local app=$2
  local hsl=$3
  local title=$4
  local desc=$5
  local color=$6
  local system_prompt=$7

  echo "=== [$idx] Building: $app ==="
  cd "$WORKDIR"
  
  # Create Next.js app (if not exists)
  if [ ! -d "$app" ]; then
    npx create-next-app@latest "$app" --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-turbopack --yes 2>&1 | grep -E "(Created|Success|Error|error)" | head -5
  fi
  
  APP_DIR="$WORKDIR/$app"
  
  # Write page.tsx
  cat > "$APP_DIR/src/app/page.tsx" << PAGEOF
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
          <h1 className="text-4xl font-bold" style="color: hsl($hsl)">$title</h1>
          <p className="text-gray-400">$desc</p>
        </div>
        <div className="bg-gray-800/60 border rounded-2xl p-6 space-y-4 shadow-xl" style="border-color: hsla($hsl, 0.3)">
          <label className="block text-sm font-medium text-gray-300">Enter your details</label>
          <textarea className="w-full h-40 bg-gray-900/80 border border-gray-700 rounded-xl p-4 text-white text-sm placeholder-gray-500 focus:outline-none resize-none"
            placeholder="Describe your financial situation, goals, and specific parameters..."
            value={input} onChange={(e) => setInput(e.target.value)} />
          <button onClick={handleGenerate} disabled={loading || !input.trim()}
            className="w-full text-white font-semibold py-3 rounded-xl transition-colors disabled:cursor-not-allowed"
            style="background-color: hsl($hsl); --tw-bg-opacity: 1">
            {loading ? "Generating..." : "Generate Analysis"}
          </button>
        </div>
        {output && (
          <div className="bg-gray-800/60 border rounded-2xl p-6" style="border-color: hsla($hsl, 0.3)">
            <h2 className="text-lg font-semibold mb-3" style="color: hsl($hsl)">Results</h2>
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
  cat > "$APP_DIR/src/app/api/generate/route.ts" << ROUTEOF
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
        { role: "system", content: "$system_prompt" },
        { role: "user", content: prompt }
      ],
      temperature: 0.7, max_tokens: 2000,
    });
    return NextResponse.json({ result: completion.choices[0].message.content });
  } catch (err: any) { return NextResponse.json({ error: err.message }, { status: 500 }); }
}
ROUTEOF

  # Install & build
  cd "$APP_DIR" && npm install openai 2>&1 | tail -2
  npm run build 2>&1 | grep -E "(✓|Error|error|Warning|Route)" | head -10
  
  # Git commit & push
  cd "$APP_DIR" && git init 2>/dev/null || true
  git add -A && git commit -m "feat: initial commit" 2>&1 | tail -2
  gh repo create NebulaLumino/"$app" --public --source=. --push 2>&1 | tail -3
  
  # Cleanup
  rm -rf "$APP_DIR/node_modules" "$APP_DIR/.next"
  echo "=== DONE: $app ==="
  echo ""
}

# App 3502: ai-fire-calculator
build_app "3502" "ai-fire-calculator" "145,60%,45%" "FIRE Calculator 🌱" "FIRE calculation engine with Monte Carlo summary" "green" "You are an expert FIRE (Financial Independence, Retire Early) financial advisor. Analyze the user's financial data and provide: 1) Current savings rate and FIRE number calculation, 2) Monte Carlo simulation summary (success probability, year to FIRE), 3) Monthly savings strategy, 4) Withdrawal rate analysis (4% rule safety), 5) Recommended investment allocation. Include specific numbers, timelines, and actionable steps."

# App 3503: ai-options-greeks
build_app "3503" "ai-options-greeks" "220,60%,55%" "Options Greeks 📈" "Options Greeks visualizer (Delta/Gamma/Theta/Vega/Rho)" "blue" "You are an expert options trader and educator. Calculate and explain the options Greeks for any given option contract: 1) Delta (price sensitivity), 2) Gamma (rate of delta change), 3) Theta (time decay), 4) Vega (volatility sensitivity), 5) Rho (interest rate sensitivity). Provide interpretation of each Greek, what it means for the position, and how to use them to manage risk."

# App 3504: ai-dividend-growth
build_app "3504" "ai-dividend-growth" "85,65%,50%" "Dividend Growth 📈" "Dividend growth portfolio builder" "lime" "You are an expert dividend investing advisor. Build a dividend growth portfolio for the user: 1) Screen for quality dividend growth stocks (DGI criteria), 2) Sector diversification recommendations, 3) Yield vs growth tradeoff analysis, 4) DRIP (Dividend Reinvestment) strategy, 5) Tax-efficient account placement. Include specific stock examples, expected yield, and dividend growth projections."

# App 3505: ai-real-estate-roi
build_app "3505" "ai-real-estate-roi" "45,70%,55%" "Real Estate ROI 🏠" "Real estate ROI calculator" "yellow" "You are an expert real estate investment analyst. Calculate ROI for real estate investments: 1) Cap rate, cash-on-cash return, and IRR calculations, 2) Rental income analysis (gross/net), 3) Mortgage amortization breakdown, 4) Appreciation projections, 5) Operating expense analysis. Provide specific numbers, break-even analysis, and buy/hold/sell recommendations."

# App 3506: ai-tax-loss-harvest
build_app "3506" "ai-tax-loss-harvest" "0,65%,50%" "Tax Loss Harvest 🔴" "Tax loss harvesting optimizer" "red" "You are an expert tax optimization advisor. Analyze investment portfolios for tax loss harvesting opportunities: 1) Identify unrealized losses that can be harvested, 2) Calculate potential tax savings (short-term vs long-term), 3) Wash sale rule compliance guidance, 4) Tax lot optimization strategies, 5) Year-end tax planning recommendations. Include specific examples with dollar amounts."

# App 3507: ai-emergency-fund
build_app "3507" "ai-emergency-fund" "175,55%,45%" "Emergency Fund 🛟" "Emergency fund planner" "teal" "You are a personal finance advisor specializing in emergency planning. Help users build and maintain emergency funds: 1) Target fund size based on expenses and risk factors, 2) Monthly savings roadmap to reach goal, 3) Best account types for emergency funds (HYSA vs money market), 4) Trigger conditions for using the fund, 5) Replenishment strategy after use. Include specific savings targets and timeline."

# App 3508: ai-debt-payoff
build_app "3508" "ai-debt-payoff" "335,55%,55%" "Debt Payoff 🌹" "Debt snowball/avalanche optimizer" "rose" "You are a debt repayment strategist. Compare debt payoff strategies: 1) Snowball method (smallest balance first), 2) Avalanche method (highest interest first), 3) Hybrid approach, 4) Balance transfer analysis, 5) Total interest saved comparison. Include amortization schedules, monthly payment plans, and exact payoff dates."

# App 3509: ai-factor-investing
build_app "3509" "ai-factor-investing" "255,55%,55%" "Factor Investing 🟣" "Factor investing portfolio builder" "purple" "You are an expert in factor-based investing. Design a factor investing portfolio: 1) Factor analysis (value, size, momentum, quality, profitability), 2) ETF/fund recommendations for each factor, 3) Factor exposure and diversification, 4) Historical factor premium data, 5) Risk-adjusted return expectations. Include specific fund tickers and allocation percentages."

# App 3510: ai-retirement-projection
build_app "3510" "ai-retirement-projection" "200,45%,45%" "Retirement Projection 💎" "Retirement savings projection" "slate" "You are a retirement planning actuary. Create comprehensive retirement projections: 1) Current vs required retirement savings, 2) Multiple scenario analysis (conservative/moderate/aggressive), 3) Social Security optimization, 4) Required minimum distributions, 5) Healthcare cost planning. Include specific savings targets, annual contribution needs, and success probability."

# App 3511: ai-black-scholes
build_app "3511" "ai-black-scholes" "185,60%,55%" "Black-Scholes 🔮" "Black-Scholes option pricer" "cyan" "You are an expert quantitative analyst. Use the Black-Scholes model to price options: 1) Call and put option prices, 2) Implied volatility calculations, 3) Greeks derivation from the model, 4) Sensitivity analysis (what-if scenarios), 5) Limitations and real-world adjustments. Include formulas, step-by-step calculations, and interpretation of results."

# App 3512: ai-risk-tolerance
build_app "3512" "ai-risk-tolerance" "25,70%,55%" "Risk Tolerance 🎯" "Risk tolerance quiz & profile builder" "orange" "You are a financial risk assessment advisor. Conduct a comprehensive risk tolerance assessment: 1) Risk capacity (financial ability to take risk), 2) Risk willingness (psychological comfort with risk), 3) Risk knowledge assessment, 4) Investor profile classification (conservative to aggressive), 5) Asset allocation recommendations matching the profile. Include a quiz format with scoring rubric."

# App 3513: ai-net-worth
build_app "3513" "ai-net-worth" "125,55%,45%" "Net Worth Tracker 💎" "Net worth tracker generator" "emerald" "You are a personal wealth analyst. Help track and grow net worth: 1) Asset inventory (investments, real estate, cash, crypto), 2) Liability breakdown (mortgages, loans, credit cards), 3) Net worth calculation and history, 4) Year-over-year growth analysis, 5) Wealth-building roadmap with specific milestones. Include templates and tracking methodology."

# App 3514: ai-behavioral-finance
build_app "3514" "ai-behavioral-finance" "305,60%,60%" "Behavioral Finance 🧠" "Behavioral finance bias detector" "pink" "You are an expert in behavioral finance and investor psychology. Identify cognitive and emotional biases: 1) Loss aversion analysis, 2) Overconfidence bias, 3) Herd behavior detection, 4) Anchoring effects, 5) Present bias. Provide a bias score, evidence-based mitigation strategies, and a personalized action plan to improve investment decision-making."

# App 3515: ai-dca-strategist
build_app "3515" "ai-dca-strategist" "75,60%,50%" "DCA Strategist 📊" "Dollar cost averaging strategist" "emerald" "You are a DCA (Dollar Cost Averaging) investment strategist. Optimize DCA strategies: 1) Lump sum vs DCA comparison with historical data, 2) Optimal DCA frequency and amount, 3) Asset allocation for DCA portfolios, 4) Roth conversion ladder analysis, 5) Tax-efficient DCA in different account types. Include backtested results and specific fund recommendations."

# App 3516: ai-etf-screener
build_app "3516" "ai-etf-screener" "165,55%,45%" "ETF Screener 🔍" "ETF screener & comparator" "cyan" "You are an ETF specialist and fund analyst. Screen and compare ETFs: 1) Filter by expense ratio, AUM, liquidity, 2) Performance comparison across timeframes, 3) Tax efficiency analysis, 4) Tracking error assessment, 5) Sector/factor exposure comparison. Include specific ETF recommendations with ticker symbols, pros/cons, and suitability notes."

# App 3517: ai-charitable-giving
build_app "3517" "ai-charitable-giving" "340,55%,55%" "Charitable Giving 💝" "Charitable giving optimizer (DAF vs QCD)" "rose" "You are a philanthropic giving strategist. Optimize charitable giving: 1) DAF (Donor Advised Fund) vs QCD (Qualified Charitable Distribution) comparison, 2) Tax deduction optimization, 3) Asset donation strategy (appreciated securities vs cash), 4) Giving circles and impact assessment, 5) Multi-year giving plan. Include dollar-specific recommendations and tax savings calculations."

# App 3518: ai-estate-planning
build_app "3518" "ai-estate-planning" "215,45%,55%" "Estate Planning 📋" "Estate planning checklist generator" "gray-blue" "You are an estate planning attorney and financial advisor. Generate a comprehensive estate planning checklist: 1) Will and testament review, 2) Beneficiary designations audit, 3) Power of attorney setup, 4) Healthcare directives, 5) Trust strategies (revocable vs irrevocable), 6) Estate tax minimization, 7) Digital asset planning. Include state-specific considerations and priority ordering."

# App 3519: ai-cash-flow-forecast
build_app "3519" "ai-cash-flow-forecast" "0,60%,50%" "Cash Flow Forecast 💰" "Small business cash flow forecaster" "red" "You are a small business CFO and financial analyst. Forecast cash flow for small businesses: 1) 13-week cash flow projection, 2) AR/AP analysis and timing, 3) Seasonal adjustment modeling, 4) Break-even analysis, 5) Working capital optimization, 6) Scenario planning (best/base/worst case). Include spreadsheet methodology and specific cash position projections."

# App 3520: ai-pe-ratio
build_app "3520" "ai-pe-ratio" "235,55%,55%" "P/E Analyzer 📊" "P/E ratio & valuation analyzer" "indigo" "You are a stock valuation expert and financial analyst. Analyze P/E ratios and valuations: 1) Trailing vs forward P/E comparison, 2) PEG ratio calculation and interpretation, 3) Industry-relative valuation, 4) Historical P/E percentile analysis, 5) Growth-adjusted fair value estimation. Include specific company analysis examples with buy/sell/hold signals based on valuation."

echo "=== ALL 20 APPS BUILT ==="
