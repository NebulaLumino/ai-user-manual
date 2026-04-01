#!/usr/bin/env python3
"""Generate all 20 app files"""
import os, subprocess

WS = "/Users/nebulalumino/.openclaw/workspace"
GLOBALS = '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n:root { --background: #0a0a0a; --foreground: #ededed; }\nbody { color: var(--foreground); background: var(--background); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }'

LAYOUT = '''import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "%s",
  description: "%s",
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
'''

ROUTE_TEMPLATE = '''import { NextRequest, NextResponse } from "next/server";
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
    let prompt = `%s`;
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
'''

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  wrote {path}")

def gen_route(app, prompt):
    route = ROUTE_TEMPLATE % prompt
    write(f"{WS}/{app}/src/app/api/generate/route.ts", route)

def gen_layout(app, title, desc):
    write(f"{WS}/{app}/src/app/layout.tsx", LAYOUT % (title, desc))
    write(f"{WS}/{app}/src/app/globals.css", GLOBALS)

ACCENTS = {
    "violet": ("from-violet-400","to-violet-600","text-violet-400","border-violet-500","bg-violet-600 hover:bg-violet-700"),
    "blue": ("from-blue-400","to-blue-600","text-blue-400","border-blue-500","bg-blue-600 hover:bg-blue-700"),
    "amber": ("from-amber-400","to-amber-600","text-amber-400","border-amber-500","bg-amber-600 hover:bg-amber-700"),
    "rose": ("from-rose-400","to-rose-600","text-rose-400","border-rose-500","bg-rose-600 hover:bg-rose-700"),
    "teal": ("from-teal-400","to-teal-600","text-teal-400","border-teal-500","bg-teal-600 hover:bg-teal-700"),
    "orange": ("from-orange-400","to-orange-600","text-orange-400","border-orange-500","bg-orange-600 hover:bg-orange-700"),
    "pink": ("from-pink-400","to-pink-600","text-pink-400","border-pink-500","bg-pink-600 hover:bg-pink-700"),
    "cyan": ("from-cyan-400","to-cyan-600","text-cyan-400","border-cyan-500","bg-cyan-600 hover:bg-cyan-700"),
    "lime": ("from-lime-400","to-lime-600","text-lime-400","border-lime-500","bg-lime-600 hover:bg-lime-700"),
    "emerald": ("from-emerald-400","to-emerald-600","text-emerald-400","border-emerald-500","bg-emerald-600 hover:bg-emerald-700"),
    "red": ("from-red-400","to-red-600","text-red-400","border-red-500","bg-red-600 hover:bg-red-700"),
    "yellow": ("from-yellow-400","to-yellow-600","text-yellow-400","border-yellow-500","bg-yellow-600 hover:bg-yellow-700"),
    "purple": ("from-purple-400","to-purple-600","text-purple-400","border-purple-500","bg-purple-600 hover:bg-purple-700"),
    "sky": ("from-sky-400","to-sky-600","text-sky-400","border-sky-500","bg-sky-600 hover:bg-sky-700"),
    "zinc": ("from-zinc-400","to-zinc-600","text-zinc-400","border-zinc-500","bg-zinc-600 hover:bg-zinc-700"),
    "indigo": ("from-indigo-400","to-indigo-600","text-indigo-400","border-indigo-500","bg-indigo-600 hover:bg-indigo-700"),
    "fuchsia": ("from-fuchsia-400","to-fuchsia-600","text-fuchsia-400","border-fuchsia-500","bg-fuchsia-600 hover:bg-fuchsia-700"),
    "stone": ("from-stone-400","to-stone-600","text-stone-400","border-stone-500","bg-stone-600 hover:bg-stone-700"),
    "neutral": ("from-neutral-400","to-neutral-600","text-neutral-400","border-neutral-500","bg-neutral-600 hover:bg-neutral-700"),
    "slate": ("from-slate-400","to-slate-600","text-slate-400","border-slate-500","bg-slate-600 hover:bg-slate-700"),
}

