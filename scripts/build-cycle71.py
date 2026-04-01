#!/usr/bin/env python3
"""Build all 20 Cycle 71 apps"""
import os
import shutil

WS = "/Users/nebulalumino/.openclaw/workspace"

# App definitions: (app_dir, accent, title, description, form_fields_html, prompt_template)
APPS = [
  ("ai-screenwriting", "violet", "AI Screenwriting", "Generate professional screenplays",
   """
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Genre *</label><select id='genre' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white'><option value=''>Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Mystery</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Logline *</label><textarea id='logline' rows='3' placeholder='A compelling one-sentence summary...' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500 resize-none'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Setting</label><input id='setting' placeholder='Time period and location' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Tone</label><select id='tone' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white'><option value=''>Select tone</option><option>Dark & gritty</option><option>Light & comedic</option><option>Serious & dramatic</option><option>Whimsical</option><option>Noir</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Format</label><select id='length' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white'><option value='short'>Short Film (5-15 min)</option><option value='feature'>Feature Film (90-120 min)</option><option value='tv-episode'>TV Episode (42 min)</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Protagonist Archetype</label><input id='archetype' placeholder='e.g. The Rebel, The Mentor, The Hero' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500'></textarea></div>
   """,
   """You are an expert screenwriter. Write a compelling screenplay excerpt based on the following:\n\nGenre: {genre}\nLogline: {logline}\nSetting: {setting}\nTone: {tone}\nFormat: {length}\nProtagonist Archetype: {archetype}\n\nInclude: scene heading, action lines, character names, dialogue, and parentheticals. Format it as a proper screenplay. Include act structure markers (FADE IN, etc.) and scene beats. Write approximately 8-12 pages worth of content."""),

  ("ai-pre-production", "blue", "AI Pre-Production Planner", "Plan film/TV pre-production",
   """
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Project Title</label><input id='title' placeholder='Your project title' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Genre</label><select id='genre' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white'><option value=''>Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Format</label><select id='format' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white'><option value='short'>Short Film</option><option value='feature'>Feature Film</option><option value='tv-pilot'>TV Pilot</option><option value='tv-season'>TV Season</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Budget Tier</label><select id='budget' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white'><option value='micro'>Micro Budget (under $50K)</option><option value='low'>Low Budget ($50K-$500K)</option><option value='mid'>Mid Budget ($500K-$5M)</option><option value='studio'>Studio Budget ($5M+)</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Shooting Location</label><input id='location' placeholder='Primary shooting location' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Target Audience</label><input id='audience' placeholder='e.g. Adults 18-34, families, genre fans' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500'></textarea></div>
   """,
   """You are an expert film production manager. Create a comprehensive pre-production plan for:\n\nProject Title: PLACEHOLDER_TITLE\nGenre: {genre}\nFormat: {format}\nBudget Tier: {budget}\nShooting Location: {location}\nTarget Audience: {audience}\n\nProvide a detailed pre-production checklist including: 1) Timeline with milestones from greenlight to production start, 2) Key departments and crew needs, 3) Script breakdown priorities, 4) Casting process timeline, 5) Location scouting priorities, 6) Budget allocation by category, 7) Permits and legal requirements, 8) Equipment and facilities needs."""),

  ("ai-streaming-analytics", "amber", "AI Streaming Analytics", "Analyze streaming performance",
   """
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Platform</label><select id='platform' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white'><option value=''>Select platform</option><option>Netflix</option><option>Amazon Prime Video</option><option>Disney+</option><option>HBO Max</option><option>Hulu</option><option>Apple TV+</option><option>Peacock</option><option>Paramount+</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Content Type</label><select id='content_type' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white'><option value=''>Select type</option><option>Original Series</option><option>Original Film</option><option>Licensed Content</option><option>Documentary</option><option>Reality Show</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Target Demographics</label><input id='demographics' placeholder='e.g. 18-34 males, 25-54 females, families' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Release Date</label><input id='release_date' type='date' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Episode Count</label><input id='episodes' type='number' placeholder='8' min='1' max='100' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Genre</label><select id='genre' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white'><option value=''>Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div>
   """,
   """You are a streaming analytics expert. Provide a comprehensive streaming performance analysis and strategy for:\n\nPlatform: {platform}\nContent Type: {content_type}\nTarget Demographics: {demographics}\nRelease Date: {release_date}\nEpisode Count: {episodes}\nGenre: {genre}\n\nInclude: 1) Predicted viewership metrics and engagement rates, 2) Optimal release strategy (binge vs. weekly), 3) Key performance indicators to track, 4) Competitive positioning against similar titles, 5) Marketing channel recommendations, 6) Subscriber acquisition impact estimate, 7) Second season renewal probability factors."""),

  ("ai-dubbing-subtitling", "rose", "AI Dubbing & Subtitling Workflow", "Plan dubbing and subtitle workflows",
   """
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Source Language</label><select id='source_lang' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white'><option value=''>Select language</option><option>English</option><option>Spanish</option><option>French</option><option>German</option><option>Japanese</option><option>Korean</option><option>Mandarin</option><option>Hindi</option><option>Portuguese</option><option>Italian</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Target Language</label><select id='target_lang' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white'><option value=''>Select language</option><option>English</option><option>Spanish</option><option>French</option><option>German</option><option>Japanese</option><option>Korean</option><option>Mandarin</option><option>Hindi</option><option>Portuguese</option><option>Italian</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Content Type</label><select id='content_type' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white'><option value=''>Select type</option><option>Feature Film</option><option>TV Series</option><option>Documentary</option><option>Animation</option><option>Short Film</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Age Rating</label><select id='age_rating' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white'><option value=''>Select rating</option><option>G/PG</option><option>PG-13</option><option>R</option><option>TV-14</option><option>TV-MA</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Runtime (minutes)</label><input id='runtime' type='number' placeholder='90' min='1' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Voice Style</label><select id='voice_style' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-rose-500 text-white'><option value=''>Select style</option><option>Natural/Cinematic</option><option>Broadcast/Formal</option><option>Casual/Conversational</option><option>Dramatic/Intense</option><option>Comedic/Tongue-in-cheek</option></select></div>
   """,
   """You are an expert in localization and international film distribution. Create a comprehensive dubbing and subtitling workflow plan for:\n\nSource Language: {source_lang}\nTarget Language: {target_lang}\nContent Type: {content_type}\nAge Rating: {age_rating}\nRuntime: {runtime} minutes\nVoice Style: {voice_style}\n\nProvide: 1) Recommended dubbing vs. subtitling strategy by region, 2) Lip-sync vs. whisper dubbing approach, 3) Cultural adaptation notes for dialogue, 4) Voice actor casting criteria (gender, age range, accent), 5) Subtitle reading speed guidelines, 6) Timeline and cost estimates per workflow stage, 7) Quality assurance checklist, 8) Platform-specific delivery requirements."""),

  ("ai-script-coverage", "teal", "AI Script Coverage", "Professional script coverage and reader's report",
   """
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Script Title *</label><input id='title' placeholder='Title of the script' required class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Genre *</label><select id='genre' required class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white'><option value=''>Select genre</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Mystery</option><option>Noir</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Page Count *</label><input id='pages' type='number' placeholder='90' min='1' max='200' required class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white placeholder-gray-500'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Logline *</label><textarea id='logline' rows='2' placeholder='One-sentence story summary...' required class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white placeholder-gray-500 resize-none'></textarea></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Writer Experience</label><select id='experience' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white'><option value=''>Select experience</option><option>First-time writer</option><option>Has written before</option><option>Writers Guild member</option><option>Produced writer</option></select></div>
   <div><label class='block text-sm font-medium text-gray-300 mb-1'>Format</label><select id='format' class='w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-teal-500 text-white'><option value='feature'>Feature Film</option><option value='tv-pilot'>TV Pilot</option><option value='short'>Short Film</option><option value='web-series'>Web Series</option></select></div>
   """,
   """You are a professional script reader for a major studio. Write a comprehensive script coverage report for:\n\nTitle: PLACEHOLDER_TITLE\nGenre: {genre}\nPage Count: {pages}\nLogline: {logline}\nWriter Experience: {experience}\nFormat: {format}\n\nProvide a detailed reader's report including: 1) LOGLINE (one compelling sentence), 2) TITLE (with genre), 3) FORMATTING assessment, 4) SYNOPSIS (2-3 paragraph detailed plot summary), 5) CHARACTERS assessment with key roles, 6) COMMENTARY on story structure, dialogue quality, and pacing, 7) COMPARABLE TITLES, 8) PROS (strengths), 9) CONS (weaknesses), 10) OVERALL rating on a scale of Pass/Consider/Recommend with detailed justification."""),
]

