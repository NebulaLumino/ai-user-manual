#!/usr/bin/env python3
import os

WS = "/Users/nebulalumino/.openclaw/workspace"
os.chdir(WS)

GLOBALS = '''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #0a0a0a;
  --foreground: #ededed;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
'''

def make_layout(title, desc):
    return '''import type { Metadata } from "next";
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
''' % (title, desc)

def make_route(prompt):
    safe_prompt = prompt.replace('"', '\\"').replace('\n', ' ')
    return '''import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://api.deepseek.com/v1",
});

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const keys = [
      "genre","logline","setting","tone","length","archetype",
      "title","format","budget","location","audience","platform",
      "content_type","demographics","release_date","episodes",
      "source_lang","target_lang","age_rating","runtime","voice_style",
      "pages","experience","protagonist_name","antagonist","supporting",
      "world_rules","conflict","resolution","themes","shooting_schedule",
      "characters","timeline","props","costumes","era","terrain","climate",
      "lighting","budget_amount","inconsistency_type","script_content",
      "festival_type","premiere_goal","bts_content_type","distribution",
      "dialogue_sample","reading_level","ep_num","season_count",
      "episode_runtime","pacing_notes","critics_praise","critics_concerns",
      "languages"
    ];

    let prompt = `%s`;
    for (const key of keys) {
      const val = body[key] || "";
      prompt = prompt.replace(new RegExp(`{${key}}`, "g"), String(val));
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
''' % prompt

def make_page(accent, title, form_fields):
    colors = {
        "violet": ("from-violet-400","to-violet-600","border-violet-500","text-violet-400","bg-violet-600 hover:bg-violet-700","bg-violet-500"),
        "blue": ("from-blue-400","to-blue-600","border-blue-500","text-blue-400","bg-blue-600 hover:bg-blue-700","bg-blue-500"),
        "amber": ("from-amber-400","to-amber-600","border-amber-500","text-amber-400","bg-amber-600 hover:bg-amber-700","bg-amber-500"),
        "rose": ("from-rose-400","to-rose-600","border-rose-500","text-rose-400","bg-rose-600 hover:bg-rose-700","bg-rose-500"),
        "teal": ("from-teal-400","to-teal-600","border-teal-500","text-teal-400","bg-teal-600 hover:bg-teal-700","bg-teal-500"),
        "orange": ("from-orange-400","to-orange-600","border-orange-500","text-orange-400","bg-orange-600 hover:bg-orange-700","bg-orange-500"),
        "pink": ("from-pink-400","to-pink-600","border-pink-500","text-pink-400","bg-pink-600 hover:bg-pink-700","bg-pink-500"),
        "cyan": ("from-cyan-400","to-cyan-600","border-cyan-500","text-cyan-400","bg-cyan-600 hover:bg-cyan-700","bg-cyan-500"),
        "lime": ("from-lime-400","to-lime-600","border-lime-500","text-lime-400","bg-lime-600 hover:bg-lime-700","bg-lime-500"),
        "emerald": ("from-emerald-400","to-emerald-600","border-emerald-500","text-emerald-400","bg-emerald-600 hover:bg-emerald-700","bg-emerald-500"),
        "red": ("from-red-400","to-red-600","border-red-500","text-red-400","bg-red-600 hover:bg-red-700","bg-red-500"),
        "yellow": ("from-yellow-400","to-yellow-600","border-yellow-500","text-yellow-400","bg-yellow-600 hover:bg-yellow-700","bg-yellow-500"),
        "purple": ("from-purple-400","to-purple-600","border-purple-500","text-purple-400","bg-purple-600 hover:bg-purple-700","bg-purple-500"),
        "sky": ("from-sky-400","to-sky-600","border-sky-500","text-sky-400","bg-sky-600 hover:bg-sky-700","bg-sky-500"),
        "zinc": ("from-zinc-400","to-zinc-600","border-zinc-500","text-zinc-400","bg-zinc-600 hover:bg-zinc-700","bg-zinc-500"),
        "indigo": ("from-indigo-400","to-indigo-600","border-indigo-500","text-indigo-400","bg-indigo-600 hover:bg-indigo-700","bg-indigo-500"),
        "fuchsia": ("from-fuchsia-400","to-fuchsia-600","border-fuchsia-500","text-fuchsia-400","bg-fuchsia-600 hover:bg-fuchsia-700","bg-fuchsia-500"),
        "stone": ("from-stone-400","to-stone-600","border-stone-500","text-stone-400","bg-stone-600 hover:bg-stone-700","bg-stone-500"),
        "neutral": ("from-neutral-400","to-neutral-600","border-neutral-500","text-neutral-400","bg-neutral-600 hover:bg-neutral-700","bg-neutral-500"),
        "slate": ("from-slate-400","to-slate-600","border-slate-500","text-slate-400","bg-slate-600 hover:bg-slate-700","bg-slate-500"),
    }
    g1, g2, fb, ta, bh, _ = colors[accent]
    return '''"use client";

import { useState } from "react";

export default function Home() {
  const [output, setOutput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form.entries()));
    setIsLoading(true);
    setOutput("");
    setError("");
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || "Generation failed");
      setOutput(json.result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white">
      <div className="max-w-5xl mx-auto px-6 py-12">
        <header className="mb-10">
          <h1 className="text-4xl font-bold bg-gradient-to-r %s %s bg-clip-text text-transparent mb-2">%s</h1>
        </header>
        <div className="grid md:grid-cols-2 gap-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            %s
            <button type="submit" disabled={isLoading} className={"w-full %s disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-colors"}>
              {isLoading ? "Generating..." : "Generate"}
            </button>
          </form>
          <div>
            {error && <div className="bg-red-900/30 border border-red-700 text-red-300 rounded-lg p-4 mb-4">{error}</div>}
            {isLoading && (
              <div className="bg-gray-800 rounded-xl p-8 text-center space-y-3">
                <div className="flex justify-center gap-2">
                  {[0,1,2].map(i => <span key={i} className={"w-3 h-3 %s rounded-full animate-bounce"} style={{animationDelay: "${i*0.1}s"}} />)}
                </div>
                <p className="text-gray-400 text-sm">Generating...</p>
              </div>
            )}
            {output && (
              <div className="bg-gray-800 rounded-xl p-6">
                <h3 className={"text-sm font-semibold mb-3 " + "%s"}>Result</h3>
                <pre className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed max-h-[600px] overflow-y-auto">{output}</pre>
              </div>
            )}
            {!output && !isLoading && (
              <div className="bg-gray-800/50 rounded-xl p-8 text-center text-gray-500 border-2 border-dashed border-gray-700">
                <p>Output will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
''' % (g1, g2, title, form_fields, bh, ta, ta)

