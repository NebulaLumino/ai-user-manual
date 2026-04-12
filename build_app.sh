#!/bin/bash
# Master builder for AI Creative Arts apps
set -e
WORKDIR="/Users/nebulalumino/.openclaw/workspace"
APP="$1"
HSL="$2"
EMOJI="$3"
shift 3
PROMPT="$*"

cd "$WORKDIR"

echo "=== Building $APP ==="

# Check disk
DISK=$(df -h / | tail -1 | awk '{print $4}')
echo "Disk free: $DISK"
if [ "$DISK" = "4Gi" ] || [ "$(echo "$DISK" | sed 's/Gi//' | sed 's/Mi//')" -lt 5000 ] 2>/dev/null; then
  echo "LOW DISK - stopping"
  exit 1
fi

# Remove existing dir if present
rm -rf "$APP"

# 1. Create Next.js app
npx create-next-app@latest "$APP" --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-turbopack --yes 2>&1 | tail -5
echo "create-next-app done"

# Change to app dir - use absolute path to be safe
APP_DIR="$WORKDIR/$APP"
cd "$APP_DIR" || { echo "FAILED to cd into $APP_DIR"; exit 1; }
pwd

# 2. Install openai
npm install openai 2>&1 | tail -1

# 3. Extract HSL
H=$(echo "$HSL" | cut -d, -f1)
S=$(echo "$HSL" | cut -d, -f2)
L=$(echo "$HSL" | cut -d, -f3)
ACCENT="hsl(${H}deg, ${S}%, ${L}%)"
TITLE=$(echo "$APP" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1))substr($i,2); print}')

# 4. Write route.ts
mkdir -p "src/app/api/generate"
cat > "src/app/api/generate/route.ts" << 'ROUTE_EOF'
import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://api.deepseek.com/v1",
});

export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  try {
    const { prompt } = await req.json();
    if (!prompt?.trim()) {
      return NextResponse.json({ error: "Prompt is required" }, { status: 400 });
    }

    const completion = await client.chat.completions.create({
      model: "deepseek-chat",
      messages: [
        { role: "system", content: PROCESSED_PROMPT },
        { role: "user", content: prompt },
      ],
      max_tokens: 800,
      temperature: 0.8,
    });

    const result = completion.choices[0]?.message?.content || "No result generated.";
    return NextResponse.json({ result });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
ROUTE_EOF

echo "route.ts written"

# 5. Write page.tsx  
cat > "src/app/page.tsx" << PAGE_EOF
"use client";

import { useState } from "react";

export default function App() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError("");
    setOutput("");
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });
      const data = await res.json();
      if (!res.ok) setError(data.error || "Something went wrong.");
      else setOutput(data.result || "");
    } catch {
      setError("Failed to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  const accent = "${ACCENT}";

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-2" style={{ color: accent }}>
            ${EMOJI} ${TITLE}
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
            rows={5}
            placeholder="Describe your request..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) handleGenerate();
            }}
          />
          <button
            onClick={handleGenerate}
            disabled={loading || !input.trim()}
            className="mt-4 w-full py-3 px-6 rounded-xl font-semibold text-white transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed hover:brightness-110 active:scale-95"
            style={{ background: accent }}
          >
            {loading ? "Generating..." : "Generate"}
          </button>
        </div>

        {error && (
          <div className="bg-red-900/30 border border-red-800 rounded-xl p-4 mb-6 text-red-300 text-sm">
            {error}
          </div>
        )}

        {output && (
          <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
              Generated Result
            </h2>
            <pre className="whitespace-pre-wrap text-gray-200 font-mono text-sm leading-relaxed">
              {output}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
}
PAGE_EOF

echo "page.tsx written"

# 6. Fix route.ts with actual prompt
sed -i '' "s|PROCESSED_PROMPT|${PROMPT}|g" "src/app/api/generate/route.ts"

# 7. Build
OPENAI_API_KEY=dummy npm run build 2>&1 | tail -8

# 8. Git init & commit
git init
git add -A
git commit -m "feat: initial commit"

# 9. Create GitHub repo and push
gh repo create NebulaLumino/"$APP" --public --source=. --push 2>&1 || {
    git remote set-url origin https://github.com/NebulaLumino/"$APP".git
    git push -u origin main 2>&1
}

# 10. Cleanup
rm -rf node_modules .next

echo "=== $APP done ==="
cd "$WORKDIR"
