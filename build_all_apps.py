#!/usr/bin/env python3
"""Build all 30 culinary AI apps from template."""
import os, shutil, subprocess, sys

WORKDIR = "/Users/nebulalumino/.openclaw/workspace"
TEMPLATE = WORKDIR + "/app-template"

APPS = [
    ("ai-ingredient-swap",  "hsl(145deg,60%,50%)",  "145deg,60%,50%",  "🔄", "AI Ingredient Swap",     "Recipe allergen/diet modifier",  "Replace eggs in brownies for vegan, or swap wheat flour for gluten-free in pancakes",                                         "You are a professional culinary AI specializing in ingredient substitutions for allergen-free, diet-specific, and flavor-optimized cooking. For the given ingredient or recipe, provide smart substitutions covering allergens, dietary preferences, and flavor matching with clear ratios."),
    ("ai-wine-pairing",     "hsl(270deg,65%,55%)",  "270deg,65%,55%",  "🍷", "AI Wine Pairing",         "Wine & food pairing advisor",     "Wine pairing for grilled ribeye with roasted vegetables, or Thai curry dinner party",                                "You are a sommelier AI assistant. Recommend wines, explain flavor interactions, suggest alternatives, and explain why each pairing works. Include region and vintage suggestions."),
    ("ai-meal-prep",        "hsl(0deg,65%,50%)",    "0deg,65%,50%",    "🥗", "AI Meal Prep",            "Macro-based meal prep planner",    "5-day meal prep for 200g protein, 150g carbs, 60g fat per day. No pork, dairy-free",                               "You are a nutrition and meal prep planning AI. Create weekly meal plans with exact macros, portion sizes, prep instructions, storage tips, and shopping lists."),
    ("ai-knife-skills",     "hsl(25deg,70%,55%)",   "25deg,70%,55%",   "🔪", "AI Knife Skills",         "Knife skills & technique guide",   "How to julienne carrots, brunoise onions, and chiffonade basil with proper technique and safety tips",                               "You are a culinary knife skills instructor. Provide step-by-step technique guides, safety tips, knife types for each cut, and common mistakes to avoid."),
    ("ai-sous-vide",        "hsl(220deg,60%,55%)",  "220deg,60%,55%",  "🌡️", "AI Sous Vide",            "Sous vide parameter calculator",   "Sous vide parameters for a 2-inch ribeye, medium-rare, 1-3 hour window with finishing sear notes",                   "You are a sous vide precision cooking expert. Provide exact temperature, time range, finishing method, and food safety notes for proteins and vegetables."),
    ("ai-fermentation",     "hsl(85deg,65%,50%)",   "85deg,65%,50%",   "🦠", "AI Fermentation",        "Fermentation starter guide",       "How to start vegetable fermentation with cabbage and carrots, 2% salt brine, troubleshooting guide",                       "You are a fermentation specialist. Guide vegetable lacto-fermentation, SCOBY creation, kombucha, and koji. Include ratios, timelines, troubleshooting, and safety notes."),
    ("ai-baking-ratio",     "hsl(175deg,55%,45%)",  "175deg,55%,45%",  "🥐", "AI Baking Ratio",        "Bakers percentage calculator",     "Bakers percentages for sourdough with 70% hydration, 20% levain, 2% salt. Convert to 800g total dough",                    "You are a professional baker. Calculate bakers percentages, convert to gram weights for specified batch sizes, and explain the role of each ingredient."),
    ("ai-food-cost",        "hsl(305deg,60%,60%)",  "305deg,60%,60%",  "💰", "AI Food Cost",           "Food cost & menu pricing",         "Food cost for chicken piccata for 4 people, 35% food cost target, and menu price suggestion",                                       "You are a restaurant cost analyst. Calculate food cost per plate, ideal menu price, food cost percentage, and suggest portion sizes to hit target margins."),
    ("ai-flavor-wheel",     "hsl(265deg,55%,50%)",  "265deg,55%,50%",  "🎡", "AI Flavor Wheel",         "Flavor profile visualizer",        "Analyze the flavor profile of miso paste and show complete flavor wheel breakdown with intensity levels",                                   "You are a flavor chemistry expert. Analyze ingredients using the six basic tastes, aroma compounds, mouthfeel, and flavor dynamics using the flavor wheel framework."),
    ("ai-sauce-recipes",    "hsl(200deg,45%,45%)",  "200deg,45%,45%",  "🫕", "AI Sauce Recipes",        "Sauce & condiment vault",           "Classic bechamel sauce recipe, or quick pan sauce for steak, or aioli from scratch",                                    "You are a sauce specialist. Provide detailed recipes for mother sauces and derivatives, with techniques, troubleshooting, and variations."),
    ("ai-seasonal-menu",     "hsl(0deg,60%,50%)",    "0deg,60%,50%",    "🌿", "AI Seasonal Menu",        "Farm-to-table seasonal menu",       "Create a 4-course spring dinner menu using in-season Pacific Northwest ingredients",                                    "You are a farm-to-table chef. Create seasonal menus using local, in-season ingredients with wine pairings and plating notes."),
    ("ai-coffee-brewing",   "hsl(45deg,75%,55%)",   "45deg,75%,55%",   "☕", "AI Coffee Brewing",        "Coffee extraction guide",            "Optimal pour-over parameters for light roast Ethiopian beans: grind size, water temp, bloom time, ratio",                                "You are a specialty coffee expert. Calculate extraction parameters for pour-over, French press, espresso, AeroPress, and cold brew with precise ratios."),
    ("ai-kitchen-gear",     "hsl(340deg,55%,55%)",  "340deg,55%,55%",  "🍳", "AI Kitchen Gear",         "Kitchen equipment advisor",         "Best knife set for a home cook on a budget, or stand mixer for bread baking under 500 dollars",                             "You are a kitchen equipment consultant. Recommend tools, knives, appliances, and gear with specific models, price ranges, and alternatives."),
    ("ai-spice-blend",      "hsl(125deg,55%,45%)",  "125deg,55%,45%",  "🌿", "AI Spice Blend",           "Custom spice blend composer",       "Create a custom garam masala for mild curry, or jerk seasoning for chicken with warming spices",                    "You are a spice blending expert. Compose custom spice blends with exact ratios, toasting instructions, and flavor notes. Provide storage tips."),
    ("ai-brine-cure",       "hsl(185deg,60%,55%)",  "185deg,60%,55%",  "🧂", "AI Brine & Cure",          "Brine & cure calculator",           "Wet brine for a 5lb turkey, or dry cure for prosciutto-style ham over 14 days",                                         "You are a charcuterie expert. Calculate wet and dry brines, curing salts, smoking schedules, and safe curing times for various cuts."),
    ("ai-vegan-protein",   "hsl(235deg,55%,55%)",  "235deg,55%,55%",  "🌱", "AI Vegan Protein",         "Vegan protein analyzer",             "Complete protein combinations for a vegan athlete needing 120g protein per day from plant sources",                                        "You are a vegan nutrition specialist. Analyze plant-based proteins, complete amino acid profiles, and create high-protein meal plans without animal products."),
    ("ai-food-storage",     "hsl(165deg,55%,45%)",  "165deg,55%,45%",  "🧊", "AI Food Storage",          "Food storage optimizer",            "How to store fresh herbs, or best methods for freezing cooked grains and beans without losing quality",                                         "You are a food preservation expert. Provide optimal storage for pantry, fridge, and freezer. Include shelf life, signs of spoilage, and best practices."),
    ("ai-sourdough",        "hsl(215deg,45%,55%)",  "215deg,45%,55%",  "🍞", "AI Sourdough",             "Sourdough starter monitor",         "My sourdough starter is 5 days old and not rising. How do I feed and maintain it for consistent baking",                                          "You are a sourdough expert. Guide starter creation, feeding schedules, bulk fermentation, proofing, scoring, and baking. Include hydration and temperature adjustments."),
    ("ai-cuisine-deep",     "hsl(0deg,65%,50%)",    "0deg,65%,50%",    "🌏", "AI Cuisine Deep Dive",     "Cultural cuisine deep dive",        "History and key techniques of Sichuan cuisine, or essential elements of Japanese kaiseki",                             "You are a culinary cultural historian. Provide deep dives into world cuisines: history, techniques, iconic ingredients, regional variations, and cultural context."),
    ("ai-molecular",        "hsl(270deg,65%,55%)",  "270deg,65%,55%",  "🧪", "AI Molecular Gastronomy",  "Molecular gastronomy translator",   "How to make agar caviar, or reverse spherification of watermelon juice with sodium alginate",                           "You are a molecular gastronomy chef. Explain techniques like spherification, emulsification, transglutaminase, and sous vide gels with precise formulas."),
    ("ai-bbq-calculator",   "hsl(85deg,65%,50%)",   "85deg,65%,50%",   "🔥", "AI BBQ Calculator",         "BBQ temperature controller",       "Smoking schedule for a 12lb pork shoulder at 225 degrees F with unwrapped and wrapped phases",                                  "You are a BBQ pitmaster. Calculate smoking temperatures, times, unwrapped vs wrapped phases, and finishing sears for brisket, pork, and ribs."),
    ("ai-food-photo",       "hsl(25deg,70%,55%)",   "25deg,70%,55%",   "📸", "AI Food Photography",       "Food photography recipe card",      "Create a beautiful recipe card for mushroom risotto with plating notes for food photography",                             "You are a food stylist and photographer. Create recipe cards with beautiful formatting, plating notes, prop suggestions, and lighting tips."),
    ("ai-kombucha",         "hsl(220deg,60%,55%)",  "220deg,60%,55%",  "🍵", "AI Kombucha",              "Kombucha brewing helper",           "First ferment timeline for 1-gallon batch, SCOBY health check, second ferment flavoring options",                              "You are a kombucha brewing specialist. Guide SCOBY maintenance, first and second ferment timelines, flavoring, carbonation, and troubleshooting."),
    ("ai-nutrition-label",  "hsl(175deg,55%,45%)",  "175deg,55%,45%",  "🏷️", "AI Nutrition Label",        "Food label decoder",                "Decode this nutrition label and explain what each value means for my dietary goals and macros",                                     "You are a nutrition facts analyst. Decode food labels, explain percent Daily Value, hidden sugars, fiber, micronutrients, and how they fit into dietary goals."),
    ("ai-bread-ferment",    "hsl(305deg,60%,60%)",  "305deg,60%,60%",  "🌾", "AI Bread Ferment",          "Bread fermentation planner",       "Plan a cold-retard schedule for a country loaf over 3 days with preferment options like poolish",                        "You are a bread fermentation expert. Plan bulk ferment, proofing, cold retard, and preferment schedules based on flour, levain strength, and target bake."),
    ("ai-shu-compare",      "hsl(265deg,55%,50%)",  "265deg,55%,50%",  "🌶️", "AI Spice Heat Compare",    "Spice heat level comparator",       "Compare ghost pepper vs Carolina reaper vs habanero: SHU ratings, flavor notes, best culinary uses",                             "You are a chili and spice expert. Compare heat levels on the Scoville scale, flavor profiles, culinary uses, and growing tips for chilies and spices."),
    ("ai-pantry-list",      "hsl(200deg,45%,45%)",  "200deg,45%,45%",  "🗃️", "AI Pantry List",             "Pantry essentials optimizer",        "Stock a well-equipped Mediterranean pantry with oils, grains, dried goods, specialty items",                         "You are a pantry planning expert. Create organized pantry lists by cuisine and purpose, from essentials to specialty items, with quality brand suggestions."),
    ("ai-dumpling-calc",     "hsl(0deg,60%,50%)",    "0deg,60%,50%",    "🥟", "AI Dumpling Calculator",    "Dumpling & filling calculator",     "Calculate filling for 50 dumplings, or best pork-to-cabbage ratio for Shanghai-style soup dumplings",                   "You are a dumpling master. Calculate portions, meat-to-vegetable ratios, dough hydration, and provide filling recipes for gyoza, bao, soup dumplings, and more."),
    ("ai-slow-cooker",      "hsl(45deg,75%,55%)",   "45deg,75%,55%",   "🍲", "AI Slow Cooker",            "Slow cooker dump meal planner",     "8-hour slow cooker beef stew for 4 people with optimal liquid levels and vegetable timing",                              "You are a slow cooker specialist. Create dump-and-go meals optimized for 6-10 hour slow cooker timing with proper texture and layered flavors."),
    ("ai-menu-writing",     "hsl(340deg,55%,55%)",  "340deg,55%,55%",  "📋", "AI Menu Writing",           "Restaurant menu writer",            "Write a 5-item prix fixe menu for an Italian restaurant with elegant, appetizing descriptions",                         "You are a restaurant menu copywriter. Write compelling, appetizing menu descriptions using sensory language, suggesting quality, and driving sales."),
]

