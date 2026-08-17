/* ============================================================
   LUXXOR VACATION — Motor de scroll del hero
   ------------------------------------------------------------
   Traduce la posición del scroll a un progreso 0 → 1 y lo publica
   como variables CSS. Toda la animación vive en el CSS; aquí solo
   se calcula el "cuándo".
   ============================================================ */

(function () {
  'use strict';

  var hero = document.getElementById('hero');
  if (!hero) return;

  // Respetamos la preferencia del sistema: sin movimiento, sin motor.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var root = document.documentElement;
  var ticking = false;

  /** Normaliza v dentro del tramo [a, b] devolviendo 0 → 1. */
  function range(v, a, b) {
    if (v <= a) return 0;
    if (v >= b) return 1;
    return (v - a) / (b - a);
  }

  /** Suavizado (ease-in-out) para que nada arranque ni pare en seco. */
  function ease(t) {
    return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  }

  function update() {
    ticking = false;

    var scrolled = -hero.getBoundingClientRect().top;
    var travel = hero.offsetHeight - window.innerHeight;
    var p = travel > 0 ? Math.min(Math.max(scrolled / travel, 0), 1) : 0;

    root.style.setProperty('--p', p.toFixed(4));

    // Tramos de la secuencia (los mismos beats que el vídeo de referencia)
    root.style.setProperty('--p-copy',     ease(range(p, 0.00, 0.30)).toFixed(4)); // se va el titular
    root.style.setProperty('--p-villa',    ease(range(p, 0.00, 0.80)).toFixed(4)); // sube la villa
    root.style.setProperty('--p-mark',     ease(range(p, 0.32, 0.58)).toFixed(4)); // entra el wordmark
    root.style.setProperty('--p-mark-out', ease(range(p, 0.78, 0.95)).toFixed(4)); // sale el wordmark
    root.style.setProperty('--p-veil',     ease(range(p, 0.72, 1.00)).toFixed(4)); // velo final
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
