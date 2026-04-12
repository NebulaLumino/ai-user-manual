#!/usr/bin/env python3
"""Build one AI Creative Arts app."""
import sys, os, subprocess, shutil

WORKDIR = "/Users/nebulalumino/.openclaw/workspace"
APP = sys.argv[1]
HSL = sys.argv[2]    # "145,60,50"
EMOJI = sys.argv[3]
PROMPT = sys.argv[4]

h, s, l = HSL.split(',')
accent = f"hsl({h}deg, {s}%, {l}%)"
title = ' '.join(w.capitalize() for w in APP.replace('-', ' ').split())

print(f"Building {APP}...")

# Check disk
result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
print(result.stdout.split('\n')[-1])

# Clean up any existing
if os.path.exists(APP):
    shutil.rmtree(APP)
    print(f"Removed existing {APP}")

# Create Next.js app
print("Creating Next.js app...")
r = subprocess.run(
    ['npx', 'create-next-app@latest', APP,
     '--typescript', '--tailwind', '--eslint', '--app', '--src-dir',
     '--import-alias', '@/\\*', '--no-turbopack', '--yes'],
    cwd=WORKDIR, capture_output=True, text=True, timeout=300
)
print(r.stdout[-500:] if r.stdout else "")
if r.returncode != 0:
    print("STDERR:", r.stderr[-300:])

# Install openai
r = subprocess.run(['npm', 'install', 'openai'], cwd=f"{WORKDIR}/{APP}",
                   capture_output=True, text=True, timeout=60)
print(r.stdout.split('\n')[-2] if r.stdout else "install done")

# Write route.ts
os.makedirs(f"{WORKDIR}/{APP}/src/app/api/generate", exist_ok=True)
with open(f"{WORKDIR}/{APP}/src/app/api/generate/route.ts", "w") as f:
    f.write(
f'''import {{ NextRequest, NextResponse }} from "next/server";
import OpenAI from "openai";

const client = new OpenAI({{
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://api.deepseek.com/v1",
}});

export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {{
  try {{
    const {{ prompt }} = await req.json();
    if (!prompt?.trim()) {{
      return NextResponse.json({{ error: "Prompt is required" }}, {{ status: 400 }});
    }}

    const completion = await client.chat.completions.create({{
      model: "deepseek-chat",
      messages: [
        {{ role: "system", content: `{PROMPT}` }},
        {{ role: "user", content: prompt }},
      ],
      max_tokens: 800,
      temperature: 0.8,
    }});

    const result = completion.choices[0]?.message?.content || "No result generated.";
    return NextResponse.json({{ result }});
  }} catch (error: unknown) {{
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({{ error: message }}, {{ status: 500 }});
  }}
}}
''')
print("route.ts written")