ACCENTS = {
  "violet": ("from-violet-400", "to-violet-600", "focus:border-violet-500", "text-violet-400", "bg-violet-500", "bg-violet-600/hover:bg-violet-700"),
  "blue": ("from-blue-400", "to-blue-600", "focus:border-blue-500", "text-blue-400", "bg-blue-500", "bg-blue-600/hover:bg-blue-700"),
  "amber": ("from-amber-400", "to-amber-600", "focus:border-amber-500", "text-amber-400", "bg-amber-500", "bg-amber-600/hover:bg-amber-700"),
  "rose": ("from-rose-400", "to-rose-600", "focus:border-rose-500", "text-rose-400", "bg-rose-500", "bg-rose-600/hover:bg-rose-700"),
  "teal": ("from-teal-400", "to-teal-600", "focus:border-teal-500", "text-teal-400", "bg-teal-500", "bg-teal-600/hover:bg-teal-700"),
  "orange": ("from-orange-400", "to-orange-600", "focus:border-orange-500", "text-orange-400", "bg-orange-500", "bg-orange-600/hover:bg-orange-700"),
  "pink": ("from-pink-400", "to-pink-600", "focus:border-pink-500", "text-pink-400", "bg-pink-500", "bg-pink-600/hover:bg-pink-700"),
  "cyan": ("from-cyan-400", "to-cyan-600", "focus:border-cyan-500", "text-cyan-400", "bg-cyan-500", "bg-cyan-600/hover:bg-cyan-700"),
  "lime": ("from-lime-400", "to-lime-600", "focus:border-lime-500", "text-lime-400", "bg-lime-500", "bg-lime-600/hover:bg-lime-700"),
  "emerald": ("from-emerald-400", "to-emerald-600", "focus:border-emerald-500", "text-emerald-400", "bg-emerald-500", "bg-emerald-600/hover:bg-emerald-700"),
  "red": ("from-red-400", "to-red-600", "focus:border-red-500", "text-red-400", "bg-red-500", "bg-red-600/hover:bg-red-700"),
  "yellow": ("from-yellow-400", "to-yellow-600", "focus:border-yellow-500", "text-yellow-400", "bg-yellow-500", "bg-yellow-600/hover:bg-yellow-700"),
  "purple": ("from-purple-400", "to-purple-600", "focus:border-purple-500", "text-purple-400", "bg-purple-500", "bg-purple-600/hover:bg-purple-700"),
  "sky": ("from-sky-400", "to-sky-600", "focus:border-sky-500", "text-sky-400", "bg-sky-500", "bg-sky-600/hover:bg-sky-700"),
  "zinc": ("from-zinc-400", "to-zinc-600", "focus:border-zinc-500", "text-zinc-400", "bg-zinc-500", "bg-zinc-600/hover:bg-zinc-700"),
  "indigo": ("from-indigo-400", "to-indigo-600", "focus:border-indigo-500", "text-indigo-400", "bg-indigo-500", "bg-indigo-600/hover:bg-indigo-700"),
  "fuchsia": ("from-fuchsia-400", "to-fuchsia-600", "focus:border-fuchsia-500", "text-fuchsia-400", "bg-fuchsia-500", "bg-fuchsia-600/hover:bg-fuchsia-700"),
  "stone": ("from-stone-400", "to-stone-600", "focus:border-stone-500", "text-stone-400", "bg-stone-500", "bg-stone-600/hover:bg-stone-700"),
  "neutral": ("from-neutral-400", "to-neutral-600", "focus:border-neutral-500", "text-neutral-400", "bg-neutral-500", "bg-neutral-600/hover:bg-neutral-700"),
  "slate": ("from-slate-400", "to-slate-600", "focus:border-slate-500", "text-slate-400", "bg-slate-500", "bg-slate-600/hover:bg-slate-700"),
}

