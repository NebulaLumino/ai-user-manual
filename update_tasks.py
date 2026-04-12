#!/usr/bin/env python3
"""Update task files 3591-3630 to Complete status."""
import os, re

WORKDIR = "/Users/nebulalumino/.openclaw/workspace"
TASKS_DIR = f"{WORKDIR}/tasks"

# Apps 3591-3620: GitHub repos confirmed pushed
APPS = {
    3591: "https://github.com/NebulaLumino/ai-melody-composer",
    3592: "https://github.com/NebulaLumino/ai-chord-progression",
    3593: "https://github.com/NebulaLumino/ai-album-cover",
    3594: "https://github.com/NebulaLumino/ai-podcast-script",
    3595: "https://github.com/NebulaLumino/ai-brand-colors",
    3596: "https://github.com/NebulaLumino/ai-typography",
    3597: "https://github.com/NebulaLumino/ai-logo-brief",
    3598: "https://github.com/NebulaLumino/ai-ui-patterns",
    3599: "https://github.com/NebulaLumino/ai-storyboard",
    3600: "https://github.com/NebulaLumino/ai-shot-list",
    3601: "https://github.com/NebulaLumino/ai-haiku-generator",
    3602: "https://github.com/NebulaLumino/ai-screenplay",
    3603: "https://github.com/NebulaLumino/ai-video-essay",
    3604: "https://github.com/NebulaLumino/ai-fashion-mood",
    3605: "https://github.com/NebulaLumino/ai-interior-design",
    3606: "https://github.com/NebulaLumino/ai-architecture-style",
    3607: "https://github.com/NebulaLumino/ai-creative-brief",
    3608: "https://github.com/NebulaLumino/ai-comic-panels",
    3609: "https://github.com/NebulaLumino/ai-print-pattern",
    3610: "https://github.com/NebulaLumino/ai-animation-style",
    3611: "https://github.com/NebulaLumino/ai-photo-composition",
    3612: "https://github.com/NebulaLumino/ai-band-merch",
    3613: "https://github.com/NebulaLumino/ai-museum-narrative",
    3614: "https://github.com/NebulaLumino/ai-dj-mix",
    3615: "https://github.com/NebulaLumino/ai-street-art",
    3616: "https://github.com/NebulaLumino/ai-boardgame-mechanics",
    3617: "https://github.com/NebulaLumino/ai-cocktail-gen",
    3618: "https://github.com/NebulaLumino/ai-tattoo-brief",
    3619: "https://github.com/NebulaLumino/ai-image-palette",
    3620: "https://github.com/NebulaLumino/ai-ux-research",
}

# Doc tasks 3621-3630
DOCS = {
    3621: "docs/task-3621-ai-generated-music-sampling-music-industry.md",
    3622: "docs/task-3622-generative-ai-architecture-parametric-design.md",
    3623: "docs/task-3623-ai-fashion-design-trend-forecasting.md",
    3624: "docs/task-3624-ai-film-production-script-coverage-editing.md",
    3625: "docs/task-3625-ai-game-art-procedural-worlds-npc.md",
    3626: "docs/task-3626-ai-advertising-neuromarketing-subconscious.md",
    3627: "docs/task-3627-ai-interior-design-ar-furniture.md",
    3628: "docs/task-3628-ai-performing-arts-choreography-stage.md",
    3629: "docs/task-3629-ai-publishing-cover-design-interactive-books.md",
    3630: "docs/task-3630-ai-craft-movements-artisan-maker-economy.md",
}

def update_app_task(task_num, repo_url):
    filepath = f"{TASKS_DIR}/task-{task_num}.md"
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        return
    with open(filepath) as f:
        content = f.read()
    # Update status
    content = re.sub(r'## Status:.*', '## Status: ✅ Complete', content)
    # Update GitHub URL
    content = re.sub(r'## GitHub Repo:.*', f'## GitHub Repo: {repo_url}', content)
    # Update progress checkboxes
    content = content.replace('- [ ] Scaffold', '- [x] Scaffold')
    content = content.replace('- [ ] Implement', '- [x] Implement')
    content = content.replace('- [ ] Build', '- [x] Build')
    content = content.replace('- [ ] GitHub push', '- [x] GitHub push')
    content = content.replace('- [ ] Cleanup', '- [x] Cleanup')
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  Updated task-{task_num}")

def update_doc_task(task_num, doc_path):
    filepath = f"{TASKS_DIR}/task-{task_num}.md"
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        return
    with open(filepath) as f:
        content = f.read()
    # Update status
    content = re.sub(r'## Status:.*', '## Status: ✅ Complete', content)
    # Update path if present
    if doc_path:
        content = re.sub(r'## Doc Path:.*', f'## Doc Path: {doc_path}', content)
    # Update progress
    content = content.replace('- [ ] Write', '- [x] Write')
    content = content.replace('- [ ] Review', '- [x] Review')
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  Updated task-{task_num}")

print("Updating app tasks 3591-3620...")
for task_num in range(3591, 3621):
    update_app_task(task_num, APPS.get(task_num, ""))

print("\nUpdating doc tasks 3621-3630...")
for task_num in range(3621, 3631):
    update_doc_task(task_num, DOCS.get(task_num, ""))

print("\nDone!")
