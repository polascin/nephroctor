/* Shared behaviour for the legal documents in /legal/.
   Two things only: the theme toggle (same contract as the home page) and the
   SK/EN document switch. The Slovak version is the legally binding one and is
   the default, so a visitor without JavaScript still gets a complete document. */
(function () {
    'use strict';

    var store = {
        get: function (key) {
            try { return localStorage.getItem(key); } catch (e) { return null; }
        },
        set: function (key, value) {
            try { localStorage.setItem(key, value); } catch (e) { /* storage blocked */ }
        }
    };

    /* --- Theme ---------------------------------------------------------- */
    var toggle = document.getElementById('theme-toggle');
    var LABELS = {
        sk: { dark: 'Tmavý režim', light: 'Svetlý režim' },
        en: { dark: 'Dark mode', light: 'Light mode' }
    };
    var SUN = '<path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 00-1.41-1.41l-1.06 1.06a.996.996 0 000 1.41c.39.39 1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06a.996.996 0 00-1.41 0z"/>';
    var MOON = '<path d="M9 2c-1.05 0-2.05.16-3 .46 1.89 1 3.18 2.99 3.18 5.27 0 3.31-2.69 6-6 6-.71 0-1.39-.13-2.02-.36C3.92 18.86 8.56 22 14 22c5.52 0 10-4.48 10-10S19.52 2 14 2c-.63 0-1.24.06-1.83.17C11.06 2.06 10.04 2 9 2z"/>';

    var docLang = 'sk';

    function isDark() {
        var explicit = document.documentElement.getAttribute('data-theme');
        if (explicit === 'dark') return true;
        if (explicit === 'light') return false;
        return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
    }

    function paintToggle() {
        if (!toggle) return;
        var dark = isDark();
        var label = dark ? LABELS[docLang].light : LABELS[docLang].dark;
        toggle.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            + (dark ? SUN : MOON) + '</svg>';
        toggle.setAttribute('aria-label', label);
        toggle.setAttribute('title', label);
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            var next = isDark() ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            store.set('nephroctor-theme', next);
            paintToggle();
        });
    }

    /* --- SK / EN document switch ---------------------------------------- */
    var blocks = document.querySelectorAll('[data-lang-block]');
    var buttons = document.querySelectorAll('[data-doc-lang]');

    function showVersion(lang, updateUrl) {
        if (lang !== 'en') lang = 'sk';
        docLang = lang;

        Array.prototype.forEach.call(blocks, function (el) {
            el.hidden = el.getAttribute('data-lang-block') !== lang;
        });
        Array.prototype.forEach.call(buttons, function (btn) {
            btn.setAttribute('aria-pressed', String(btn.getAttribute('data-doc-lang') === lang));
        });

        document.documentElement.lang = lang;
        var title = document.querySelector('[data-title-' + lang + ']');
        if (title) document.title = title.getAttribute('data-title-' + lang);

        paintToggle();

        if (updateUrl) {
            try {
                history.replaceState(null, '', lang === 'sk'
                    ? window.location.pathname
                    : window.location.pathname + '?lang=en');
            } catch (e) { /* replaceState unavailable (e.g. file:// origin) */ }
        }
    }

    Array.prototype.forEach.call(buttons, function (btn) {
        btn.addEventListener('click', function () {
            showVersion(btn.getAttribute('data-doc-lang'), true);
        });
    });

    /* Any of the 24 site languages maps onto one of the two document versions:
       Slovak for sk/cs (Czech readers get the binding original), English for the
       rest. An unrecognised code is treated as no signal at all, exactly as the
       home page treats it, so it falls through instead of forcing English. */
    var SITE_LANGUAGES = ['sk', 'cs', 'en', 'de', 'fr', 'es', 'it', 'pt', 'nl', 'pl', 'hu', 'ro',
                          'bg', 'hr', 'sl', 'da', 'sv', 'fi', 'et', 'lv', 'lt', 'el', 'ga', 'mt'];

    function resolveDocLang(code) {
        if (!code || SITE_LANGUAGES.indexOf(code) === -1) return null;
        return (code === 'sk' || code === 'cs') ? 'sk' : 'en';
    }

    var requested = null;
    try {
        requested = new URLSearchParams(window.location.search).get('lang');
    } catch (e) { /* URLSearchParams unavailable */ }

    showVersion(resolveDocLang(requested) || resolveDocLang(store.get('nephroctor-lang')) || 'sk', false);
})();
