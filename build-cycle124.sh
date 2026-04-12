#!/bin/bash
# Build one app: arg1=appname arg2=hsl-color arg3=description arg4=system-prompt-subject
set -e

APPNAME=$1
HSL=$2
DESC=$3
SUBJECT=$4

WORKDIR=/Users/nebulalumino/.openclaw/workspace

echo "===== Building $APPNAME ====="
cd $WORKDIR

# Create Next.js app
npx create-next-app@latest $APPNAME --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-turbopack --yes 2>&1 | tail -3

# Install openai
cd $APPNAME
npm install openai 2>&1 | tail -2

# Write page.tsx
cat > src/app/page.tsx << 'PAGEOF'
"use client";
import { useState } from "react";
export default function Home() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState("");
  const handleGenerate = async () => {
    if (!input.trim()) return;
    setLoading(true); setOutput("");
    try {
      const res = await fetch("/api/generate", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({input}) });
      const data = await res.json();
      setOutput(data.result || "No response.");
    } catch { setOutput("Error."); }
    setLoading(false);
  };
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold" style={{color}}>{icon} {title}</h1>
          <p className="text-gray-400 text-sm">{desc}</p>
        </div>
        <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6 shadow-xl">
          <label className="block text-sm font-medium text-gray-300 mb-2">Your input</label>
          <textarea value={input} onChange={e=>setInput(e.target.value)}
            placeholder={placeholder}
            className="w-full bg-gray-900/80 border border-gray-600 rounded-xl p-4 text-white text-sm placeholder-gray-500 resize-y min-h-[120px] focus:outline-none focus:ring-2" style={{"--tw-ring-color": accentColor+"55"} as React.CSSProperties}/>
          <button onClick={handleGenerate} disabled={loading}
            className="mt-4 w-full py-3 px-6 rounded-xl font-semibold text-white transition-all hover:opacity-90 disabled:opacity-50"
            style={{backgroundColor: accentColor}}>
            {loading ? "Generating..." : "Generate"}
          </button>
        </div>
        {output && (
          <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6 shadow-xl">
            <h2 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">Result</h2>
            <div className="prose prose-invert prose-sm max-w-none text-gray-200 whitespace-pre-wrap">{output}</div>
          </div>
        )}
      </div>
    </main>
  );
}
PAGEOF

# Build
OPENAI_API_KEY=dummy npm run build 2>&1 | tail -4

# Git
git init && git add -A && git commit -m "feat: initial commit"
gh repo create NebulaLumino/$APPNAME --public --source . 2>/dev/null || true
git remote set-url origin https://github.com/NebulaLumino/$APPNAME.git 2>/dev/null || true
git push -u origin main 2>&1 | tail -2

# Cleanup
cd $WORKDIR
rm -rf $APPNAME/node_modules $APPNAME/.next
echo "===== Done: $APPNAME ====="
