import re

with open("frontend/src/style.css", "r") as f:
    content = f.read()

# 1. Remove specific .dark overrides block
content = re.sub(r'/\* Specific dark mode selector overrides \*/.*', '', content, flags=re.DOTALL)

# 2. Add tokens to :root and :root.dark
root_dark_tokens = """
  --header-bg: rgba(17, 24, 39, 0.95);
  --nav-btn-color: #9ca3af;
  --nav-btn-active-bg: #1e293b;
  --heading-text: #f3f4f6;
  --tabbar-bg: #1f2937;
  --tabbar-btn-color: #9ca3af;
  --tabbar-active-bg: #111827;
  --table-th-bg: #1f2937;
  --table-th-text: #d1d5db;
  --table-td-border: #1f2937;
  --table-td-text: #e5e7eb;
  --table-hover-bg: rgba(255, 255, 255, 0.02);
  --control-bg: #111827;
  --control-border: #374151;
  --ghost-bg: #111827;
  --ghost-hover-bg: #1f2937;
  --pill-bg: #1f2937;
  --pill-text: #d1d5db;
  --badge-bg: #1e293b;
  --progress-bg: #1f2937;
}"""
content = content.replace("}\n\n:root.dark {", "  --header-bg: rgba(255, 255, 255, 0.95);\n  --nav-btn-color: #334155;\n  --nav-btn-active-bg: #e8f1fb;\n  --heading-text: #0f172a;\n  --tabbar-bg: #ffffff;\n  --tabbar-btn-color: #64748b;\n  --tabbar-active-bg: #f8fafc;\n  --table-th-bg: var(--panel-soft);\n  --table-th-text: #475569;\n  --table-td-border: #e5edf6;\n  --table-td-text: var(--text);\n  --table-hover-bg: #f8fbff;\n  --control-bg: #ffffff;\n  --control-border: #cbd5e1;\n  --ghost-bg: #ffffff;\n  --ghost-hover-bg: #f8fafc;\n  --pill-bg: #f8fafc;\n  --pill-text: #64748b;\n  --badge-bg: #e8f1fb;\n  --progress-bg: #e2e8f0;\n}\n\n:root.dark {")
content = content.replace("--primary-dark: #60a5fa;\n}", "--primary-dark: #60a5fa;\n" + root_dark_tokens)

# 3. Replace hardcoded colors in CSS components
replacements = [
    (r'background: rgba\(255, 255, 255, 0.95\);', r'background: var(--header-bg);'),
    (r'\.main-nav button,[\s\S]*?color: #334155;', r'.main-nav button,\n.user-chip {\n  min-height: 38px;\n  padding: 0 13px;\n  border: 0;\n  border-radius: 7px;\n  background: transparent;\n  color: var(--nav-btn-color);'),
    (r'background: #e8f1fb;', r'background: var(--nav-btn-active-bg);'),
    
    (r'\.page-heading h1,\n\.hero-section h1,\n\.statement h1,\n\.placeholder-page h1,\n\.profile-page h1 {\n  margin: 0;\n  color: #0f172a;', 
     r'.page-heading h1,\n.hero-section h1,\n.statement h1,\n.placeholder-page h1,\n.profile-page h1 {\n  margin: 0;\n  color: var(--heading-text);'),
     
    (r'\.stat-card strong {\n  font-size: 32px;\n  color: #0f172a;', 
     r'.stat-card strong {\n  font-size: 32px;\n  color: var(--heading-text);'),
     
    (r'\.control {\n  width: 100%;\n  min-height: 42px;\n  padding: 9px 11px;\n  border: 1px solid #cbd5e1;\n  border-radius: 7px;\n  background: #ffffff;', 
     r'.control {\n  width: 100%;\n  min-height: 42px;\n  padding: 9px 11px;\n  border: 1px solid var(--control-border);\n  border-radius: 7px;\n  background: var(--control-bg);'),
     
    (r'\.data-table th,\n\.data-table td {\n  padding: 13px 14px;\n  border-bottom: 1px solid #e5edf6;\n  text-align: left;\n  white-space: nowrap;\n}', 
     r'.data-table th,\n.data-table td {\n  padding: 13px 14px;\n  border-bottom: 1px solid var(--table-td-border);\n  text-align: left;\n  white-space: nowrap;\n  color: var(--table-td-text);\n}'),
     
    (r'\.data-table th {\n  background: var\(--panel-soft\);\n  color: #475569;', 
     r'.data-table th {\n  background: var(--table-th-bg);\n  color: var(--table-th-text);'),
     
    (r'\.data-table tbody tr:hover {\n  background: #f8fbff;', 
     r'.data-table tbody tr:hover {\n  background: var(--table-hover-bg);'),
     
    (r'\.ghost-btn {\n  border: 1px solid #cbd5e1;\n  background: #ffffff;', 
     r'.ghost-btn {\n  border: 1px solid var(--control-border);\n  background: var(--ghost-bg);'),
     
    (r'\.badge,\n\.tag {\n  background: #e8f1fb;', 
     r'.badge,\n.tag {\n  background: var(--badge-bg);'),
     
    (r'\.tabbar {\n  display: flex;\n  gap: 20px;\n  border-bottom: 1px solid var\(--border\);\n}', 
     r'.tabbar {\n  display: flex;\n  gap: 20px;\n  border-bottom: 1px solid var(--border);\n  background: var(--tabbar-bg);\n}'),
     
    (r'\.tabbar button {\n  padding: 12px 4px;\n  border: 0;\n  background: transparent;\n  color: #64748b;', 
     r'.tabbar button {\n  padding: 12px 4px;\n  border: 0;\n  background: transparent;\n  color: var(--tabbar-btn-color);'),
     
    (r'\.tabbar button\.active {\n  color: var\(--primary-dark\);\n  border-bottom: 2px solid var\(--primary-dark\);\n}', 
     r'.tabbar button.active {\n  color: var(--nav-btn-active-color, var(--primary-dark));\n  border-bottom: 2px solid var(--primary-dark);\n  background: var(--tabbar-active-bg);\n}'),
     
    (r'\.case-pill,\n\.problem-status-list span {\n  display: inline-block;\n  padding: 3px 8px;\n  border-radius: 4px;\n  background: #f8fafc;\n  color: #64748b;\n  font-size: 13px;\n  font-weight: 600;\n}', 
     r'.case-pill,\n.problem-status-list span {\n  display: inline-block;\n  padding: 3px 8px;\n  border-radius: 4px;\n  background: var(--pill-bg);\n  color: var(--pill-text);\n  font-size: 13px;\n  font-weight: 600;\n}'),
     
    (r'\.progress-bar {\n  width: 100%;\n  height: 8px;\n  background: #e2e8f0;\n  border-radius: 4px;\n  overflow: hidden;\n}', 
     r'.progress-bar {\n  width: 100%;\n  height: 8px;\n  background: var(--progress-bg);\n  border-radius: 4px;\n  overflow: hidden;\n}')
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open("frontend/src/style.css", "w") as f:
    f.write(content)

print("Refactored style.css successfully!")