GLOBALS = """@tailwind base;
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
"""

LAYOUT = """import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PLACEHOLDER_TITLE",
  description: "PLACEHOLDER_DESC",
};

export default function RootLayout({{
  children,
}}: Readonly<{{
  children: React.ReactNode;
}}>) {{
  return (
    <html lang="en">
      <body>{{children}}</body>
    </html>
  );
}}
"""

ROUTE = """import {{ NextRequest, NextResponse }} from "next/server";
import OpenAI from "openai";

const client = new OpenAI({{
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://api.deepseek.com/v1",
}});

export async function POST(req: NextRequest) {{
  try {{
    const body = await req.json();
    const prompt = `{prompt}`;

    const substituted = prompt
      .replaceAll("{{genre}}", body.genre || "")
      .replaceAll("{{logline}}", body.logline || "")
      .replaceAll("{{setting}}", body.setting || "")
      .replaceAll("{{tone}}", body.tone || "")
      .replaceAll("{{length}}", body.length || "")
      .replaceAll("{{archetype}}", body.archetype || "")
      .replaceAll("{PLACEHOLDER_TITLE}", body.title || "")
      .replaceAll("{{format}}", body.format || "")
      .replaceAll("{{budget}}", body.budget || "")
      .replaceAll("{{location}}", body.location || "")
      .replaceAll("{{audience}}", body.audience || "")
      .replaceAll("{{platform}}", body.platform || "")
      .replaceAll("{{content_type}}", body.content_type || "")
      .replaceAll("{{demographics}}", body.demographics || "")
      .replaceAll("{{release_date}}", body.release_date || "")
      .replaceAll("{{episodes}}", String(body.episodes || ""))
      .replaceAll("{{source_lang}}", body.source_lang || "")
      .replaceAll("{{target_lang}}", body.target_lang || "")
      .replaceAll("{{age_rating}}", body.age_rating || "")
      .replaceAll("{{runtime}}", String(body.runtime || ""))
      .replaceAll("{{voice_style}}", body.voice_style || "")
      .replaceAll("{{pages}}", String(body.pages || ""))
      .replaceAll("{{experience}}", body.experience || "")
      .replaceAll("{{protagonist_name}}", body.protagonist_name || "")
      .replaceAll("{{antagonist}}", body.antagonist || "")
      .replaceAll("{{supporting}}", body.supporting || "")
      .replaceAll("{{world_rules}}", body.world_rules || "")
      .replaceAll("{{conflict}}", body.conflict || "")
      .replaceAll("{{resolution}}", body.resolution || "")
      .replaceAll("{{themes}}", body.themes || "")
      .replaceAll("{{shooting_schedule}}", body.shooting_schedule || "")
      .replaceAll("{{characters}}", body.characters || "")
      .replaceAll("{{timeline}}", body.timeline || "")
      .replaceAll("{{props}}", body.props || "")
      .replaceAll("{{costumes}}", body.costumes || "")
      .replaceAll("{{era}}", body.era || "")
      .replaceAll("{{terrain}}", body.terrain || "")
      .replaceAll("{{climate}}", body.climate || "")
      .replaceAll("{{lighting}}", body.lighting || "")
      .replaceAll("{{budget_amount}}", body.budget_amount || "")
      .replaceAll("{{inconsistency_type}}", body.inconsistency_type || "")
      .replaceAll("{{script_content}}", body.script_content || "")
      .replaceAll("{{festival_type}}", body.festival_type || "")
      .replaceAll("{{premiere_goal}}", body.premiere_goal || "")
      .replaceAll("{{bts_content_type}}", body.bts_content_type || "")
      .replaceAll("{{distribution}}", body.distribution || "")
      .replaceAll("{{dialogue_sample}}", body.dialogue_sample || "")
      .replaceAll("{{reading_level}}", body.reading_level || "")
      .replaceAll("{{ep_num}}", String(body.ep_num || ""))
      .replaceAll("{{season_count}}", String(body.season_count || ""))
      .replaceAll("{{episode_runtime}}", String(body.episode_runtime || ""))
      .replaceAll("{{pacing_notes}}", body.pacing_notes || "")
      .replaceAll("{{critics_praise}}", body.critics_praise || "")
      .replaceAll("{{critics_concerns}}", body.critics_concerns || "")
      .replaceAll("{{languages}}", body.languages || "");

    const completion = await client.chat.completions.create({{
      model: "deepseek-chat",
      messages: [
        {{ role: "system", content: "You are a world-class expert in this domain. Provide detailed, actionable, well-structured output." }},
        {{ role: "user", content: substituted }},
      ],
      temperature: 0.7,
      max_tokens: 2000,
    }});

    return NextResponse.json({{ result: completion.choices[0].message.content }});
  }} catch (err: any) {{
    return NextResponse.json({{ error: err.message }}, {{ status: 500 }});
  }}
}}
"""

