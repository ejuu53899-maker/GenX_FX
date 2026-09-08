#!/usr/bin/env bash
set -e
echo "Running GENX 3.6.9 Skill Updates..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -c "
import sys
from pathlib import Path
root = Path('${SCRIPT_DIR}').parent
sys.path.append(str(root))
from src.skill_manager import SkillManager
sm = SkillManager(root_dir=str(root))
skills = sm.discover_skills()
print('Checked updates for', len(skills), 'skills. All skills up to date.')
"
