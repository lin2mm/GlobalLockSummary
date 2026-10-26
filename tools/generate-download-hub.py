import os
import shutil

os.makedirs('assets/downloads', exist_ok=True)

files_to_serve = [
    ('docs/01_METHODOLOGY_AND_CONTEXT_MEMORY.md', '01_METHODOLOGY_AND_CONTEXT_MEMORY.md'),
    ('docs/00_AUTONOMOUS_OPTIMIZATION_LOOP.md', '00_AUTONOMOUS_OPTIMIZATION_LOOP.md'),
    ('docs/10_SMART_LOCK_RETROFIT_METHODOLOGY.md', '10_SMART_LOCK_RETROFIT_METHODOLOGY.md'),
    ('docs/02_PROJECT_PLAN_AND_CONVENTIONS.xlsx', '02_PROJECT_PLAN_AND_CONVENTIONS.xlsx'),
    ('docs/03_GLOBAL_LOCK_DATA_INDEX.xlsx', '03_GLOBAL_LOCK_DATA_INDEX.xlsx'),
    ('docs/07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx', '07_VISUAL_COLOR_HIERARCHY_DESIGN.xlsx'),
    ('docs/08_HARDWARE_ADAPTERS_AND_BOM.xlsx', '08_HARDWARE_ADAPTERS_AND_BOM.xlsx'),
    ('docs/09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx', '09_IMAGE_ASSETS_HEALTH_AUDIT.xlsx')
]

for src, dst in files_to_serve:
    if os.path.exists(src):
        target = os.path.join('assets/downloads', dst)
        shutil.copyfile(src, target)
        print(f"Copied {src} -> {target}")

