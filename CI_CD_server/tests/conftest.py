from pathlib import Path
import sys

CWD = Path(__file__).parent
# this needs to be above `src` imports
sys.path.insert(0, str(CWD.parent))