def field_text(label, input_html, id):
    return '<div><label class="block text-sm font-medium text-gray-300 mb-1">%s</label>%s</div>' % (label, input_html.replace('id="%s"' % id, 'id="%s" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white placeholder-gray-500"' % id).replace('FOCUS', ''))

def select_field(label, id, options_html):
    opts = ''.join(options_html)
    return '<div><label class="block text-sm font-medium text-gray-300 mb-1">%s</label><select id="%s" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-FOCUS text-white">%s</select></div>' % (label, id, opts)

def select_opt(val, label=None):
    return '<option value="%s">%s</option>' % (val, label or val)

def build_app(dir_name, accent, title, desc, fields_html, prompt):
    app_dir = os.path.join(WS, dir_name)
    if os.path.exists(app_dir):
        print("SKIP " + dir_name)
        return
    os.makedirs(os.path.join(app_dir, "src/app/api/generate"), exist_ok=True)
    with open(os.path.join(app_dir, "src/app/globals.css"), "w") as f:
        f.write(GLOBALS)
    with open(os.path.join(app_dir, "src/app/layout.tsx"), "w") as f:
        f.write(make_layout(title, desc))
    with open(os.path.join(app_dir, "src/app/page.tsx"), "w") as f:
        f.write(make_page(accent, title, fields_html))
    with open(os.path.join(app_dir, "src/app/api/generate/route.ts"), "w") as f:
        f.write(make_route(prompt))
    print("BUILT " + dir_name)

# ─── BATCH 2 (2116-2120) ───────────────────────────────────────────────────

build_app("ai-pre-production", "blue",
    "AI Pre-Production Planner",
    "Plan comprehensive film and TV pre-production workflows",
    '''
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Project Title</label><input id="title" placeholder="Your project title" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Genre</label><select id="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white"><option value="">Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Format</label><select id="format" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white"><option value="short">Short Film</option><option value="feature">Feature Film</option><option value="tv-pilot">TV Pilot</option><option value="tv-season">TV Season</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Budget Tier</label><select id="budget" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white"><option value="micro">Micro (under $50K)</option><option value="low">Low ($50K-$500K)</option><option value="mid">Mid ($500K-$5M)</option><option value="studio">Studio ($5M+)</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Primary Location</label><input id="location" placeholder="Main shooting location" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Target Audience</label><input id="audience" placeholder="e.g. Adults 18-34, families" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"></div>
    ''',
    """You are an expert film production manager. Create a comprehensive pre-production plan for:
Project Title: {title}
Genre: {genre}
Format: {format}
Budget Tier: {budget}
Shooting Location: {location}
Target Audience: {audience}

Provide: 1) Detailed timeline from greenlight to production start with weekly milestones, 2) Key crew positions and hiring order, 3) Script breakdown priorities by department, 4) Casting process timeline and strategy, 5) Location scouting checklist, 6) Budget allocation breakdown by category (percentage), 7) Legal/permit requirements, 8) Risk assessment with mitigation plans, 9) Day-one readiness checklist."""
)

