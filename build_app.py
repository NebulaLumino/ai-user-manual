#!/usr/bin/env python3
import sys, os, re

APP_NAME = sys.argv[1]
HSL = sys.argv[2]
PROMPT = sys.argv[3]

h, s, l = HSL.split(',')
accent = f"hsl({h}deg, {s}%, {l}%)"
title_words = APP_NAME.replace('-', ' ').replace('/', ' ').title()

route = f'''import {{ NextRequest, NextResponse }} from "next/server";
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
'''

page = f'''"use client";

import {{ useState }} from "react";

export default function App() {{
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {{
    if (!input.trim()) return;
    setLoading(true);
    setError("");
    setOutput("");
    try {{
      const res = await fetch("/api/generate", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ prompt: input }}),
      }});
      const data = await res.json();
      if (!res.ok) setError(data.error || "Something went wrong.");
      else setOutput(data.result || "");
    }} catch {{
      setError("Failed to connect to the server.");
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-2" style={{ color: "{accent}" }}>
            ✨ {title_words}
          </h1>
          <p className="text-gray-400 text-sm">
            Describe what you need and let AI generate it for you.
          </p>
        </div>

        <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-6 mb-6">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Your request
          </label>
          <textarea
            className="w-full bg-gray-800/60 border border-gray-700 rounded-xl p-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 resize-none"
            style={{}}
            rows={{5}}
            placeholder="Describe your request..."
            value={{input}}
            onChange={{(e) => setInput(e.target.value)}}
            onKeyDown={{(e) => {{
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) handleGenerate();
            }}}}
          />
          <button
            onClick={{handleGenerate}}
            disabled={{loading || !input.trim()}}
            className="mt-4 w-full py-3 px-6 rounded-xl font-semibold text-white transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed hover:brightness-110 active:scale-95"
            style={{ background: "{accent}" }}
          >
            {{loading ? "Generating..." : "Generate"}}
          </button>
        </div>

        {{error && (
          <div className="bg-red-900/30 border border-red-800 rounded-xl p-4 mb-6 text-red-300 text-sm">
            {{error}}
          </div>
        )}}

        {{output && (
          <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
              Generated Result
            </h2>
            <pre className="whitespace-pre-wrap text-gray-200 font-mono text-sm leading-relaxed">
              {{output}}
            </pre>
          </div>
        )}}
      </div>
    </main>
  );
}}
'''

os.makedirs(f"{APP_NAME}/src/app/api/generate", exist_ok=True)
with open(f"{APP_NAME}/src/app/api/generate/route.ts", "w") as f:
    f.write(route)
with open(f"{APP_NAME}/src/app/page.tsx", "w") as f:
    f.write(page)

print(f"Written: {APP_NAME}")
