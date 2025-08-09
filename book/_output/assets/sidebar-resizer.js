// Make Quarto sidebar resizable by dragging a vertical handle
(function () {
  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function pxToNumber(px) {
    if (typeof px === 'number') return px;
    const n = Number(String(px).replace('px', ''));
    return isNaN(n) ? 0 : n;
  }

  function initSidebarResizer() {
    const sidebar = document.getElementById('quarto-sidebar');
    if (!sidebar) return;

    // Only enable on desktop-like layout when sidebar is visible horizontally
    const mq = window.matchMedia('(min-width: 992px)');
    if (!mq.matches) return;

    // Create resizer handle if not exists
    let resizer = document.getElementById('sidebar-resizer');
    if (!resizer) {
      resizer = document.createElement('div');
      resizer.id = 'sidebar-resizer';
      document.body.appendChild(resizer);
    }

    const rootStyle = getComputedStyle(document.documentElement);
    const minWidth = pxToNumber(rootStyle.getPropertyValue('--sidebar-width-min') || 180);
    // Max in vw; compute absolute max against viewport
    const maxVw = String(rootStyle.getPropertyValue('--sidebar-width-max-vw') || '60vw').trim();
    const vw = window.innerWidth / 100;
    const maxWidth = maxVw.endsWith('vw') ? pxToNumber(parseFloat(maxVw) * vw) : pxToNumber(maxVw);

    // Initialize position from CSS variable or current sidebar width
    const initial = getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width');
    let current = pxToNumber(initial) || sidebar.getBoundingClientRect().width;
    current = clamp(current, minWidth, maxWidth);
    document.documentElement.style.setProperty('--sidebar-width', current + 'px');

    function updateHandlePosition(px) {
      document.documentElement.style.setProperty('--sidebar-width', px + 'px');
      // resizer is positioned via CSS using the variable
    }

    let dragging = false;
    let startX = 0;
    let startWidth = current;

    function onDown(e) {
      dragging = true;
      resizer.classList.add('active');
      startX = e.touches ? e.touches[0].clientX : e.clientX;
      startWidth = pxToNumber(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width'));
      e.preventDefault();
    }

    function onMove(e) {
      if (!dragging) return;
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const delta = clientX - startX;
      const next = clamp(startWidth + delta, minWidth, maxWidth);
      updateHandlePosition(next);
    }

    function onUp() {
      if (!dragging) return;
      dragging = false;
      resizer.classList.remove('active');
      // Persist width in localStorage
      const finalWidth = pxToNumber(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width'));
      try { localStorage.setItem('quartoSidebarWidth', String(finalWidth)); } catch {}
    }

    resizer.addEventListener('mousedown', onDown, { passive: false });
    resizer.addEventListener('touchstart', onDown, { passive: false });
    window.addEventListener('mousemove', onMove, { passive: false });
    window.addEventListener('touchmove', onMove, { passive: false });
    window.addEventListener('mouseup', onUp);
    window.addEventListener('touchend', onUp);

    // Restore width if previously saved
    try {
      const saved = pxToNumber(localStorage.getItem('quartoSidebarWidth'));
      if (saved) {
        updateHandlePosition(clamp(saved, minWidth, maxWidth));
      }
    } catch {}

    // Recompute bounds on resize
    window.addEventListener('resize', () => {
      const vw2 = window.innerWidth / 100;
      const maxWidth2 = maxVw.endsWith('vw') ? pxToNumber(parseFloat(maxVw) * vw2) : maxWidth;
      const currentWidth = pxToNumber(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width'));
      const adjusted = clamp(currentWidth, minWidth, maxWidth2);
      updateHandlePosition(adjusted);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSidebarResizer);
  } else {
    initSidebarResizer();
  }
})();


