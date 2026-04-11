#!/usr/bin/env python3
import subprocess
import os
import shutil
import sys

WORKDIR = "/Users/nebulalumino/.openclaw/workspace"
TEMPLATE = f"{WORKDIR}/.build-template"

APPS = [
    ("ai-spaced-repetition", "SM-2 Spaced Repetition Scheduler",
     "Create optimized SM-2 spaced repetition schedules for any topic.",
     "Enter a topic or list of concepts to create a spaced repetition schedule...",
     "#5cb578"),
    ("ai-socratic-tutor", "Socratic Tutor Engine",
     "Engage in guided Socratic dialogue for deeper conceptual understanding.",
     "Enter a topic or concept to begin a Socratic dialogue...",
     "#b366d9"),
    ("ai-rubric-generator", "Assessment Rubric Builder",
     "Build detailed, actionable assessment rubrics for academic assignments.",
     "Enter an assignment description to generate an assessment rubric...",
     "#6b8fc9"),
    ("ai-differentiated-instruction", "Differentiated Lesson Planner",
     "Plan tiered lessons for diverse learner needs and readiness levels.",
     "Enter a topic or learning standard to create differentiated lesson plans...",
     "#4dbd8f"),
    ("ai-learning-styles", "VARK Learning Style Assessment",
     "Take a VARK self-assessment and get personalized study strategies.",
     "Enter a subject or topic to create a VARK self-assessment questionnaire...",
     "#a6d14d"),
    ("ai-blooms-taxonomy", "Bloom Taxonomy Lesson Sequencer",
     "Sequence lessons through Bloom's taxonomy cognitive levels.",
     "Enter a topic to scaffold a lesson through Bloom's taxonomy levels...",
     "#d4a63d"),
    ("ai-course-syllabus", "Academic Syllabus Generator",
     "Generate comprehensive, professional academic syllabi.",
     "Enter a course title, subject, and target audience to generate a syllabus...",
     "#d47a3d"),
    ("ai-literature-review", "Literature Review Synthesizer",
     "Synthesize and organize scientific literature reviews.",
     "Enter your research topic or thesis statement to organize a literature review...",
     "#6b5dc9"),
    ("ai-hypothesis-generator", "Research Hypothesis Generator",
     "Generate testable, well-formulated research hypotheses.",
     "Enter a research question or area of interest to generate testable hypotheses...",
     "#d96bb3"),
    ("ai-experimental-design", "Experimental Design Optimizer",
     "Design rigorous experiments with proper controls.",
     "Enter a research question to design a rigorous experiment...",
     "#3dbdb3"),
    ("ai-lab-protocol", "Lab Protocol Optimizer",
     "Optimize laboratory protocols with troubleshooting guides.",
     "Enter an experimental goal or technique to generate an optimized lab protocol...",
     "#d94d4d"),
    ("ai-data-viz-suggester", "Data Visualization Recommender",
     "Get the best data visualizations for your research.",
     "Enter a data description or research question to get visualization recommendations...",
     "#3dbd6b"),
    ("ai-lab-notebook", "Lab Notebook Reviewer",
     "Review lab notebook entries for completeness and compliance.",
     "Enter lab notebook entry details or paste an entry to review...",
     "#3dbd9f"),
    ("ai-lab-safety", "Lab Safety Compliance Auditor",
     "Perform comprehensive lab safety compliance audits.",
     "Enter lab type or materials to perform a comprehensive safety audit...",
     "#d94d6b"),
    ("ai-student-report", "Student Progress Report Writer",
     "Write formative, detailed student progress reports.",
     "Enter student name, grade level, and subject area to generate a progress report...",
     "#6b8fa6"),
    ("ai-thesis-planner", "Thesis/Dissertation Timeline Planner",
     "Plan your thesis or dissertation with structured timelines.",
     "Enter thesis topic and defense deadline to create a structured timeline...",
     "#a64dd9"),
    ("ai-grant-budget", "Research Grant Budget Builder",
     "Build detailed, compliant research grant budgets.",
     "Enter grant type, project scope, and funding amount to build a budget...",
     "#4d7a8f"),
    ("ai-peer-review", "Peer Review Feedback Generator",
     "Generate constructive peer review feedback.",
     "Paste a manuscript abstract or section to generate peer review feedback...",
     "#d94d9f"),
    ("ai-knowledge-graph", "Research Knowledge Graph Constructor",
     "Construct conceptual knowledge graphs from research.",
     "Enter a research topic or list of papers to construct a knowledge graph...",
     "#d94d4d"),
    ("ai-citation-formatter", "Multi-Format Citation Manager",
     "Format citations in APA, MLA, Chicago, IEEE, Harvard, Vancouver.",
     "Enter references or citation lists to format in APA, MLA, Chicago, IEEE and more...",
     "#9f4dd9"),
]