def gen_page(app, accent, title, fields_html):
    g1, g2, ta, fb, bh = ACCENTS[accent]
    # fields_html uses %s as placeholder for focus border
    safe_fields = fields_html.replace("FOCUS", fb)
    page = (
        '"use client";\n\n'
        'import { useState } from "react";\n\n'
        'export default function Home() {\n'
        '  const [output, setOutput] = useState("");\n'
        '  const [isLoading, setIsLoading] = useState(false);\n'
        '  const [error, setError] = useState("");\n\n'
        '  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {\n'
        '    e.preventDefault();\n'
        '    const form = e.currentTarget;\n'
        '    const data = Object.fromEntries(new FormData(form.entries()));\n'
        '    setIsLoading(true);\n'
        '    setOutput("");\n'
        '    setError("");\n'
        '    try {\n'
        '      const res = await fetch("/api/generate", {\n'
        '        method: "POST",\n'
        '        headers: { "Content-Type": "application/json" },\n'
        '        body: JSON.stringify(data),\n'
        '      });\n'
        '      const json = await res.json();\n'
        '      if (!res.ok) throw new Error(json.error || "Generation failed");\n'
        '      setOutput(json.result);\n'
        '    } catch (err: any) {\n'
        '      setError(err.message);\n'
        '    } finally {\n'
        '      setIsLoading(false);\n'
        '    }\n'
        '  }\n\n'
        '  return (\n'
        '    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white">\n'
        '      <div className="max-w-5xl mx-auto px-6 py-12">\n'
        '        <header className="mb-10">\n'
        '          <h1 className="text-4xl font-bold bg-gradient-to-r %s %s bg-clip-text text-transparent mb-2">%s</h1>\n'
        '        </header>\n'
        '        <div className="grid md:grid-cols-2 gap-8">\n'
        '          <form onSubmit={handleSubmit} className="space-y-4">\n'
        '            %s\n'
        '            <button type="submit" disabled={isLoading} className={"w-full %s disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-colors"}>\n'
        '              {isLoading ? "Generating..." : "Generate"}\n'
        '            </button>\n'
        '          </form>\n'
        '          <div>\n'
        '            {error && <div className="bg-red-900/30 border border-red-700 text-red-300 rounded-lg p-4 mb-4">{error}</div>}\n'
        '            {isLoading && (\n'
        '              <div className="bg-gray-800 rounded-xl p-8 text-center space-y-3">\n'
        '                <div className="flex justify-center gap-2">\n'
        '                  {[0,1,2].map(i => <span key={i} className={"w-3 h-3 %s rounded-full animate-bounce"} style={{animationDelay: `${i*0.1}s`}} />)}\n'
        '                </div>\n'
        '                <p className="text-gray-400 text-sm">Generating...</p>\n'
        '              </div>\n'
        '            )}\n'
        '            {output && (\n'
        '              <div className="bg-gray-800 rounded-xl p-6">\n'
        '                <h3 className={"text-sm font-semibold mb-3 " + "%s"}>Result</h3>\n'
        '                <pre className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed max-h-[600px] overflow-y-auto">{output}</pre>\n'
        '              </div>\n'
        '            )}\n'
        '            {!output && !isLoading && (\n'
        '              <div className="bg-gray-800/50 rounded-xl p-8 text-center text-gray-500 border-2 border-dashed border-gray-700">\n'
        '                <p>Output will appear here</p>\n'
        '              </div>\n'
        '            )}\n'
        '          </div>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>\n'
        '  );\n'
        '}\n'
    ) % (g1, g2, title, safe_fields, bh, ta, ta)
    write(f"{WS}/{app}/src/app/page.tsx", page)

def build(app, accent, title, desc, fields_html, prompt):
    print(f"Building {app}...")
    gen_layout(app, title, desc)
    gen_route(app, prompt)
    gen_page(app, accent, title, fields_html)

# ─── ALL 20 APPS ───────────────────────────────────────────────────────────────

build("ai-screenwriting", "violet", "AI Screenwriting",
    "Generate professional screenplays",
    (
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Genre</label>'
        '<select id="genre" name="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Mystery</option><option>Noir</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Logline *</label>'
        '<textarea id="logline" name="logline" rows="3" placeholder="A compelling one-sentence summary..." class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500 resize-none"></textarea></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Setting</label>'
        '<input id="setting" name="setting" placeholder="Time period and location" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Tone</label>'
        '<select id="tone" name="tone" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Dark & gritty</option><option>Light & comedic</option><option>Serious & dramatic</option><option>Whimsical</option><option>Noir</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Format</label>'
        '<select id="length" name="length" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="short">Short Film (5-15 min)</option><option value="feature">Feature Film (90-120 min)</option><option value="tv-episode">TV Episode (42 min)</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Protagonist Archetype</label>'
        '<input id="archetype" name="archetype" placeholder="e.g. The Rebel, The Mentor, The Hero" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
    ),
    "You are an expert screenwriter. Write a compelling screenplay excerpt based on: Genre: {genre}, Logline: {logline}, Setting: {setting}, Tone: {tone}, Format: {length}, Protagonist: {archetype}. Include scene heading, action lines, character names, dialogue, and parentheticals. Format as proper screenplay with FADE IN, act structure markers, and scene beats. Write approximately 8-12 pages worth of content."
)

