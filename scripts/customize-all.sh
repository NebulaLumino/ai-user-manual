#!/bin/bash
# Customize all 20 Cycle 71 apps
WS="/Users/nebulalumino/.openclaw/workspace"
CD="cd $WS"

GLOBALS='@tailwind base;
@tailwind components;
@tailwind utilities;

:root { --background: #0a0a0a; --foreground: #ededed; }
body { color: var(--foreground); background: var(--background); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }'

write_route() {
  APP=$1
  PROMPT=$2
  mkdir -p "$WS/$APP/src/app/api/generate"
  cat > "$WS/$APP/src/app/api/generate/route.ts" << 'ROUTE_EOF'
import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://api.deepseek.com/v1",
});

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const keys = [
      "genre","logline","setting","tone","length","archetype","title","format",
      "budget","location","audience","platform","content_type","demographics",
      "release_date","episodes","source_lang","target_lang","age_rating","runtime",
      "voice_style","pages","experience","protagonist_name","antagonist","supporting",
      "world_rules","conflict","resolution","themes","shooting_schedule","characters",
      "timeline","props","costumes","era","terrain","climate","lighting",
      "budget_amount","inconsistency_type","script_content","festival_type",
      "premiere_goal","bts_content_type","distribution","dialogue_sample",
      "reading_level","ep_num","season_count","episode_runtime","pacing_notes",
      "critics_praise","critics_concerns","languages"
    ];
    let prompt = `ROUTE_EOF
    # Escape the prompt for the template literal
    echo "$PROMPT" | sed 's/"/\\"/g' >> "$WS/$APP/src/app/api/generate/route.ts"
    cat >> "$WS/$APP/src/app/api/generate/route.ts" << 'ROUTE_MID'
`;
    for (const key of keys) {
      prompt = prompt.replace(new RegExp("{" + key + "}", "g"), String(body[key] || ""));
    }
    const completion = await client.chat.completions.create({
      model: "deepseek-chat",
      messages: [
        { role: "system", content: "You are a world-class expert in this domain. Provide detailed, actionable, well-structured output." },
        { role: "user", content: prompt },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    });
    return NextResponse.json({ result: completion.choices[0].message.content });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
ROUTE_MID
}

write_layout() {
  APP=$1; TITLE=$2; DESC=$3
  cat > "$WS/$APP/src/app/layout.tsx" << EOF
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "${TITLE}",
  description: "${DESC}",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
EOF
}

write_globals() {
  APP=$1
  echo "$GLOBALS" > "$WS/$APP/src/app/globals.css"
}

echo "Writing globals and layouts for all apps..."
for app in ai-screenwriting ai-pre-production ai-streaming-analytics ai-dubbing-subtitling ai-script-coverage ai-film-marketing ai-post-production ai-casting-breakdown ai-tv-arc-planner ai-film-budget ai-continuity-checker ai-location-scouting ai-film-festival-strategy ai-bts-content ai-dialogue-polisher ai-binge-pacing ai-film-review-aggregator ai-bilingual-subtitles ai-talent-pitch ai-props-set-design; do
  write_globals $app
done

# Write layouts with proper titles
declare -A TITLES=(
  ["ai-screenwriting"]="AI Screenwriting|PGenerate professional screenplays with act structure, dialogue, and scene beats"
  ["ai-pre-production"]="AI Pre-Production Planner|Plan comprehensive film and TV pre-production workflows"
  ["ai-streaming-analytics"]="AI Streaming Analytics|Analyze and predict streaming platform performance"
  ["ai-dubbing-subtitling"]="AI Dubbing & Subtitling Workflow|Plan professional dubbing and subtitle localization workflows"
  ["ai-script-coverage"]="AI Script Coverage|Professional script coverage and reader's report generator"
  ["ai-film-marketing"]="AI Film Marketing|Strategic film and TV marketing campaign planner"
  ["ai-post-production"]="AI Post-Production Planner|Plan post-production workflow from edit to delivery"
  ["ai-casting-breakdown"]="AI Casting Breakdown|Create professional casting breakdowns and character analyses"
  ["ai-tv-arc-planner"]="AI TV Arc Planner|Plan multi-season TV series story arcs and episode structures"
  ["ai-film-budget"]="AI Film Budget|Generate detailed production budgets and cost breakdowns"
  ["ai-continuity-checker"]="AI Continuity Checker|Detect inconsistencies in scripts and production details"
  ["ai-location-scouting"]="AI Location Scouting|Find and evaluate filming locations"
  ["ai-film-festival-strategy"]="AI Film Festival Strategy|Strategize festival submissions and premiere strategy"
  ["ai-bts-content"]="AI BTS Content Planner|Plan behind-the-scenes content and promotional material"
  ["ai-dialogue-polisher"]="AI Dialogue Polisher|Polish and refine screenplay dialogue"
  ["ai-binge-pacing"]="AI Binge Pacing Analyzer|Analyze and optimize streaming episode pacing"
  ["ai-film-review-aggregator"]="AI Film Review Aggregator|Synthesize and analyze film reviews from multiple sources"
  ["ai-bilingual-subtitles"]="AI Bilingual Subtitles|Create and manage bilingual subtitle workflows"
  ["ai-talent-pitch"]="AI Talent Pitch|Generate compelling talent pitches and actor comparisons"
  ["ai-props-set-design"]="AI Props & Set Design|Plan props, set dressing, and production design"
)

for app in "${!TITLES[@]}"; do
  IFS='|' read -r title desc <<< "${TITLES[$app]}"
  write_layout "$app" "$title" "$desc"
done

echo "Done customizing layouts and globals"
