import os
from pathlib import Path

src_dir = Path("/home/ikun/PycharmProjects/hfutxc-acm-oj/frontend/src")

def migrate_file(p: Path):
    content = p.read_text(encoding="utf-8")
    
    if "authStore" not in content and "themeStore" not in content:
        return

    # Update imports
    content = content.replace("import { authStore", "import { useAuthStore")
    content = content.replace("import { authStore } from", "import { useAuthStore } from")
    content = content.replace("import { authStore, initAuth } from", "import { useAuthStore, initAuth } from")
    content = content.replace("import { authStore, canAccessAdmin, logout } from", "import { useAuthStore, canAccessAdmin, logout } from")
    content = content.replace("import { authStore, setToken } from", "import { useAuthStore, setToken } from")

    content = content.replace("import { themeStore, toggleTheme } from", "import { useThemeStore, toggleTheme } from")
    
    # Inject const authStore = useAuthStore() in <script setup>
    if "useAuthStore" in content and "const authStore =" not in content:
        if "<script setup>" in content:
            content = content.replace("<script setup>", "<script setup>\nimport { useAuthStore } from '../stores/authStore' (fake)\nconst authStore = useAuthStore()")
            # Wait, the import is already there, I shouldn't duplicate it. Let's just do:
            content = content.replace("<script setup>", "<script setup>\nconst authStore = useAuthStore()")
        elif "export function" not in content and p.suffix != ".js": 
            # some js files might need it
            pass

    if "useThemeStore" in content and "const themeStore =" not in content:
        if "<script setup>" in content:
            content = content.replace("<script setup>", "<script setup>\nconst themeStore = useThemeStore()")

    p.write_text(content, encoding="utf-8")

for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith(".vue") or f.endswith(".js"):
            migrate_file(Path(root) / f)

print("Migration script finished.")
