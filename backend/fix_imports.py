import glob

files = glob.glob("**/*.py", recursive=True)
for f in files:
    if f.startswith(".venv"): continue
    with open(f, "r") as file:
        content = file.read()
    if "from sqlmodel.ext.asyncio.session import AsyncSession" in content:
        content = content.replace("from sqlmodel.ext.asyncio.session import AsyncSession", "from sqlmodel.ext.asyncio.session import AsyncSession")
        with open(f, "w") as file:
            file.write(content)