build("ai-pre-production", "blue", "AI Pre-Production Planner",
    "Plan film and TV pre-production workflows",
    (
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Project Title</label>'
        '<input id="title" name="title" placeholder="Your project title" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Genre</label>'
        '<select id="genre" name="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Format</label>'
        '<select id="format" name="format" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="short">Short Film</option><option value="feature">Feature Film</option><option value="tv-pilot">TV Pilot</option><option value="tv-season">TV Season</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Budget Tier</label>'
        '<select id="budget" name="budget" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="micro">Micro (under $50K)</option><option value="low">Low ($50K-$500K)</option><option value="mid">Mid ($500K-$5M)</option><option value="studio">Studio ($5M+)</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Primary Location</label>'
        '<input id="location" name="location" placeholder="Main shooting location" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Target Audience</label>'
        '<input id="audience" name="audience" placeholder="e.g. Adults 18-34, families" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
    ),
    "You are an expert film production manager. Create a comprehensive pre-production plan for: Title: {title}, Genre: {genre}, Format: {format}, Budget: {budget}, Location: {location}, Audience: {audience}. Provide: 1) Timeline from greenlight to production start with weekly milestones, 2) Key crew positions and hiring order, 3) Script breakdown by department, 4) Casting process timeline, 5) Location scouting checklist, 6) Budget allocation breakdown by percentage, 7) Legal/permit requirements, 8) Risk assessment, 9) Day-one readiness checklist."
)

build("ai-streaming-analytics", "amber", "AI Streaming Analytics",
    "Analyze streaming platform performance",
    (
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Platform</label>'
        '<select id="platform" name="platform" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Netflix</option><option>Amazon Prime</option><option>Disney+</option><option>HBO Max</option><option>Hulu</option><option>Apple TV+</option><option>Peacock</option><option>Paramount+</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Content Type</label>'
        '<select id="content_type" name="content_type" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Original Series</option><option>Original Film</option><option>Licensed Content</option><option>Documentary</option><option>Reality Show</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Target Demographics</label>'
        '<input id="demographics" name="demographics" placeholder="e.g. 18-34 males, 25-54 females" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Release Date</label>'
        '<input id="release_date" name="release_date" type="date" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Episode Count</label>'
        '<input id="episodes" name="episodes" type="number" placeholder="8" min="1" max="100" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Genre</label>'
        '<select id="genre" name="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div>'
    ),
    "You are a streaming analytics expert. Provide performance analysis for: Platform: {platform}, Type: {content_type}, Demographics: {demographics}, Release: {release_date}, Episodes: {episodes}, Genre: {genre}. Include: 1) Viewership/engagement predictions, 2) Release strategy (binge vs weekly), 3) Top 5 KPIs, 4) Competitive positioning, 5) Marketing channels, 6) Subscriber impact, 7) Renewal probability, 8) International expansion recommendations."
)

build("ai-dubbing-subtitling", "rose", "AI Dubbing & Subtitling Workflow",
    "Plan dubbing and subtitle localization",
    (
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Source Language</label>'
        '<select id="source_lang" name="source_lang" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>English</option><option>Spanish</option><option>French</option><option>German</option><option>Japanese</option><option>Korean</option><option>Mandarin</option><option>Hindi</option><option>Portuguese</option><option>Italian</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Target Language</label>'
        '<select id="target_lang" name="target_lang" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>English</option><option>Spanish</option><option>French</option><option>German</option><option>Japanese</option><option>Korean</option><option>Mandarin</option><option>Hindi</option><option>Portuguese</option><option>Italian</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Content Type</label>'
        '<select id="content_type" name="content_type" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Feature Film</option><option>TV Series</option><option>Documentary</option><option>Animation</option><option>Short Film</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Age Rating</label>'
        '<select id="age_rating" name="age_rating" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>G/PG</option><option>PG-13</option><option>R</option><option>TV-14</option><option>TV-MA</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Runtime (minutes)</label>'
        '<input id="runtime" name="runtime" type="number" placeholder="90" min="1" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Voice Style</label>'
        '<select id="voice_style" name="voice_style" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Natural/Cinematic</option><option>Broadcast/Formal</option><option>Casual/Conversational</option><option>Dramatic/Intense</option><option>Comedic</option></select></div>'
    ),
    "You are an expert in localization. Create a dubbing/subtitling workflow for: Source: {source_lang}, Target: {target_lang}, Type: {content_type}, Rating: {age_rating}, Runtime: {runtime}min, Style: {voice_style}. Provide: 1) Dub vs sub rec by region, 2) Lip-sync approach, 3) Cultural adaptation notes, 4) Voice casting criteria, 5) Subtitle reading speed guidelines, 6) Timeline/cost breakdown, 7) QA checklist, 8) Platform delivery specs."
)