# Write page.tsx - use double-brace escaping for JSX expressions in f-string
# In f-strings: {{x}} becomes literal {x} in output
page_content = (
    '"use client";\n\n'
    'import { useState } from "react";\n\n'
    'export default function App() {\n'
    '  const [input, setInput] = useState("");\n'
    '  const [output, setOutput] = useState("");\n'
    '  const [loading, setLoading] = useState(false);\n'
    '  const [error, setError] = useState("");\n\n'
    '  const handleGenerate = async () => {\n'
    '    if (!input.trim()) return;\n'
    '    setLoading(true);\n'
    '    setError("");\n'
    '    setOutput("");\n'
    '    try {\n'
    '      const res = await fetch("/api/generate", {\n'
    '        method: "POST",\n'
    '        headers: { "Content-Type": "application/json" },\n'
    '        body: JSON.stringify({ prompt: input }),\n'
    '      });\n'
    '      const data = await res.json();\n'
    '      if (!res.ok) setError(data.error || "Something went wrong.");\n'
    '      else setOutput(data.result || "");\n'
    '    } catch {\n'
    '      setError("Failed to connect to the server.");\n'
    '    } finally {\n'
    '      setLoading(false);\n'
    '    }\n'
    '  };\n\n'
    f'  const accent = "{accent}";\n\n'
    '  return (\n'
    '    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col items-center justify-center p-6">\n'
    '      <div className="w-full max-w-2xl">\n'
    '        <div className="text-center mb-10">\n'
    f'          <h1 className="text-4xl font-bold mb-2" style={{{{color: accent}}}}>\n'
    f'            {EMOJI} {title}\n'
    '          </h1>\n'
    '          <p className="text-gray-400 text-sm">\n'
    '            Describe what you need and let AI generate it for you.\n'
    '          </p>\n'
    '        </div>\n\n'
    '        <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-6 mb-6">\n'
    '          <label className="block text-sm font-medium text-gray-300 mb-2">\n'
    '            Your request\n'
    '          </label>\n'
    '          <textarea\n'
    '            className="w-full bg-gray-800/60 border border-gray-700 rounded-xl p-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 resize-none"\n'
    '            rows={5}\n'
    '            placeholder="Describe your request..."\n'
    '            value={input}\n'
    '            onChange={(e) => setInput(e.target.value)}\n'
    '            onKeyDown={(e) => {\n'
    '              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) handleGenerate();\n'
    '            }}\n'
    '          />\n'
    '          <button\n'
    '            onClick={handleGenerate}\n'
    '            disabled={loading || !input.trim()}\n'
    '            className="mt-4 w-full py-3 px-6 rounded-xl font-semibold text-white transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed hover:brightness-110 active:scale-95"\n'
    f'            style={{{{background: accent}}}}\n'
    '          >\n'
    '            {loading ? "Generating..." : "Generate"}\n'
    '          </button>\n'
    '        </div>\n\n'
    '        {error && (\n'
    '          <div className="bg-red-900/30 border border-red-800 rounded-xl p-4 mb-6 text-red-300 text-sm">\n'
    '            {error}\n'
    '          </div>\n'
    '        )}\n\n'
    '        {output && (\n'
    '          <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6">\n'
    '            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">\n'
    '              Generated Result\n'
    '            </h2>\n'
    '            <pre className="whitespace-pre-wrap text-gray-200 font-mono text-sm leading-relaxed">\n'
    '              {output}\n'
    '            </pre>\n'
    '          </div>\n'
    '        )}\n'
    '      </div>\n'
    '    </main>\n'
    '  );\n'
    '}\n'
)

with open(f"{WORKDIR}/{APP}/src/app/page.tsx", "w") as f:
    f.write(page_content)
print("page.tsx written")

# Build
env = os.environ.copy()
env['OPENAI_API_KEY'] = 'dummy'
r = subprocess.run(['npm', 'run', 'build'], cwd=f"{WORKDIR}/{APP}",
                   capture_output=True, text=True, timeout=300, env=env)
lines = (r.stdout + r.stderr).split('\n')
print('\n'.join(lines[-15:]))
if r.returncode != 0:
    print("BUILD FAILED")
    sys.exit(1)

# Git init & commit
subprocess.run(['git', 'init'], cwd=f"{WORKDIR}/{APP}", capture_output=True)
subprocess.run(['git', 'add', '-A'], cwd=f"{WORKDIR}/{APP}", capture_output=True)
subprocess.run(['git', 'commit', '-m', 'feat: initial commit'],
               cwd=f"{WORKDIR}/{APP}", capture_output=True)

# GitHub repo & push
r = subprocess.run(
    ['gh', 'repo', 'create', f'NebulaLumino/{APP}', '--public', '--source=.', '--push'],
    cwd=f"{WORKDIR}/{APP}", capture_output=True, text=True
)
print(r.stdout[-300:] if r.stdout else "")
if 'X Unable to add remote' in r.stdout or r.returncode != 0:
    subprocess.run(
        ['git', 'remote', 'set-url', 'origin',
         f'https://github.com/NebulaLumino/{APP}.git'],
        cwd=f"{WORKDIR}/{APP}", capture_output=True
    )
    r2 = subprocess.run(['git', 'push', '-u', 'origin', 'main'],
                        cwd=f"{WORKDIR}/{APP}", capture_output=True, text=True)
    print(r2.stdout[-200:] if r2.stdout else "")

# Cleanup
shutil.rmtree(f"{WORKDIR}/{APP}/node_modules")
shutil.rmtree(f"{WORKDIR}/{APP}/.next")
print(f"=== {APP} done ===")
