#!/usr/bin/env python3
"""Generate all 20 app files from JSON data"""
import os, json

WS = "/Users/nebulalumino/.openclaw/workspace"
with open(f"{WS}/scripts/genapps.json") as f:
    APPS = json.load(f)
with open(f"{WS}/scripts/genprompts.json") as f:
    PROMPTS = json.load(f)
with open(f"{WS}/scripts/genfields.json") as f:
    FIELDS = json.load(f)

G = '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n:root { --background: #0a0a0a; --foreground: #ededed; }\nbody { color: var(--foreground); background: var(--background); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }'

LAYOUT = 'import type { Metadata } from "next";\nimport "./globals.css";\n\nexport const metadata: Metadata = {\n  title: "%s",\n  description: "%s",\n};\n\nexport default function RootLayout({\n  children,\n}: Readonly<{\n  children: React.ReactNode;\n}>) {\n  return (\n    <html lang="en">\n      <body>{children}</body>\n    </html>\n  );\n}\n'

ROUTE_TPL = 'import { NextRequest, NextResponse } from "next/server";\nimport OpenAI from "openai";\n\nconst client = new OpenAI({\n  apiKey: process.env.OPENAI_API_KEY,\n  baseURL: "https://api.deepseek.com/v1",\n});\n\nexport async function POST(req: NextRequest) {\n  try {\n    const body = await req.json();\n    const keys = ["genre","logline","setting","tone","length","archetype","title","format","budget","location","audience","platform","content_type","demographics","release_date","episodes","source_lang","target_lang","age_rating","runtime","voice_style","pages","experience","protagonist_name","antagonist","supporting","world_rules","conflict","resolution","themes","shooting_schedule","characters","timeline","props","costumes","era","terrain","climate","lighting","budget_amount","inconsistency_type","script_content","festival_type","premiere_goal","bts_content_type","distribution","dialogue_sample","reading_level","ep_num","season_count","episode_runtime","pacing_notes","critics_praise","critics_concerns","languages"];\n    let prompt = `%s`;\n    for (const key of keys) {\n      prompt = prompt.replace(new RegExp("{" + key + "}", "g"), String(body[key] || ""));\n    }\n    const completion = await client.chat.completions.create({\n      model: "deepseek-chat",\n      messages: [\n        { role: "system", content: "You are a world-class expert in this domain. Provide detailed, actionable, well-structured output." },\n        { role: "user", content: prompt },\n      ],\n      temperature: 0.7,\n      max_tokens: 2000,\n    });\n    return NextResponse.json({ result: completion.choices[0].message.content });\n  } catch (err: any) {\n    return NextResponse.json({ error: err.message }, { status: 500 });\n  }\n}\n'

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

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def gen_page(app, accent, title, fields):
    g1,g2,ta,fb,bh = ACCENTS[accent]
    fs = fields.replace("FOCUS", fb)
    return (
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
    ) % (g1, g2, title, fs, bh, ta, ta)

for app_info in APPS:
    app, accent, title, desc = app_info
    fields = FIELDS.get(app, '<div><p class="text-gray-400">Form fields coming soon.</p></div>')
    prompt = PROMPTS.get(app, "Provide a helpful response based on the user's input.")
    print(f"Generating {app}...")
    w(f"{WS}/{app}/src/app/globals.css", G)
    w(f"{WS}/{app}/src/app/layout.tsx", LAYOUT % (title, desc))
    w(f"{WS}/{app}/src/app/page.tsx", gen_page(app, accent, title, fields))
    w(f"{WS}/{app}/src/app/api/generate/route.ts", ROUTE_TPL % prompt)
    print(f"  Done: {app}")
