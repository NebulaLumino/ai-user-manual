#!/usr/bin/env python3
"""Generate all 20 app files - using proper React components"""
import os, json

WS = "/Users/nebulalumino/.openclaw/workspace"
with open(f"{WS}/scripts/genapps.json") as f:
    APPS = json.load(f)
with open(f"{WS}/scripts/genprompts.json") as f:
    PROMPTS = json.load(f)

G = '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n:root { --background: #0a0a0a; --foreground: #ededed; }\nbody { color: var(--foreground); background: var(--background); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }'

LAYOUT = 'import type { Metadata } from "next";\nimport "./globals.css";\n\nexport const metadata: Metadata = {\n  title: "%s",\n  description: "%s",\n};\n\nexport default function RootLayout({\n  children,\n}: Readonly<{\n  children: React.ReactNode;\n}>) {\n  return (\n    <html lang="en">\n      <body>{children}</body>\n    </html>\n  );\n}\n'

ROUTE_TPL = 'import { NextRequest, NextResponse } from "next/server";\nimport OpenAI from "openai";\n\nlet _client: OpenAI | null = null;\nfunction getClient() {\n  if (!_client) {\n    _client = new OpenAI({\n      apiKey: process.env.OPENAI_API_KEY,\n      baseURL: "https://api.deepseek.com/v1",\n    });\n  }\n  return _client;\n}\n\nexport async function POST(req: NextRequest) {\n  try {\n    const body = await req.json();\n    const keys = ["genre","logline","setting","tone","length","archetype","title","format","budget","location","audience","platform","content_type","demographics","release_date","episodes","source_lang","target_lang","age_rating","runtime","voice_style","pages","experience","protagonist_name","antagonist","supporting","world_rules","conflict","resolution","themes","shooting_schedule","characters","timeline","props","costumes","era","terrain","climate","lighting","budget_amount","inconsistency_type","script_content","festival_type","premiere_goal","bts_content_type","distribution","dialogue_sample","reading_level","ep_num","season_count","episode_runtime","pacing_notes","critics_praise","critics_concerns","languages"];\n    let prompt = `%s`;\n    for (const key of keys) {\n      prompt = prompt.replace(new RegExp("{" + key + "}", "g"), String(body[key] || ""));\n    }\n    const completion = await getClient().chat.completions.create({\n      model: "deepseek-chat",\n      messages: [\n        { role: "system", content: "You are a world-class expert in this domain. Provide detailed, actionable, well-structured output." },\n        { role: "user", content: prompt },\n      ],\n      temperature: 0.7,\n      max_tokens: 2000,\n    });\n    return NextResponse.json({ result: completion.choices[0].message.content });\n  } catch (err: any) {\n    return NextResponse.json({ error: err.message }, { status: 500 });\n  }\n}\n'

ACCENTS = {
    "violet": ("from-violet-400","to-violet-600","text-violet-400","bg-violet-600 hover:bg-violet-700"),
    "blue": ("from-blue-400","to-blue-600","text-blue-400","bg-blue-600 hover:bg-blue-700"),
    "amber": ("from-amber-400","to-amber-600","text-amber-400","bg-amber-600 hover:bg-amber-700"),
    "rose": ("from-rose-400","to-rose-600","text-rose-400","bg-rose-600 hover:bg-rose-700"),
    "teal": ("from-teal-400","to-teal-600","text-teal-400","bg-teal-600 hover:bg-teal-700"),
    "orange": ("from-orange-400","to-orange-600","text-orange-400","bg-orange-600 hover:bg-orange-700"),
    "pink": ("from-pink-400","to-pink-600","text-pink-400","bg-pink-600 hover:bg-pink-700"),
    "cyan": ("from-cyan-400","to-cyan-600","text-cyan-400","bg-cyan-600 hover:bg-cyan-700"),
    "lime": ("from-lime-400","to-lime-600","text-lime-400","bg-lime-600 hover:bg-lime-700"),
    "emerald": ("from-emerald-400","to-emerald-600","text-emerald-400","bg-emerald-600 hover:bg-emerald-700"),
    "red": ("from-red-400","to-red-600","text-red-400","bg-red-600 hover:bg-red-700"),
    "yellow": ("from-yellow-400","to-yellow-600","text-yellow-400","bg-yellow-600 hover:bg-yellow-700"),
    "purple": ("from-purple-400","to-purple-600","text-purple-400","bg-purple-600 hover:bg-purple-700"),
    "sky": ("from-sky-400","to-sky-600","text-sky-400","bg-sky-600 hover:bg-sky-700"),
    "zinc": ("from-zinc-400","to-zinc-600","text-zinc-400","bg-zinc-600 hover:bg-zinc-700"),
    "indigo": ("from-indigo-400","to-indigo-600","text-indigo-400","bg-indigo-600 hover:bg-indigo-700"),
    "fuchsia": ("from-fuchsia-400","to-fuchsia-600","text-fuchsia-400","bg-fuchsia-600 hover:bg-fuchsia-700"),
    "stone": ("from-stone-400","to-stone-600","text-stone-400","bg-stone-600 hover:bg-stone-700"),
    "neutral": ("from-neutral-400","to-neutral-600","text-neutral-400","bg-neutral-600 hover:bg-neutral-700"),
    "slate": ("from-slate-400","to-slate-600","text-slate-400","bg-slate-600 hover:bg-slate-700"),
}