def run(cmd, cwd=None, capture=True, timeout=300):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=capture, text=True, timeout=timeout)
    if result.returncode != 0:
        print(f"  [ERROR] returncode={result.returncode}")
        if result.stdout: print(result.stdout[-500:])
        if result.stderr: print(result.stderr[-500:])
        raise SystemExit(result.returncode)
    if capture and result.stdout:
        print(result.stdout[-500:])
    return result

def build_app(app_name, app_title, app_desc, placeholder, accent_hex):
    app_dir = f"{WORKDIR}/{app_name}"
    if os.path.exists(app_dir):
        shutil.rmtree(app_dir)
    
    print(f"\n==== Building {app_name} ({accent_hex}) ====")
    
    # Create Next.js app
    r = run(
        f"npx create-next-app@latest {app_name} --typescript --tailwind --eslint --app --src-dir --import-alias \"@/*\" --no-turbopack --yes",
        cwd=WORKDIR, timeout=180
    )
    print(r.stdout.split('\n')[-6:] if r.stdout else "")
    
    # Read template
    with open(f"{TEMPLATE}/app/page.tsx") as f:
        page = f.read()
    with open(f"{TEMPLATE}/api/generate/route.ts") as f:
        route = f.read()
    
    # Substitute placeholders
    page = page.replace("APP_TITLE_PLACEHOLDER", app_title)
    page = page.replace("APP_DESC_PLACEHOLDER", app_desc)
    page = page.replace("APP_PH_PLACEHOLDER", placeholder)
    page = page.replace("APP_HEX_PLACEHOLDER", accent_hex)
    page = page.replace("APP_CSS_VAR", accent_hex.lstrip('#'))
    
    # Write app files
    os.makedirs(f"{app_dir}/src/app/api/generate", exist_ok=True)
    with open(f"{app_dir}/src/app/page.tsx", "w") as f:
        f.write(page)
    with open(f"{app_dir}/src/app/api/generate/route.ts", "w") as f:
        f.write(route)
    
    # Install openai dependency
    print("  Installing openai...")
    run("npm install openai", cwd=app_dir)
    
    # Build
    print("  Building...")
    r = run("npm run build", cwd=app_dir, timeout=180)
    
    # Git init, create repo, and push
    print("  Git init + push...")
    run("git init", cwd=app_dir)
    run("git add -A && git commit -m 'feat: initial commit'", cwd=app_dir)
    # Create repo first, then push
    r = subprocess.run(f"gh repo create NebulaLumino/{app_name} --public 2>&1", shell=True, cwd=app_dir, capture_output=True, text=True)
    print("  gh repo create:", r.stdout.strip() or r.stderr.strip())
    run(f"git remote add origin https://github.com/NebulaLumino/{app_name}.git", cwd=app_dir)
    r2 = subprocess.run("git push -u origin main 2>&1", shell=True, cwd=app_dir, capture_output=True, text=True, timeout=60)
    print("  git push:", r2.stdout.strip() or r2.stderr.strip())
    
    # Cleanup
    run(f"rm -rf {app_dir}/node_modules {app_dir}/.next")
    print(f"  === Done {app_name} ===")

for app in APPS:
    build_app(*app)

print("\n\n✅ ALL APPS BUILT")