def build_page_tsx(app_dir, accent, title, form_fields_html):
    g1, g2, fb, ta, ba, bh = ACCENTS[accent]
    return f'''"use client";

import {{ useState }} from "react";

export default function Home() {{
  const [output, setOutput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {{
    e.preventDefault();
    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form.entries()));
    setIsLoading(true);
    setOutput("");
    setError("");
    try {{
      const res = await fetch("/api/generate", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify(data),
      }});
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || "Generation failed");
      setOutput(json.result);
    }} catch (err: any) {{
      setError(err.message);
    }} finally {{
      setIsLoading(false);
    }}
  }}

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white">
      <div className="max-w-5xl mx-auto px-6 py-12">
        <header className="mb-10">
          <h1 className="text-4xl font-bold bg-gradient-to-r {g1} {g2} bg-clip-text text-transparent mb-2">PLACEHOLDER_TITLE</h1>
        </header>
        <div className="grid md:grid-cols-2 gap-8">
          <form onSubmit={{handleSubmit}} className="space-y-4">
            {form_fields_html}
            <button type="submit" disabled={{isLoading}} className="{{w-full {ba} disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-colors}}">
              {{isLoading ? "Generating..." : "Generate"}}
            </button>
          </form>
          <div>
            {{error && <div className="bg-red-900/30 border border-red-700 text-red-300 rounded-lg p-4 mb-4">{{error}}</div>}}
            {{isLoading && (
              <div className="bg-gray-800 rounded-xl p-8 text-center space-y-3">
                <div className="flex justify-center gap-2">
                  {{[0,1,2].map(i => <span key={{i}} className={{`w-3 h-3 {ta} rounded-full animate-bounce`}} style={{{{animationDelay: `${{i*0.1}}s`}}}} />)}}
                </div>
                <p className="text-gray-400 text-sm">Generating...</p>
              </div>
            )}}
            {{output && (
              <div className="bg-gray-800 rounded-xl p-6">
                <h3 className="{{ta}} font-semibold mb-3">Result</h3>
                <pre className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed max-h-[600px] overflow-y-auto">{{output}}</pre>
              </div>
            )}}
            {{!output && !isLoading && (
              <div className="bg-gray-800/50 rounded-xl p-8 text-center text-gray-500 border-2 border-dashed border-gray-700">
                <p>Output will appear here</p>
              </div>
            )}}
          </div>
        </div>
      </div>
    </div>
  );
}}
'''

for app_dir, accent, title, description, form_fields_html, prompt_template in APPS:
    app_path = os.path.join(WS, app_dir)
    os.makedirs(app_path, exist_ok=True)
    os.makedirs(os.path.join(app_path, "src/app/api/generate"), exist_ok=True)
    os.makedirs(os.path.join(app_path, "src/app"), exist_ok=True)

    with open(os.path.join(app_path, "src/app/globals.css"), "w") as f:
        f.write(GLOBALS)

    layout_content = LAYOUT.format(title=title, description=description)
    with open(os.path.join(app_path, "src/app/layout.tsx"), "w") as f:
        f.write(layout_content)

    page_content = build_page_tsx(app_dir, accent, title, form_fields_html)
    with open(os.path.join(app_path, "src/app/page.tsx"), "w") as f:
        f.write(page_content)

    route_content = ROUTE.replace('`{prompt}`', '`' + prompt_template.replace('`', '\\`') + '`')
    route_content = route_content.format(prompt=prompt_template)
    with open(os.path.join(app_path, "src/app/api/generate/route.ts"), "w") as f:
        f.write(route_content)

    print(f"Built {app_dir} ({accent})")

print("Batch 1 complete!")
