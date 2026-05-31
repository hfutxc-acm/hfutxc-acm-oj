import os
from pathlib import Path
import re

src_dir = Path("/home/ikun/PycharmProjects/hfutxc-acm-oj/frontend/src")

def fix_file(p: Path):
    content = p.read_text(encoding="utf-8")
    original = content
    
    if "authStore" not in content:
        return

    # Update imports
    content = re.sub(r"import \{(.*?)\} from ['\"](?:\.\./)*stores/authStore(?:\.js)?['\"]", 
                     r"import {\1} from '../stores/authStore'", content) # normalize
    
    # Simple replace
    content = content.replace("authStore,", "useAuthStore,")
    content = content.replace("authStore }", "useAuthStore }")
    content = content.replace("initAuth", "useAuthStore") # we will just use useAuthStore().initAuth()
    content = content.replace("setToken", "useAuthStore") 
    content = content.replace("logout", "useAuthStore")
    content = content.replace("canAccessAdmin", "useAuthStore")
    
    # Dedup imports
    if "useAuthStore" in content:
        import_match = re.search(r"import \{(.*?)\} from ['\"](\.\./)*stores/authStore(\.js)?['\"]", content)
        if import_match:
            new_import = f"import {{ useAuthStore }} from '{import_match.group(2) or '../'}stores/authStore'"
            content = content[:import_match.start()] + new_import + content[import_match.end():]

    # Replace usages
    content = content.replace("authStore.", "authStore().")
    content = content.replace("setToken(", "authStore().setToken(")
    content = content.replace("logout(", "authStore().logout(")
    content = content.replace("initAuth(", "authStore().initAuth(")
    content = content.replace("canAccessAdmin(", "authStore().canAccessAdmin")

    # In Vue templates we can't use authStore(). inside template easily if authStore is not defined in script setup.
    # To avoid breaking Vue templates, we need to inject `const authStore = useAuthStore` in script setup,
    # OR we just replace `authStore.` with `useAuthStore().` directly everywhere.
    # Wait, in Vue template, `useAuthStore().currentUser` works if `useAuthStore` is imported!
    content = content.replace("authStore().", "useAuthStore().")
    content = content.replace("authStore()", "useAuthStore()")
    
    if content != original:
        p.write_text(content, encoding="utf-8")
        print(f"Fixed {p.name}")

for root, dirs, files in os.walk(src_dir):
    for f in files:
        if (f.endswith(".vue") or f.endswith(".js")) and f != "authStore.js":
            fix_file(Path(root) / f)

print("Auth store fix finished.")
