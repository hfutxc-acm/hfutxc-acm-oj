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
        { name: "red", hex: "#ef5350" },
        { name: "pink", hex: "#e91e63" },
        { name: "purple", hex: "#ab47bc" },
        { name: "deep purple", hex: "#7e57c2" },
        { name: "indigo", hex: "#3f51b5" },
        { name: "blue", hex: "#2196f3" },
        { name: "light blue", hex: "#03a9f4" },
        { name: "cyan", hex: "#00bcd4" },
        { name: "teal", hex: "#009688" },
        { name: "green", hex: "#4caf50" },
        { name: "light green", hex: "#8bc34a" },
        { name: "lime", hex: "#c0ca33" },
        { name: "yellow", hex: "#fbc02d" },
        { name: "amber", hex: "#ffc107" },
        { name: "orange", hex: "#ff9800" },
        { name: "deep orange", hex: "#ff5722" },
        { name: "brown", hex: "#795548" },
        { name: "grey", hex: "#757575" },
        { name: "blue grey", hex: "#607d8b" },
        { name: "black", hex: "#000000" }
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
        btn.style.backgroundColor = c.hex;
        
        btn.onclick = () => {
            document.body.setAttribute("data-md-color-primary", c.name);
            
            // ELEGANT NATIVE WAY: Update Material's internal palette state
            if (typeof __md_get !== 'undefined' && typeof __md_set !== 'undefined') {
                const palette = __md_get("__palette");
                if (palette && palette.color) {
                    palette.color.primary = c.name;
                    __md_set("__palette", palette);
                }
            }
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