def run_cmd(cmd, cwd=None, env=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, env=env,
                           capture_output=True, text=True)
    return result

# Remove existing apps
for name, _, _, _, _, _, _, _ in APPS:
    app_dir = WORKDIR + "/" + name
    if os.path.exists(app_dir):
        shutil.rmtree(app_dir)

for i, (name, accent, hsl_color, icon, title, desc, placeholder, system) in enumerate(APPS):
    print(f"\n[{i+1}/30] === {name} ===")
    app_dir = WORKDIR + "/" + name

    # Copy template
    shutil.copytree(TEMPLATE, app_dir)
    os.makedirs(app_dir + "/src/app/api/generate", exist_ok=True)
    print("  Template copied")

    # Write page.tsx
    page_code = (
        '"use client";\n'
        'import { useState } from "react";\n'
        'export default function Home() {\n'
        '  const [input, setInput] = useState("");\n'
        '  const [loading, setLoading] = useState(false);\n'
        '  const [output, setOutput] = useState("");\n'
        '  const handleGenerate = async () => {\n'
        '    if (!input.trim()) return;\n'
        '    setLoading(true); setOutput("");\n'
        '    try {\n'
        '      const res = await fetch("/api/generate", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({input}) });\n'
        '      const data = await res.json();\n'
        '      setOutput(data.result || "No response.");\n'
        '    } catch { setOutput("Error generating response."); }\n'
        '    setLoading(false);\n'
        '  };\n'
        '  return (\n'
        '    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-gray-900 text-white flex flex-col items-center justify-center p-6">\n'
        '      <div className="w-full max-w-2xl space-y-6">\n'
        '        <div className="text-center space-y-2">\n'
        '          <h1 className="text-3xl font-bold" style={{color:"' + accent + '"}}>' + icon + ' ' + title + '</h1>\n'
        '          <p className="text-gray-400 text-sm">' + desc + '</p>\n'
        '        </div>\n'
        '        <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6 shadow-xl">\n'
        '          <label className="block text-sm font-medium text-gray-300 mb-2">Your input</label>\n'
        '          <textarea value={input} onChange={e=>setInput(e.target.value)}\n'
        '            placeholder="' + placeholder + '..."\n'
        '            className="w-full bg-gray-900/80 border border-gray-600 rounded-xl p-4 text-white text-sm placeholder-gray-500 resize-y min-h-[120px] focus:outline-none focus:ring-2 focus:ring-white/20"/>\n'
        '          <button onClick={handleGenerate} disabled={loading}\n'
        '            className="mt-4 w-full py-3 px-6 rounded-xl font-semibold text-white transition-all hover:opacity-90 disabled:opacity-50"\n'
        '            style={{backgroundColor:"' + accent + '"}}>\n'
        '            {loading ? "Generating..." : "Generate"}\n'
        '          </button>\n'
        '        </div>\n'
        '        {output && (\n'
        '          <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6 shadow-xl">\n'
        '            <h2 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">Result</h2>\n'
        '            <div className="prose prose-invert prose-sm max-w-none text-gray-200 whitespace-pre-wrap">{output}</div>\n'
        '          </div>\n'
        '        )}\n'
        '      </div>\n'
        '    </main>\n'
        '  );\n'
        '}\n'
    )
    with open(app_dir + "/src/app/page.tsx", "w") as f:
        f.write(page_code)

    # Write route.ts
    route_code = (
        'import OpenAI from "openai";\n'
        'export async function POST(req: Request) {\n'
        '  const { input } = await req.json();\n'
        '  if (!input) return new Response("No input", { status: 400 });\n'
        '  const openai = new OpenAI({\n'
        '    apiKey: process.env.OPENAI_API_KEY,\n'
        '    baseURL: "https://api.deepseek.com/v1",\n'
        '  });\n'
        '  const completion = await openai.chat.completions.create({\n'
        '    model: "deepseek-chat",\n'
        '    messages: [\n'
        '      { role: "system", content: "' + system.replace('"', '\\"') + '" },\n'
        '      { role: "user", content: input },\n'
        '    ],\n'
        '    temperature: 0.8,\n'
        '    max_tokens: 800,\n'
        '  });\n'
        '  return Response.json({ result: completion.choices[0].message.content });\n'
        '}\n'
    )
    with open(app_dir + "/src/app/api/generate/route.ts", "w") as f:
        f.write(route_code)

    print("  Files written")

    # Build
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = "dummy"
    result = run_cmd("npm run build 2>&1 | tail -8", cwd=app_dir, env=env)
    if result.returncode != 0:
        print(f"  BUILD FAILED:\n{result.stdout[-1000:]}")
        # Try to continue
        continue
    print("  Build OK")

    # Git init & commit
    run_cmd("git init", cwd=app_dir)
    run_cmd("git add -A && git commit -m 'feat: initial commit'", cwd=app_dir)
    print("  Git committed")

    # Create GH repo (ignore if already exists)
    run_cmd("gh repo create NebulaLumino/" + name + " --public --source . 2>/dev/null || true", cwd=app_dir)
    run_cmd("git remote set-url origin https://github.com/NebulaLumino/" + name + ".git 2>/dev/null || true", cwd=app_dir)
    push = run_cmd("git push -u origin main 2>&1", cwd=app_dir)
    if push.returncode == 0:
        print("  Pushed to GitHub")
    else:
        print("  Push result: " + push.stdout[-200:])

    # Cleanup
    shutil.rmtree(app_dir + "/node_modules")
    shutil.rmtree(app_dir + "/.next")
    print("  Cleaned up")

    # Check disk
    disk = run_cmd("df -h / | tail -1 | awk '{print $4}'")
    print("  Disk free: " + disk.stdout.strip())

print("\nAll 30 apps done!")
