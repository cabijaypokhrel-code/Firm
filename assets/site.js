// Shared site behavior: sticky-header compaction + mobile nav toggle
(function () {
    'use strict';

    var header = document.getElementById('siteHeader');
    if (header) {
        var ticking = false;
        window.addEventListener('scroll', function () {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(function () {
                header.classList.toggle('site-header--compact', window.scrollY > 48);
                ticking = false;
            });
        }, { passive: true });
    }

    var toggle = document.getElementById('navToggle');
    var nav = document.getElementById('primaryNav');
    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var open = nav.classList.toggle('open');
            toggle.setAttribute('aria-expanded', String(open));
        });
    }
})();
