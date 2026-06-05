from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
repo_root_text = str(REPO_ROOT)
if repo_root_text not in sys.path:
    sys.path.insert(0, repo_root_text)

from foundry_hands_on.learning import print_script_learning_goal

print_script_learning_goal()