# Form components as Python strings - these are JSX React components
def f1(id, label, type="text", placeholder="", required=False, options=None, rows=0):
    req = " required" if required else ""
    if options:
        opts = "".join(f'<option key="{o}" value="{o}">{o}</option>' for o in options)
        return f'<div><label className="block text-sm font-medium text-gray-300 mb-1">{label}</label><select id="{id}" name="{id}" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white"{req}>{opts}</select></div>'
    elif rows > 0:
        return f'<div><label className="block text-sm font-medium text-gray-300 mb-1">{label}</label><textarea id="{id}" name="{id}" rows={rows} placeholder="{placeholder}" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500 resize-none"{req}></textarea></div>'
    else:
        tp = 'type="date"' if type == "date" else 'type="number"' if type == "number" else ""
        ph = f'placeholder="{placeholder}"' if placeholder else ""
        return f'<div><label className="block text-sm font-medium text-gray-300 mb-1">{label}</label><input id="{id}" name="{id}" {tp} {ph} className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"{req}></div>'

def gen_form(fields):
    return '<FormFields />'

def make_page(accent, title, fields_html):
    g1,g2,ta,bh = ACCENTS[accent]
    return (
        '"use client";\n\n'
        'import { useState } from "react";\n'
        + fields_html + '\n\n'
        'export default function Home() {\n'
        '  const [output, setOutput] = useState("");\n'
        '  const [isLoading, setIsLoading] = useState(false);\n'
        '  const [error, setError] = useState("");\n\n'
        '  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {\n'
        '    e.preventDefault();\n'
        '    const form = e.currentTarget;\n'
        '    const data = Object.fromEntries(new FormData(form.entries()));\n'
        '    setIsLoading(true); setOutput(""); setError("");\n'
        '    try {\n'
        '      const res = await fetch("/api/generate", {\n'
        '        method: "POST",\n'
        '        headers: { "Content-Type": "application/json" },\n'
        '        body: JSON.stringify(data),\n'
        '      });\n'
        '      const json = await res.json();\n'
        '      if (!res.ok) throw new Error(json.error || "Generation failed");\n'
        '      setOutput(json.result);\n'
        '    } catch (err: any) { setError(err.message); }\n'
        '    finally { setIsLoading(false); }\n'
        '  }\n\n'
        '  return (\n'
        '    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white">\n'
        '      <div className="max-w-5xl mx-auto px-6 py-12">\n'
        '        <header className="mb-10">\n'
        '          <h1 className="text-4xl font-bold bg-gradient-to-r %s %s bg-clip-text text-transparent mb-2">%s</h1>\n'
        '        </header>\n'
        '        <div className="grid md:grid-cols-2 gap-8">\n'
        '          <form onSubmit={handleSubmit} className="space-y-4">\n'
        '            <FormFields />\n'
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
    ) % (g1, g2, title, bh, ta, ta)

def make_form_component(fields_html):
    return (
        'export default function FormFields() {\n'
        '  return (\n'
        '    <>\n'
        '    ' + fields_html + '\n'
        '    </>\n'
        '  );\n'
        '}\n'
    )

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def build_form(accent, fields):
    """Generate form component HTML for an app"""
    g1,g2,ta,bh = ACCENTS[accent]
    fb = "border-" + ta.split("-")[0] + "-500"  # e.g. "border-blue-500"
    # Replace placeholder with actual border class
    return fields.replace("focus:border-blue-500", f"focus:outline-none {fb}")

# Field generators per app (accent, HTML fields)
APP_FORMS = {
    "ai-screenwriting": (
        "violet",
        '<div><label className="block text-sm font-medium text-gray-300 mb-1">Genre</label><select id="genre" name="genre" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Mystery</option><option>Noir</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Logline *</label><textarea id="logline" name="logline" rows={3} placeholder="A compelling one-sentence summary..." className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500 resize-none" required></textarea></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Setting</label><input id="setting" name="setting" placeholder="Time period and location" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500"></input></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Tone</label><select id="tone" name="tone" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white"><option value="">Select</option><option>Dark &amp; gritty</option><option>Light &amp; comedic</option><option>Serious &amp; dramatic</option><option>Whimsical</option><option>Noir</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Format</label><select id="length" name="length" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white"><option value="short">Short Film (5-15 min)</option><option value="feature">Feature Film (90-120 min)</option><option value="tv-episode">TV Episode (42 min)</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Protagonist Archetype</label><input id="archetype" name="archetype" placeholder="e.g. The Rebel, The Mentor, The Hero" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500"></input></div>'
    ),
}

