import os
from pathlib import Path
import re

src_dir = Path("/home/ikun/PycharmProjects/hfutxc-acm-oj/frontend/src")

def fix_file(p: Path):
    content = p.read_text(encoding="utf-8")
    original = content
    
    if "themeStore" not in content:
        return

    # Update imports
    content = re.sub(r"import \{(.*?)\} from ['\"](?:\.\./)*stores/themeStore(?:\.js)?['\"]", 
                     r"import {\1} from '../stores/themeStore'", content) # normalize
    
    # Simple replace
    content = content.replace("themeStore,", "useThemeStore,")
    content = content.replace("themeStore }", "useThemeStore }")
    content = content.replace("toggleTheme", "useThemeStore") 
    
    # Dedup imports
    if "useThemeStore" in content:
        import_match = re.search(r"import \{(.*?)\} from ['\"](\.\./)*stores/themeStore(\.js)?['\"]", content)
        if import_match:
            new_import = f"import {{ useThemeStore }} from '{import_match.group(2) or '../'}stores/themeStore'"
            content = content[:import_match.start()] + new_import + content[import_match.end():]

    # Replace usages
    content = content.replace("themeStore.", "themeStore().")
    content = content.replace("toggleTheme(", "themeStore().toggleTheme(")

    # Just like useAuthStore
    content = content.replace("themeStore().", "useThemeStore().")
    content = content.replace("themeStore()", "useThemeStore()")
    
    if content != original:
        p.write_text(content, encoding="utf-8")
        print(f"Fixed {p.name}")

for root, dirs, files in os.walk(src_dir):
    for f in files:
        if (f.endswith(".vue") or f.endswith(".js")) and f != "themeStore.js":
            fix_file(Path(root) / f)

print("Theme store fix finished.")
