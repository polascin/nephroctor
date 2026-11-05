/* Clarity is loaded only after explicit analytics consent on public pages. */
(() => {
    "use strict";
    const config = document.currentScript;
    if (!config || !/^[a-z0-9]+$/.test(config.dataset.project || "")) return;
    const allowed = (config.dataset.paths || "/,/index.php").split(",");
    if (!allowed.includes(location.pathname)) return;
    if ([...new URLSearchParams(location.search).keys()].some(k => !["lang", "slug", "page", "category"].includes(k))) return;
    const project = config.dataset.project;
    const external = config.dataset.consent === "external";
    const key = "clarity-consent-v1-" + project;
    const sk = document.documentElement.lang.startsWith("sk");
    let loaded = false;
    let banner;
    let previousFocus = null;
    let dismissible = false;
    const read = () => { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } };
    const save = granted => { try { localStorage.setItem(key, JSON.stringify({granted, expires: Date.now() + 180 * 86400000})); } catch { /* Consent still applies for this page. */ } };
    const focusable = root => [...root.querySelectorAll("a[href], button:not([disabled])")].filter(el => !el.hasAttribute("disabled"));
    function closeBanner() {
        if (!banner) return;
        banner.removeEventListener("keydown", onKeyDown);
        banner.remove();
        banner = null;
        const restore = previousFocus;
        previousFocus = null;
        dismissible = false;
        if (restore && typeof restore.focus === "function") restore.focus();
    }
    function onKeyDown(event) {
        if (!banner) return;
        if (event.key === "Escape") {
            if (!dismissible) return;
            event.preventDefault();
            closeBanner();
            return;
        }
        if (event.key !== "Tab") return;
        const items = focusable(banner);
        if (!items.length) return;
        const first = items[0];
        const last = items[items.length - 1];
        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
    }
    function apply(granted, persist = true) {
        if (persist && !external) save(granted);
        if (granted) {
            if (!window.clarity) window.clarity = function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
            window.clarity("consentv2", {analytics_Storage: "granted", ad_Storage: "denied"});
            if (!loaded) {
                // Mask all page text, including any content entered by a visitor.
                document.body.setAttribute("data-clarity-mask", "true");
                const script = document.createElement("script");
                script.async = true;
                script.src = "https://www.clarity.ms/tag/" + project;
                document.head.appendChild(script);
                loaded = true;
            }
        } else {
            if (window.clarity) window.clarity("consentv2", {analytics_Storage: "denied", ad_Storage: "denied"});
            for (const name of ["_clck", "_clsk"]) {
                document.cookie = name + "=; Max-Age=0; Path=/; SameSite=Lax";
                const parts = location.hostname.split(".");
                while (parts.length > 1) {
                    document.cookie = name + "=; Max-Age=0; Path=/; Domain=." + parts.join(".") + "; SameSite=Lax";
                    parts.shift();
                }
            }
            // Stop the already loaded SDK, including its cookieless mode.
            if (loaded && persist) location.reload();
        }
        closeBanner();
    }
    if (external) {
        window.addEventListener("site:analytics-consent", e => apply(e.detail === true));
        return;
    }
    const css = document.createElement("link");
    css.rel = "stylesheet";
    // Keep any ?v= (or other) query from the script URL so CSS is not stuck on
    // a day-long browser cache when the loader itself was cache-busted.
    const scriptUrl = new URL(config.src, location.href);
    const cssUrl = new URL("clarity-consent.css", scriptUrl);
    cssUrl.search = scriptUrl.search;
    css.href = cssUrl.href;
    document.head.appendChild(css);
    const settings = document.createElement("button");
    settings.type = "button";
    settings.className = "clarity-settings";
    settings.textContent = sk ? "Nastavenia analytiky" : "Analytics settings";
    settings.addEventListener("click", () => show(true));
    (document.querySelector("footer") || document.body).appendChild(settings);
    function show(fromSettings = false) {
        if (banner) {
            if (fromSettings) banner.querySelector("button").focus();
            return;
        }
        dismissible = fromSettings;
        previousFocus = fromSettings ? document.activeElement : null;
        banner = document.createElement("section");
        banner.className = "clarity-consent";
        banner.setAttribute("role", "dialog");
        banner.setAttribute("aria-modal", "true");
        banner.setAttribute("aria-labelledby", "clarity-consent-title");
        banner.setAttribute("aria-describedby", "clarity-consent-desc");
        banner.tabIndex = -1;
        const title = document.createElement("h2");
        title.id = "clarity-consent-title";
        title.textContent = sk ? "Voliteľná analytika" : "Optional analytics";
        const text = document.createElement("p");
        text.id = "clarity-consent-desc";
        text.textContent = sk
            ? "S vaším súhlasom používame Microsoft Clarity na meranie návštevnosti, kliknutí, posúvania a záznamov používania verejných stránok. Text je maskovaný. Bez súhlasu sa Clarity nenačíta. Reklamný súhlas zostáva vypnutý. Voľbu môžete kedykoľvek zmeniť v nastaveniach analytiky."
            : "With your consent, we use Microsoft Clarity for visits, clicks, scrolling and session recordings on public pages. Text is masked. Clarity does not load without consent. Advertising consent stays denied. You can change your choice in Analytics settings at any time.";
        const link = document.createElement("a");
        link.href = config.dataset.privacy || "/privacy.php";
        link.textContent = sk ? "Ochrana súkromia" : "Privacy policy";
        const decline = document.createElement("button");
        decline.type = "button";
        decline.textContent = sk ? "Odmietnuť" : "Decline";
        decline.addEventListener("click", () => apply(false));
        const accept = document.createElement("button");
        accept.type = "button";
        accept.setAttribute("data-choice", "allow");
        accept.textContent = sk ? "Povoliť analytiku" : "Allow analytics";
        accept.addEventListener("click", () => apply(true));
        banner.append(title, text, link, decline, accept);
        banner.addEventListener("keydown", onKeyDown);
        document.body.appendChild(banner);
        if (fromSettings) decline.focus();
        else banner.focus();
    }
    const stored = read();
    if (stored && stored.expires > Date.now() && typeof stored.granted === "boolean") apply(stored.granted, false);
    else show();
    window.addEventListener("storage", e => {
        if (e.key !== key) return;
        const value = read();
        if (!value || !value.granted || value.expires <= Date.now()) { if (loaded) location.reload(); }
        else apply(true, false);
    });
})();