# Default fallback forms for apps not yet defined
DEFAULT_FORMS = {
    "ai-pre-production": "blue",
    "ai-streaming-analytics": "amber",
    "ai-dubbing-subtitling": "rose",
    "ai-script-coverage": "teal",
    "ai-film-marketing": "orange",
    "ai-post-production": "pink",
    "ai-casting-breakdown": "cyan",
    "ai-tv-arc-planner": "lime",
    "ai-film-budget": "emerald",
    "ai-continuity-checker": "red",
    "ai-location-scouting": "yellow",
    "ai-film-festival-strategy": "purple",
    "ai-bts-content": "sky",
    "ai-dialogue-polisher": "zinc",
    "ai-binge-pacing": "indigo",
    "ai-film-review-aggregator": "fuchsia",
    "ai-bilingual-subtitles": "stone",
    "ai-talent-pitch": "neutral",
    "ai-props-set-design": "slate",
}

# Generic form template
def generic_form(accent, extra_fields=""):
    g1,g2,ta,bh = ACCENTS[accent]
    fb = "border-" + ta.replace("text-","").split("-")[0] + "-500"
    base = '<div><label className="block text-sm font-medium text-gray-300 mb-1">Title</label><input id="title" name="title" placeholder="Project title" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none ' + fb.replace("border-", "focus:outline-none focus:border-") + ' text-white placeholder-gray-500"></input></div>'
    return base + extra_fields

# Actually, let me just write all 20 forms manually with the correct accent colors
# Using proper JSX

def write_app(app, accent, title, desc, prompt, fields_html):
    g1,g2,ta,bh = ACCENTS[accent]
    fb = "border-" + ta.replace("text-","").split("-")[0] + "-500"
    # Fix the fields_html to use the correct border class
    fixed_fields = fields_html.replace("focus:border-blue-500", f"focus:outline-none {fb}")
    
    form_component = (
        'export default function FormFields() {\n'
        '  return (\n'
        '    <>\n'
        '    ' + fixed_fields.replace('"', '\\"').replace('\n', ' ').replace('    ', '') + '\n'
        '    </>\n'
        '  );\n'
        '}\n'
    )
    
    page = (
        '"use client";\n\n'
        'import { useState } from "react";\n'
        'import FormFields from "./FormFields";\n\n'
        'export default function Home() {\n'
        '  const [output, setOutput] = useState("");\n'
        '  const [isLoading, setIsLoading] = useState(false);\n'
        '  const [error, setError] = useState("");\n\n'
        '  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {\n'
        '    e.preventDefault();\n'
        '    const form = e.currentTarget;\n'
        '    const data = Object.fromEntries(new FormData(form.entries()));\n'
        '    setIsLoading(true); setOutput(""); setError("");\n'
        '    try {\n'
        '      const res = await fetch("/api/generate", {\n'
        '        method: "POST",\n'
        '        headers: { "Content-Type": "application/json" },\n'
        '        body: JSON.stringify(data),\n'
        '      });\n'
        '      const json = await res.json();\n'
        '      if (!res.ok) throw new Error(json.error || "Generation failed");\n'
        '      setOutput(json.result);\n'
        '    } catch (err: any) { setError(err.message); }\n'
        '    finally { setIsLoading(false); }\n'
        '  }\n\n'
        '  return (\n'
        '    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white">\n'
        '      <div className="max-w-5xl mx-auto px-6 py-12">\n'
        '        <header className="mb-10">\n'
        '          <h1 className="text-4xl font-bold bg-gradient-to-r %s %s bg-clip-text text-transparent mb-2">%s</h1>\n'
        '        </header>\n'
        '        <div className="grid md:grid-cols-2 gap-8">\n'
        '          <form onSubmit={handleSubmit} className="space-y-4">\n'
        '            <FormFields />\n'
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
    ) % (g1, g2, title, bh, ta, ta)

    w(f"{WS}/{app}/src/app/globals.css", G)
    w(f"{WS}/{app}/src/app/layout.tsx", LAYOUT % (title, desc))
    w(f"{WS}/{app}/src/app/page.tsx", page)
    w(f"{WS}/{app}/src/app/FormFields.tsx", form_component)
    w(f"{WS}/{app}/src/app/api/generate/route.ts", ROUTE_TPL % prompt)
    print(f"Done: {app}")