build_app("ai-streaming-analytics", "amber",
    "AI Streaming Analytics",
    "Analyze and predict streaming platform performance",
    '''
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Platform</label><select id="platform" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white"><option value="">Select platform</option><option>Netflix</option><option>Amazon Prime</option><option>Disney+</option><option>HBO Max</option><option>Hulu</option><option>Apple TV+</option><option>Peacock</option><option>Paramount+</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Content Type</label><select id="content_type" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white"><option value="">Select type</option><option>Original Series</option><option>Original Film</option><option>Licensed Content</option><option>Documentary</option><option>Reality Show</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Target Demographics</label><input id="demographics" placeholder="e.g. 18-34 males, 25-54 females" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Release Date</label><input id="release_date" type="date" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Episode Count</label><input id="episodes" type="number" placeholder="8" min="1" max="100" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Genre</label><select id="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white"><option value="">Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div>
    ''',
    """You are a streaming analytics expert. Provide a comprehensive performance analysis for:
Platform: {platform}
Content Type: {content_type}
Target Demographics: {demographics}
Release Date: {release_date}
Episode Count: {episodes}
Genre: {genre}

Include: 1) Predicted viewership and engagement metrics, 2) Optimal release strategy (binge vs. weekly drops), 3) Top 5 KPIs to track, 4) Competitive positioning vs. similar titles, 5) Marketing channel recommendations, 6) Subscriber acquisition impact, 7) Second season renewal probability, 8) International expansion recommendations."""
)

build_app("ai-dubbing-subtitling", "rose",
    "AI Dubbing & Subtitling Workflow",
    "Plan professional dubbing and subtitle localization workflows",
    '''
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Source Language</label><select id="source_lang" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white"><option value="">Select</option><option>English</option><option>Spanish</option><option>French</option><option>German</option><option>Japanese</option><option>Korean</option><option>Mandarin</option><option>Hindi</option><option>Portuguese</option><option>Italian</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Target Language</label><select id="target_lang" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white"><option value="">Select</option><option>English</option><option>Spanish</option><option>French</option><option>German</option><option>Japanese</option><option>Korean</option><option>Mandarin</option><option>Hindi</option><option>Portuguese</option><option>Italian</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Content Type</label><select id="content_type" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white"><option value="">Select</option><option>Feature Film</option><option>TV Series</option><option>Documentary</option><option>Animation</option><option>Short Film</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Age Rating</label><select id="age_rating" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white"><option value="">Select</option><option>G/PG</option><option>PG-13</option><option>R</option><option>TV-14</option><option>TV-MA</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Runtime (minutes)</label><input id="runtime" type="number" placeholder="90" min="1" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Voice Style</label><select id="voice_style" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white"><option value="">Select</option><option>Natural/Cinematic</option><option>Broadcast/Formal</option><option>Casual/Conversational</option><option>Dramatic/Intense</option><option>Comedic/Tongue-in-cheek</option></select></div>
    ''',
    """You are an expert in localization and international film distribution. Create a dubbing and subtitling workflow for:
Source Language: {source_lang}
Target Language: {target_lang}
Content Type: {content_type}
Age Rating: {age_rating}
Runtime: {runtime} minutes
Voice Style: {voice_style}

Provide: 1) Dubbing vs. subtitling recommendation by region, 2) Lip-sync or whisper dubbing approach, 3) Cultural adaptation notes, 4) Voice actor casting criteria, 5) Subtitle reading speed guidelines, 6) Timeline and cost breakdown, 7) QA checklist, 8) Platform-specific delivery specs."""
)

build_app("ai-script-coverage", "teal",
    "AI Script Coverage",
    "Professional script coverage and reader's report generator",
    '''
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Script Title *</label><input id="title" placeholder="Title of the script" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Genre *</label><select id="genre" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white"><option value="">Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Mystery</option><option>Noir</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Page Count *</label><input id="pages" type="number" placeholder="90" min="1" max="200" required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Logline *</label><textarea id="logline" rows="2" placeholder="One-sentence story summary..." required class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white placeholder-gray-500 resize-none"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Writer Experience</label><select id="experience" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white"><option value="">Select</option><option>First-time writer</option><option>Has written before</option><option>Writers Guild member</option><option>Produced writer</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Format</label><select id="format" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white"><option value="feature">Feature Film</option><option value="tv-pilot">TV Pilot</option><option value="short">Short Film</option><option value="web-series">Web Series</option></select></div>
    ''',
    """You are a professional script reader for a major studio. Write a comprehensive coverage report for:
Title: {title}
Genre: {genre}
Page Count: {pages}
Logline: {logline}
Writer Experience: {experience}
Format: {format}

Provide a detailed reader report including: 1) LOGLINE, 2) TITLE & GENRE, 3) FORMATTING assessment, 4) SYNOPSIS (2-3 paragraph plot summary), 5) CHARACTERS assessment, 6) COMMENTARY on structure/dialogue/pacing, 7) COMPARABLE TITLES, 8) PROS, 9) CONS, 10) OVERALL rating (Pass/Consider/Recommend) with justification."""
)

