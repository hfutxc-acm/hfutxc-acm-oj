document.addEventListener("DOMContentLoaded", function() {
    const header = document.querySelector(".md-header__option");
    if (!header) return;

    // Create a color picker wrapper
    const picker = document.createElement("div");
    picker.className = "md-header__button md-icon";
    picker.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-10 10c0 5.52 4.48 10 10 10a10 10 0 0 0 10-10 10 10 0 0 0-10-10m0 18c-4.42 0-8-3.58-8-8 0-4.42 3.58-8 8-8s8 3.58 8 8-3.58 8-8 8m-1-4a1 1 0 0 1-1-1 1 1 0 0 1 1-1 1 1 0 0 1 1 1 1 1 0 0 1-1 1m-4-1a1 1 0 0 1-1-1 1 1 0 0 1 1-1 1 1 0 0 1 1 1 1 1 0 0 1-1 1m9-1a1 1 0 0 1-1-1 1 1 0 0 1 1-1 1 1 0 0 1 1 1 1 1 0 0 1-1 1m-5-4a1 1 0 0 1-1-1 1 1 0 0 1 1-1 1 1 0 0 1 1 1 1 1 0 0 1-1 1m3-2a1 1 0 0 1-1-1 1 1 0 0 1 1-1 1 1 0 0 1 1 1 1 1 0 0 1-1 1Z"/></svg>';
    picker.title = "Change Theme Color";
    picker.style.cursor = "pointer";
    picker.style.marginLeft = "10px";

    const colors = [
        { name: "red", hex: "#ff8787" },
        { name: "pink", hex: "#fcc2d7" },
        { name: "purple", hex: "#e599f7" },
        { name: "deep-purple", hex: "#b197fc" },
        { name: "indigo", hex: "#91a7ff" },
        { name: "blue", hex: "#74c0fc" },
        { name: "light-blue", hex: "#66d9e8" },
        { name: "cyan", hex: "#63e6be" },
        { name: "teal", hex: "#38d9a9" },
        { name: "green", hex: "#8ce99a" },
        { name: "light-green", hex: "#b2f2bb" },
        { name: "lime", hex: "#d8f5a2" },
        { name: "yellow", hex: "#ffec99" },
        { name: "amber", hex: "#ffe066" },
        { name: "orange", hex: "#ffd43b" },
        { name: "rainbow", hex: "linear-gradient(to right, #ff6b6b, #ffb347, #ffeb3b, #77dd77, #4dd0e1, #64b5f6, #ba68c8)", isRainbow: true },
        { name: "brown", hex: "#e6ca90" },
        { name: "grey", hex: "#ced4da" },
        { name: "blue-grey", hex: "#a5d8ff" },
        { name: "black", hex: "#868e96" }
    ];
    
    // Custom dropdown
    const dropdown = document.createElement("div");
    dropdown.style.display = "none";
    dropdown.style.position = "absolute";
    dropdown.style.top = "48px";
    dropdown.style.right = "10px";
    dropdown.style.background = "var(--md-default-bg-color)";
    dropdown.style.boxShadow = "0 4px 6px rgba(0,0,0,0.3)";
    dropdown.style.padding = "10px";
    dropdown.style.borderRadius = "4px";
    dropdown.style.gridTemplateColumns = "repeat(5, 30px)";
    dropdown.style.gap = "5px";
    dropdown.style.zIndex = "100";

    colors.forEach(c => {
        const btn = document.createElement("div");
        btn.style.width = "30px";
        btn.style.height = "30px";
        btn.style.borderRadius = "50%";
        btn.style.cursor = "pointer";
        btn.setAttribute("title", c.name);
        if (c.isRainbow) {
            btn.style.background = c.hex;
        } else {
            btn.style.backgroundColor = c.hex;
        }
        
        btn.onclick = () => {
            localStorage.setItem("custom-primary-color", c.name);
            document.body.setAttribute("data-md-color-primary", c.name);
            dropdown.style.display = "none";
        };
        dropdown.appendChild(btn);
    });

    picker.onclick = (e) => {
        e.stopPropagation();
        dropdown.style.display = dropdown.style.display === "none" ? "grid" : "none";
    };

    document.body.onclick = () => { dropdown.style.display = "none"; };
    
    header.appendChild(picker);
    header.appendChild(dropdown);
});