build("ai-script-coverage", "teal", "AI Script Coverage",
    "Professional script coverage and reader's report",
    (
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Script Title *</label>'
        '<input id="title" name="title" placeholder="Title of the script" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Genre *</label>'
        '<select id="genre" name="genre" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Mystery</option><option>Noir</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Page Count *</label>'
        '<input id="pages" name="pages" type="number" placeholder="90" min="1" max="200" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Logline *</label>'
        '<textarea id="logline" name="logline" rows="2" placeholder="One-sentence story summary..." required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500 resize-none"></textarea></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Writer Experience</label>'
        '<select id="experience" name="experience" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>First-time writer</option><option>Has written before</option><option>Writers Guild member</option><option>Produced writer</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Format</label>'
        '<select id="format" name="format" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="feature">Feature Film</option><option value="tv-pilot">TV Pilot</option><option value="short">Short Film</option><option value="web-series">Web Series</option></select></div>'
    ),
    "You are a professional script reader. Write a coverage report for: Title: {title}, Genre: {genre}, Pages: {pages}, Logline: {logline}, Writer: {experience}, Format: {format}. Include: 1) LOGLINE, 2) TITLE & GENRE, 3) FORMATTING assessment, 4) SYNOPSIS (2-3 paragraph), 5) CHARACTERS, 6) COMMENTARY on structure/dialogue/pacing, 7) COMPARABLE TITLES, 8) PROS, 9) CONS, 10) OVERALL rating (Pass/Consider/Recommend) with justification."
)

build("ai-film-marketing", "orange", "AI Film Marketing",
    "Strategic film and TV marketing campaign planner",
    (
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Film Title</label>'
        '<input id="title" name="title" placeholder="Title of your film" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Genre</label>'
        '<select id="genre" name="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Distribution</label>'
        '<select id="platform" name="platform" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Theatrical</option><option>Netflix</option><option>Amazon Prime</option><option>Disney+</option><option>HBO Max</option><option>Theatrical + Streaming</option><option>Festival circuit</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Marketing Budget</label>'
        '<select id="budget" name="budget" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Grassroots (under $50K)</option><option>Moderate ($50K-$500K)</option><option>Major ($500K-$5M)</option><option>Studio-level ($5M+)</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Release Date</label>'
        '<input id="release_date" name="release_date" type="date" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Target Audience</label>'
        '<input id="audience" name="audience" placeholder="e.g. Adult men 18-34, families" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
    ),
    "You are a film marketing strategist. Create a campaign plan for: Title: {title}, Genre: {genre}, Platform: {platform}, Budget: {budget}, Release: {release_date}, Audience: {audience}. Provide: 1) 12-week campaign phases, 2) Key messages and taglines, 3) Social media strategy by platform, 4) Talent publicity, 5) Press strategy, 6) Poster/key art recommendations, 7) Trailer release plan, 8) Festival premiere strategy, 9) Influencer partnerships, 10) Opening weekend projections."
)

build("ai-post-production", "pink", "AI Post-Production Planner",
    "Plan post-production workflow",
    (
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Project Title</label>'
        '<input id="title" name="title" placeholder="Project title" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Runtime (minutes)</label>'
        '<input id="runtime" name="runtime" type="number" placeholder="95" min="1" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Editing Software</label>'
        '<select id="format" name="format" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white"><option value="">Select</option><option>Adobe Premiere Pro</option><option>Avid Media Composer</option><option>DaVinci Resolve</option><option>Final Cut Pro</option><option>Mixed</option></select></div>'
        '<div><label class="block text-sm font-medium text-gray-300 mb-1">Color Grade Style</label>'
        '<select id="tone" name="tone" class="w