# ─── BATCH 3 (2121-2125) ───────────────────────────────────────────────────

build_app("ai-film-marketing", "orange",
    "AI Film Marketing",
    "Strategic film and TV marketing campaign planner",
    '''
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Film Title</label><input id="title" placeholder="Title of your film" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-orange-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Genre</label><select id="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-orange-500 text-white"><option value="">Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Distribution Platform</label><select id="platform" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-orange-500 text-white"><option value="">Select</option><option>Theatrical</option><option>Netflix</option><option>Amazon Prime</option><option>Disney+</option><option>HBO Max</option><option>Theatrical + Streaming</option><option>Festival circuit</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Marketing Budget Tier</label><select id="budget" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-orange-500 text-white"><option value="">Select</option><option>Grassroots (under $50K)</option><option>Moderate ($50K-$500K)</option><option>Major ($500K-$5M)</option><option>Studio-level ($5M+)</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Release Date</label><input id="release_date" type="date" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-orange-500 text-white"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Target Audience</label><input id="audience" placeholder="e.g. Adult men 18-34, families with kids" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-orange-500 text-white placeholder-gray-500"></div>
    ''',
    """You are a film marketing strategist. Create a comprehensive marketing campaign plan for:
Film Title: {title}
Genre: {genre}
Distribution Platform: {platform}
Marketing Budget: {budget}
Release Date: {release_date}
Target Audience: {audience}

Provide: 1) Campaign phases with timeline (12 weeks pre-release to post-release), 2) Key marketing messages and taglines, 3) Social media strategy by platform (TikTok, Instagram, Twitter/X, YouTube), 4) Talent publicity opportunities, 5) Press and media strategy, 6) Poster and key art recommendations, 7) Trailer release strategy, 8) Festival premiere strategy, 9) Influencer and creator partnerships, 10) Opening weekend projections."""
)

build_app("ai-post-production", "pink",
    "AI Post-Production Planner",
    "Plan the post-production workflow from edit to delivery",
    '''
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Project Title</label><input id="title" placeholder="Project title" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-pink-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Runtime (minutes)</label><input id="runtime" type="number" placeholder="95" min="1" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-pink-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Editing Software</label><select id="format" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-pink-500 text-white"><option value="">Select</option><option>Adobe Premiere Pro</option><option>Avid Media Composer</option><option>DaVinci Resolve</option><option>Final Cut Pro</option><option>不明/混合</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Color Grade Style</label><select id="tone" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-pink-500 text-white"><option value="">Select</option><option>Natural/Realistic</option><option>High contrast cinematic</option><option>Desaturated gritty</option><option>Vibrant stylized</option><option>Period authentic</option><option>Noir/black & white</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">VFX Complexity</label><select id="genre" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-pink-500 text-white"><option value="">Select</option><option>Minimal (no VFX)</option><option>Light (simple replacements)</option><option>Moderate (set extensions)</option><option>Heavy (full CGI)</option></select></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Delivery Platforms</label><input id="audience" placeholder="e.g. Netflix, theatrical, festival" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-pink-500 text-white placeholder-gray-500"></div>
    ''',
    """You are a post-production supervisor. Create a comprehensive post-production workflow plan for:
Project Title: {title}
Runtime: {runtime} minutes
Editing Software: {format}
Color Grade Style: {tone}
VFX Complexity: {genre}
Delivery Platforms: {audience}

Provide: 1) Phases: assembly cut, director's cut, fine cut, picture lock, 2) Sound design and mix workflow (DME), 3) Color grading pipeline, 4) VFX breakdown and vendor handoff, 5) Music and score spotting notes, 6) Deliverable specs for each platform, 7) Quality control checkpoints, 8) Typical timeline by phase, 9) Budget allocation across post departments."""
)

build_app("ai-casting-breakdown", "cyan",
    "AI Casting Breakdown",
    "Create professional casting breakdowns and character analyses",
    '''
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Project Title</label><input id="title" placeholder="Project title" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500 text-white placeholder-gray-500"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Protagonist Description</label><textarea id="protagonist_name" rows="3" placeholder="Age, appearance, personality, arc..." class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500 text-white placeholder-gray-500 resize-none"></div>
    <div><label class="block text-sm font-medium text-gray-300 mb-1">Antagonist /