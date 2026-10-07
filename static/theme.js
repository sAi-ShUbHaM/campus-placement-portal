(() => {


    const root = document.documentElement;
    const storageKey = "campus-placement-theme";
    
    function getInitialTheme() {
    
        const saved = localStorage.getItem(storageKey);
    
        if (saved === "light" || saved === "dark") {
            return saved;
        }
    
        return window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark"
            : "light";
    }
    
    
    function applyTheme(theme) {
    
        root.setAttribute("data-theme", theme);
    
        localStorage.setItem(storageKey, theme);
    
        document.querySelectorAll("[data-theme-toggle]").forEach(button => {
    
            const icon = button.querySelector(".theme-icon");
    
            if (icon) {
                icon.textContent = theme === "dark" ? "☀" : "☾";
            }
    
            button.title =
                theme === "dark"
                    ? "Switch to light mode"
                    : "Switch to dark mode";
    
            button.setAttribute(
                "aria-label",
                theme === "dark"
                    ? "Switch to light mode"
                    : "Switch to dark mode"
            );
    
        });
    }
    
    
    function setupThemeButtons() {
    
        const buttons =
            document.querySelectorAll("[data-theme-toggle]");
    
        buttons.forEach(button => {
    
            if (button.dataset.themeReady === "true") {
                return;
            }
    
            button.dataset.themeReady = "true";
    
            button.addEventListener("click", () => {
    
                const currentTheme =
                    root.getAttribute("data-theme") || "light";
    
                const nextTheme =
                    currentTheme === "dark"
                        ? "light"
                        : "dark";
    
                applyTheme(nextTheme);
    
            });
    
        });
    
    }
    
    
    function initTheme() {
    
        applyTheme(getInitialTheme());
    
        setupThemeButtons();
    
    }
    
    
    if (document.readyState === "loading") {
    
        document.addEventListener(
            "DOMContentLoaded",
            initTheme
        );
    
    } else {
    
        initTheme();
    
    }

    
    })();
    