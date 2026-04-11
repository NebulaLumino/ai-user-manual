#!/bin/bash
set -e

WORKDIR="/Users/nebulalumino/.openclaw/workspace"
TEMPLATE="$WORKDIR/.build-template"

APPS='
ai-spaced-repetition|SM-2 Spaced Repetition Scheduler|Enter a topic or list of concepts to create a spaced repetition schedule...|hsl(145,55%,45%)|#5cb578
ai-socratic-tutor|Socratic Tutor Engine|Enter a topic or concept to begin a Socratic dialogue...|hsl(270,65%,55%)|#b366d9
ai-rubric-generator|Assessment Rubric Builder|Enter an assignment description to generate an assessment rubric...|hsl(220,60%,55%)|#6b8fc9
ai-differentiated-instruction|Differentiated Lesson Planner|Enter a topic or learning standard to create differentiated lesson plans...|hsl(175,55%,45%)|#4dbd8f
ai-learning-styles|VARK Learning Style Assessment|Enter a topic to create a VARK self-assessment questionnaire...|hsl(85,65%,50%)|#a6d14d
ai-blooms-taxonomy|Bloom Taxonomy Lesson Sequencer|Enter a topic to scaffold a lesson through Bloom\'s taxonomy levels...|hsl(45,70%,55%)|#d4a63d
ai-course-syllabus|Academic Syllabus Generator|Enter a course title, subject, and target audience to generate a syllabus...|hsl(25,70%,55%)|#d47a3d
ai-literature-review|Literature Review Synthesizer|Enter your research topic or thesis statement to organize a literature review...|hsl(235,55%,55%)|#6b5dc9
ai-hypothesis-generator|Research Hypothesis Generator|Enter a research question or area of interest to generate testable hypotheses...|hsl(305,60%,60%)|#d96bb3
ai-experimental-design|Experimental Design Optimizer|Enter a research question to design a rigorous experiment...|hsl(185,60%,55%)|#3dbdb3
ai-lab-protocol|Lab Protocol Optimizer|Enter an experimental goal or technique to generate an optimized lab protocol...|hsl(0,65%,50%)|#d94d4d
ai-data-viz-suggester|Data Visualization Recommender|Enter a data description or research question to get visualization recommendations...|hsl(125,55%,45%)|#3dbd6b
ai-lab-notebook|Lab Notebook Reviewer|Enter lab notebook entry details or paste an entry to review...|hsl(165,55%,45%)|#3dbd9f
ai-lab-safety|Lab Safety Compliance Auditor|Enter lab type or materials to perform a comprehensive safety audit...|hsl(340,55%,55%)|#d94d6b
ai-student-report|Student Progress Report Writer|Enter student name, grade level, and subject area to generate a progress report...|hsl(215,45%,55%)|#6b8fa6
ai-thesis-planner|Thesis/Dissertation Timeline Planner|Enter thesis topic and defense deadline to create a structured timeline...|hsl(265,55%,50%)|#a64dd9
ai-grant-budget|Research Grant Budget Builder|Enter grant type, project scope, and funding amount to build a budget...|hsl(200,45%,45%)|#4d7a8f
ai-peer-review|Peer Review Feedback Generator|Paste a manuscript abstract or section to generate peer review feedback...|hsl(335,55%,55%)|#d94d9f
ai-knowledge-graph|Research Knowledge Graph Constructor|Enter a research topic or list of papers to construct a knowledge graph...|hsl(0,60%,50%)|#d94d4d
ai-citation-formatter|Multi-Format Citation Manager|Enter references or citation lists to format in APA, MLA, Chicago, IEEE and more...|hsl(255,55%,55%)|#9f4dd9
'

cd "$WORKDIR"

for app in $APPS; do
  IFS='|' read -r APPNAME APP_TITLE APP_DESC APP_PLACEHOLDER HSL_HEX ACCENT_HEX <<< "$app"
  echo "==== Building $APPNAME ===="

  # Create next.js app
  npx create-next-app@latest "$APPNAME" --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-turbopack --yes 2>&1 | tail -5

  # Copy template files
  mkdir -p "$APPNAME/src/app/api/generate"
  cp "$TEMPLATE/app/page.tsx" "$APPNAME/src/app/page.tsx"
  cp "$TEMPLATE/api/generate/route.ts" "$APPNAME/src/app/api/generate/route.ts"

  # Update page.tsx with app-specific content
  sed -i '' \
    -e "s|APP_NAME|'$APPNAME'|g" \
    -e "s|APP_TITLE|'$APP_TITLE'|g" \
    -e "s|APP_DESCRIPTIONS\\[APP_NAME\\]|'$APP_DESC'|g" \
    -e "s|APP_PLACEHOLDERS\\[APP_NAME\\]|'$APP_PLACEHOLDER'|g" \
    -e "s|ACCENT_HEX|'$ACCENT_HEX'|g" \
    -e "s|ACCENT_COLOR|${HSL_HEX//,/}|g" \
    "$APPNAME/src/app/page.tsx"

  # Build
  cd "$APPNAME"
  npm run build 2>&1 | tail -10

  # Git init and push
  git init && git add -A && git commit -m "feat: initial commit"
  gh repo create NebulaLumino/"$APPNAME" --public --push 2>/dev/null || \
    { git remote add origin "https://github.com/NebulaLumino/$APPNAME.git" 2>/dev/null; git push -u origin main; }

  cd "$WORKDIR"
  rm -rf "$APPNAME/node_modules" "$APPNAME/.next"
  echo "==== Done $APPNAME ===="
done