# All 20 app definitions
build_form("ai-screenwriting", "violet",
    "AI Screenwriting", "Generate professional screenplays",
    "You are an expert screenwriter. Write a compelling screenplay excerpt based on: Genre: {genre}, Logline: {logline}, Setting: {setting}, Tone: {tone}, Format: {length}, Protagonist: {archetype}. Include scene heading, action lines, character names, dialogue, and parentheticals. Format as proper screenplay with FADE IN, act structure markers, and scene beats.",
    '<div><label className="block text-sm font-medium text-gray-300 mb-1">Genre</label><select id="genre" name="genre" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Mystery</option><option>Noir</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Logline *</label><textarea id="logline" name="logline" rows={3} placeholder="A compelling one-sentence summary..." className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500 resize-none" required></textarea></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Setting</label><input id="setting" name="setting" placeholder="Time period and location" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500"></input></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Tone</label><select id="tone" name="tone" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white"><option value="">Select</option><option>Dark &amp; gritty</option><option>Light &amp; comedic</option><option>Serious &amp; dramatic</option><option>Whimsical</option><option>Noir</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Format</label><select id="length" name="length" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white"><option value="short">Short Film (5-15 min)</option><option value="feature">Feature Film (90-120 min)</option><option value="tv-episode">TV Episode (42 min)</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Protagonist Archetype</label><input id="archetype" name="archetype" placeholder="e.g. The Rebel, The Mentor, The Hero" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500 text-white placeholder-gray-500"></input></div>'
)

# I'll write the remaining 19 apps using compact calls
apps_data = [
  ("ai-pre-production","blue","AI Pre-Production Planner","Plan film and TV pre-production workflows",
   "You are an expert film production manager. Create a comprehensive pre-production plan for: Title: {title}, Genre: {genre}, Format: {format}, Budget: {budget}, Location: {location}, Audience: {audience}. Provide: 1) Timeline from greenlight to production start, 2) Key crew positions and hiring order, 3) Script breakdown by department, 4) Casting process timeline, 5) Location scouting checklist, 6) Budget allocation breakdown, 7) Legal/permit requirements, 8) Risk assessment, 9) Day-one readiness checklist.",
   '<div><label className="block text-sm font-medium text-gray-300 mb-1">Project Title</label><input id="title" name="title" placeholder="Your project title" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"></input></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Genre</label><select id="genre" name="genre" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white"><option value="">Select</option><option>Drama</option><option>Thriller</option><option>Comedy</option><option>Horror</option><option>Sci-Fi</option><option>Romance</option><option>Action</option><option>Documentary</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Format</label><select id="format" name="format" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white"><option value="short">Short Film</option><option value="feature">Feature Film</option><option value="tv-pilot">TV Pilot</option><option value="tv-season">TV Season</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Budget Tier</label><select id="budget" name="budget" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white"><option value="micro">Micro (under $50K)</option><option value="low">Low ($50K-$500K)</option><option value="mid">Mid ($500K-$5M)</option><option value="studio">Studio ($5M+)</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Primary Location</label><input id="location" name="location" placeholder="Main shooting location" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"></input></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Target Audience</label><input id="audience" name="audience" placeholder="e.g. Adults 18-34, families" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"></input></div>'),
  ("ai-streaming-analytics","amber","AI Streaming Analytics","Analyze streaming platform performance",
   "You are a streaming analytics expert. Provide performance analysis for: Platform: {platform}, Type: {content_type}, Demographics: {demographics}, Release: {release_date}, Episodes: {episodes}, Genre: {genre}. Include: 1) Viewership/engagement predictions, 2) Release strategy (binge vs weekly), 3) Top 5 KPIs, 4) Competitive positioning, 5) Marketing channels, 6) Subscriber impact, 7) Renewal probability, 8) International expansion recommendations.",
   '<div><label className="block text-sm font-medium text-gray-300 mb-1">Platform</label><select id="platform" name="platform" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white"><option value="">Select</option><option>Netflix</option><option>Amazon Prime</option><option>Disney+</option><option>HBO Max</option><option>Hulu</option><option>Apple TV+</option><option>Peacock</option><option>Paramount+</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Content Type</label><select id="content_type" name="content_type" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white"><option value="">Select</option><option>Original Series</option><option>Original Film</option><option>Licensed Content</option><option>Documentary</option><option>Reality Show</option></select></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Target Demographics</label><input id="demographics" name="demographics" placeholder="e.g. 18-34 males, 25-54 females" className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-amber-500 text-white placeholder-gray-500"></input></div><div><label className="block text-sm font-medium text-gray-300 mb-1">Release Date</label><input id="release_date" name="release_date" type="date" className="w-full bg-gray-